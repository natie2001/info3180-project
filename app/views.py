from app import app, db
from app.models import Member, UserDetail, Tag, SwipeAction, Connection, DirectMessage, SavedProfile
from flask import request, jsonify, session, send_from_directory
from functools import wraps
import os

PERMITTED_FILE_TYPES = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def is_valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PERMITTED_FILE_TYPES

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

def fetch_or_build_tag(label_text):
    label_text = label_text.strip().lower()
    tag = Tag.query.filter_by(label=label_text).first()
    if not tag:
        tag = Tag(label=label_text)
        db.session.add(tag)
        db.session.flush()
    return tag

def check_connection(peer1_id, peer2_id):
    return Connection.query.filter(
        ((Connection.peer_a_id == peer1_id) & (Connection.peer_b_id == peer2_id)) |
        ((Connection.peer_a_id == peer2_id) & (Connection.peer_b_id == peer1_id))
    ).first() is not None

def calculate_compatibility(base_profile, candidate_profile):
    """Generates a compatibility score (0-100) based on shared traits."""
    points = 0

    base_tags = {t.label for t in base_profile.tags}
    candidate_tags = {t.label for t in candidate_profile.tags}
    overlap = base_tags & candidate_tags
    if base_tags:
        points += min(40, int((len(overlap) / len(base_tags)) * 40))

    age_gap = abs(base_profile.years_old - candidate_profile.years_old)
    if age_gap <= 2:
        points += 20
    elif age_gap <= 5:
        points += 15
    elif age_gap <= 10:
        points += 10

    if base_profile.city_area and candidate_profile.city_area:
        if base_profile.city_area.lower() == candidate_profile.city_area.lower():
            points += 25
        elif base_profile.home_parish and candidate_profile.home_parish:
            if base_profile.home_parish.lower() == candidate_profile.home_parish.lower():
                points += 10

    if base_profile.connection_goal and candidate_profile.connection_goal:
        if base_profile.connection_goal == candidate_profile.connection_goal:
            points += 15

    return round(points, 1)

# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def handle_registration():
    payload = request.get_json()

    mandatory = ['username', 'email', 'password']
    for req in mandatory:
        if not payload.get(req):
            return jsonify({'error': f'Missing required field: {req}'}), 400

    if Member.query.filter_by(email_address=payload['email']).first():
        return jsonify({'error': 'Email is already registered'}), 409

    if Member.query.filter_by(handle=payload['username']).first():
        return jsonify({'error': 'Username is already taken'}), 409

    new_member = Member(handle=payload['username'], email_address=payload['email'])
    new_member.set_password(payload['password'])
    db.session.add(new_member)
    db.session.commit()

    session['user_id'] = new_member.id
    return jsonify({'message': 'Registration successful', 'user': new_member.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def handle_login():
    payload = request.get_json()
    active_member = Member.query.filter_by(email_address=payload.get('email')).first()

    if not active_member or not active_member.check_password(payload.get('password', '')):
        return jsonify({'error': 'Invalid credentials provided'}), 401

    session['user_id'] = active_member.id
    return jsonify({
        'message': 'Login successful',
        'user': active_member.to_dict(),
        'has_profile': active_member.member_info is not None
    }), 200

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def handle_logout():
    session.clear()
    return jsonify({'message': 'Successfully logged out'}), 200

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    active_member = Member.query.get(session['user_id'])
    return jsonify({
        'user': active_member.to_dict(),
        'has_profile': active_member.member_info is not None,
        'profile': active_member.member_info.to_dict() if active_member.member_info else None
    }), 200

# ─── Profiles ─────────────────────────────────────────────────────────────────

@app.route('/api/profiles', methods=['POST'])
@require_auth
def setup_profile():
    active_member = Member.query.get(session['user_id'])

    if active_member.member_info:
        return jsonify({'error': 'User detail record already exists'}), 409

    payload = request.form
    mandatory = ['name', 'age']
    for req in mandatory:
        if not payload.get(req):
            return jsonify({'error': f'Field {req} is mandatory'}), 400

    new_detail = UserDetail(
        member_id=active_member.id,
        full_name=payload.get('name'),
        years_old=int(payload.get('age')),
        about_me=payload.get('bio'),
        city_area=payload.get('location'),
        home_parish=payload.get('parish'),
        sex=payload.get('gender'),
        seeking=payload.get('looking_for', 'any'),
        job_title=payload.get('occupation'),
        connection_goal=payload.get('relationship_type'),
        visibility_status=payload.get('is_public', 'true').lower() == 'true'
    )

    if 'profile_photo' in request.files:
        uploaded = request.files['profile_photo']
        if uploaded and is_valid_file(uploaded.filename):
            import uuid
            extension = uploaded.filename.rsplit('.', 1)[1].lower()
            secure_name = f"{uuid.uuid4().hex}.{extension}"
            target_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(target_dir, exist_ok=True)
            uploaded.save(os.path.join(target_dir, secure_name))
            new_detail.display_picture = secure_name

    raw_tags = payload.get('interests', '')
    if raw_tags:
        tag_list = [t.strip() for t in raw_tags.split(',') if t.strip()]
        for t_name in tag_list:
            new_detail.tags.append(fetch_or_build_tag(t_name))

    db.session.add(new_detail)
    db.session.commit()
    return jsonify({'message': 'Details saved successfully', 'profile': new_detail.to_dict()}), 201

@app.route('/api/profiles/<int:target_id>', methods=['GET'])
@require_auth
def fetch_profile(target_id):
    target_member = Member.query.get_or_404(target_id)
    if not target_member.member_info:
        return jsonify({'error': 'Detail record not found'}), 404
    if not target_member.member_info.visibility_status and target_id != session['user_id']:
        return jsonify({'error': 'This profile is currently private'}), 403
    return jsonify({'profile': target_member.member_info.to_dict()}), 200

@app.route('/api/profiles/<int:target_id>', methods=['PUT'])
@require_auth
def modify_profile(target_id):
    if target_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403

    target_member = Member.query.get_or_404(target_id)
    if not target_member.member_info:
        return jsonify({'error': 'Detail record not found'}), 404

    detail_record = target_member.member_info
    payload = request.form

    attributes_map = {
        'name': 'full_name', 'age': 'years_old', 'bio': 'about_me',
        'location': 'city_area', 'parish': 'home_parish', 'gender': 'sex',
        'looking_for': 'seeking', 'occupation': 'job_title', 'relationship_type': 'connection_goal'
    }
    
    for req_key, db_key in attributes_map.items():
        if payload.get(req_key) is not None:
            val = payload.get(req_key)
            setattr(detail_record, db_key, int(val) if db_key == 'years_old' else val)

    if payload.get('is_public') is not None:
        detail_record.visibility_status = payload.get('is_public').lower() == 'true'

    if 'profile_photo' in request.files:
        uploaded = request.files['profile_photo']
        if uploaded and is_valid_file(uploaded.filename):
            import uuid
            extension = uploaded.filename.rsplit('.', 1)[1].lower()
            secure_name = f"{uuid.uuid4().hex}.{extension}"
            target_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(target_dir, exist_ok=True)
            uploaded.save(os.path.join(target_dir, secure_name))
            detail_record.display_picture = secure_name

    if payload.get('interests') is not None:
        detail_record.tags = []
        tag_list = [t.strip() for t in payload.get('interests').split(',') if t.strip()]
        for t_name in tag_list:
            detail_record.tags.append(fetch_or_build_tag(t_name))

    db.session.commit()
    return jsonify({'message': 'Detail record updated', 'profile': detail_record.to_dict()}), 200

@app.route('/api/uploads/<filename>', methods=['GET'])
def retrieve_media(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ─── Browse & Matching ────────────────────────────────────────────────────────

@app.route('/api/browse', methods=['GET'])
@require_auth
def discover_users():
    active_member = Member.query.get(session['user_id'])
    if not active_member.member_info:
        return jsonify({'error': 'Please complete your detail record first'}), 400

    base_info = active_member.member_info

    processed_ids = {s.target_id for s in active_member.given_swipes}
    processed_ids.add(active_member.id) 

    search_query = UserDetail.query.join(Member).filter(
        UserDetail.member_id.notin_(processed_ids),
        UserDetail.visibility_status == True
    )

    if base_info.seeking and base_info.seeking != 'any':
        search_query = search_query.filter(UserDetail.sex == base_info.seeking)

    area_filter = request.args.get('location')
    min_years = request.args.get('age_min', type=int)
    max_years = request.args.get('age_max', type=int)
    tag_filter = request.args.get('interests')

    if area_filter:
        search_query = search_query.filter(UserDetail.city_area.ilike(f'%{area_filter}%'))
    if min_years:
        search_query = search_query.filter(UserDetail.years_old >= min_years)
    if max_years:
        search_query = search_query.filter(UserDetail.years_old <= max_years)

    candidate_records = search_query.order_by(UserDetail.setup_date.desc()).all()

    if tag_filter:
        required_tags = {t.strip().lower() for t in tag_filter.split(',')}
        candidate_records = [c for c in candidate_records if required_tags & {t.label for t in c.tags}]

    output_list = []
    for candidate in candidate_records:
        candidate_data = candidate.to_dict()
        candidate_data['match_score'] = calculate_compatibility(base_info, candidate)
        output_list.append(candidate_data)

    output_list.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify({'profiles': output_list}), 200

@app.route('/api/like/<int:target_id>', methods=['POST'])
@require_auth
def register_like(target_id):
    active_id = session['user_id']

    if active_id == target_id:
        return jsonify({'error': 'Invalid action'}), 400

    target_member = Member.query.get_or_404(target_id)

    prior_action = SwipeAction.query.filter_by(actor_id=active_id, target_id=target_id).first()
    if prior_action:
        return jsonify({'error': 'Action already recorded'}), 409

    new_action = SwipeAction(actor_id=active_id, target_id=target_id)
    db.session.add(new_action)

    reciprocal = SwipeAction.query.filter_by(actor_id=target_id, target_id=active_id).first()
    connection_formed = False
    
    if reciprocal:
        id_a, id_b = sorted([active_id, target_id])
        prior_connection = Connection.query.filter_by(peer_a_id=id_a, peer_b_id=id_b).first()
        if not prior_connection:
            new_connection = Connection(peer_a_id=id_a, peer_b_id=id_b)
            db.session.add(new_connection)
        connection_formed = True

    db.session.commit()
    return jsonify({'message': 'Interest registered', 'is_match': connection_formed}), 201

@app.route('/api/pass/<int:target_id>', methods=['POST'])
@require_auth
def register_pass(target_id):
    active_id = session['user_id']
    prior_action = SwipeAction.query.filter_by(actor_id=active_id, target_id=target_id).first()
    if not prior_action:
        new_action = SwipeAction(actor_id=active_id, target_id=target_id)
        db.session.add(new_action)
        db.session.commit()
    return jsonify({'message': 'Candidate bypassed'}), 200

@app.route('/api/matches', methods=['GET'])
@require_auth
def fetch_connections():
    active_id = session['user_id']
    active_connections = Connection.query.filter(
        (Connection.peer_a_id == active_id) | (Connection.peer_b_id == active_id)
    ).order_by(Connection.formed_at.desc()).all()

    output_list = []
    for conn in active_connections:
        peer_id = conn.peer_b_id if conn.peer_a_id == active_id else conn.peer_a_id
        peer_member = Member.query.get(peer_id)
        if peer_member and peer_member.member_info:
            peer_data = peer_member.member_info.to_dict()
            peer_data['matched_at'] = conn.formed_at.isoformat()
            peer_data['match_id'] = conn.id
            output_list.append(peer_data)

    return jsonify({'matches': output_list, 'count': len(output_list)}), 200

# ─── Messaging ────────────────────────────────────────────────────────────────

@app.route('/api/messages/<int:peer_id>', methods=['GET'])
@require_auth
def load_thread(peer_id):
    active_id = session['user_id']

    if not check_connection(active_id, peer_id):
        return jsonify({'error': 'Connection required for direct messaging'}), 403

    thread_messages = DirectMessage.query.filter(
        ((DirectMessage.author_id == active_id) & (DirectMessage.recipient_id == peer_id)) |
        ((DirectMessage.author_id == peer_id) & (DirectMessage.recipient_id == active_id))
    ).order_by(DirectMessage.dispatched_at.asc()).all()

    return jsonify({'messages': [m.to_dict() for m in thread_messages]}), 200

@app.route('/api/messages/<int:peer_id>', methods=['POST'])
@require_auth
def dispatch_message(peer_id):
    active_id = session['user_id']

    if not check_connection(active_id, peer_id):
        return jsonify({'error': 'Connection required for direct messaging'}), 403

    payload = request.get_json()
    text_body = payload.get('content', '').strip()
    if not text_body:
        return jsonify({'error': 'Content body required'}), 400

    new_msg = DirectMessage(author_id=active_id, recipient_id=peer_id, body_text=text_body)
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({'message': new_msg.to_dict()}), 201

@app.route('/api/conversations', methods=['GET'])
@require_auth
def fetch_inbox():
    active_id = session['user_id']

    active_connections = Connection.query.filter(
        (Connection.peer_a_id == active_id) | (Connection.peer_b_id == active_id)
    ).all()

    inbox_threads = []
    for conn in active_connections:
        peer_id = conn.peer_b_id if conn.peer_a_id == active_id else conn.peer_a_id
        peer_member = Member.query.get(peer_id)
        if not peer_member or not peer_member.member_info:
            continue

        latest_msg = DirectMessage.query.filter(
            ((DirectMessage.author_id == active_id) & (DirectMessage.recipient_id == peer_id)) |
            ((DirectMessage.author_id == peer_id) & (DirectMessage.recipient_id == active_id))
        ).order_by(DirectMessage.dispatched_at.desc()).first()

        inbox_threads.append({
            'user_id': peer_id,
            'name': peer_member.member_info.full_name,
            'profile_photo': f'/api/uploads/{peer_member.member_info.display_picture}' if peer_member.member_info.display_picture else None,
            'last_message': latest_msg.to_dict() if latest_msg else None
        })

    return jsonify({'conversations': inbox_threads}), 200

# ─── Search ───────────────────────────────────────────────────────────────────

@app.route('/api/search', methods=['GET'])
@require_auth
def perform_search():
    area_filter = request.args.get('location')
    min_years = request.args.get('age_min', type=int)
    max_years = request.args.get('age_max', type=int)
    tag_filter = request.args.get('interests')
    ordering = request.args.get('sort', 'newest')  

    active_id = session['user_id']
    search_query = UserDetail.query.filter(
        UserDetail.member_id != active_id,
        UserDetail.visibility_status == True
    )

    if area_filter:
        search_query = search_query.filter(UserDetail.city_area.ilike(f'%{area_filter}%'))
    if min_years:
        search_query = search_query.filter(UserDetail.years_old >= min_years)
    if max_years:
        search_query = search_query.filter(UserDetail.years_old <= max_years)

    if ordering == 'newest':
        search_query = search_query.order_by(UserDetail.setup_date.desc())

    candidate_records = search_query.all()

    if tag_filter:
        required_tags = {t.strip().lower() for t in tag_filter.split(',')}
        candidate_records = [c for c in candidate_records if required_tags & {t.label for t in c.tags}]

    base_info = Member.query.get(active_id).member_info
    output_list = []
    for candidate in candidate_records:
        candidate_data = candidate.to_dict()
        if base_info:
            candidate_data['match_score'] = calculate_compatibility(base_info, candidate)
        output_list.append(candidate_data)

    if ordering == 'score' and base_info:
        output_list.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    return jsonify({'results': output_list, 'count': len(output_list)}), 200

# ─── Favourites ───────────────────────────────────────────────────────────────

@app.route('/api/favourites/<int:target_id>', methods=['POST'])
@require_auth
def bookmark_user(target_id):
    active_id = session['user_id']
    prior_bookmark = SavedProfile.query.filter_by(owner_id=active_id, bookmarked_member_id=target_id).first()
    if prior_bookmark:
        return jsonify({'error': 'User already bookmarked'}), 409
    new_bookmark = SavedProfile(owner_id=active_id, bookmarked_member_id=target_id)
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({'message': 'Added to bookmarks'}), 201

@app.route('/api/favourites/<int:target_id>', methods=['DELETE'])
@require_auth
def drop_bookmark(target_id):
    active_id = session['user_id']
    target_bookmark = SavedProfile.query.filter_by(owner_id=active_id, bookmarked_member_id=target_id).first()
    if target_bookmark:
        db.session.delete(target_bookmark)
        db.session.commit()
    return jsonify({'message': 'Removed from bookmarks'}), 200

@app.route('/api/favourites', methods=['GET'])
@require_auth
def list_bookmarks():
    active_id = session['user_id']
    active_bookmarks = SavedProfile.query.filter_by(owner_id=active_id).all()
    output_list = []
    for b in active_bookmarks:
        peer = Member.query.get(b.bookmarked_member_id)
        if peer and peer.member_info:
            output_list.append(peer.member_info.to_dict())
    return jsonify({'favourites': output_list}), 200

# ─── Moderation (Optional Feature) ──────────────────────────────────────────

@app.route('/api/report/<int:target_id>', methods=['POST'])
@require_auth
def report_user(target_id):
    """Handles reporting of a user for moderation."""
    # Since we don't have a full moderation system, we just acknowledge the report
    # and in a real app, this would flag an admin dashboard. 
    return jsonify({'message': 'Report submitted successfully. Our team will review this user.'}), 201

# ─── Misc ─────────────────────────────────────────────────────────────────────

@app.route('/')
def system_check():
    return jsonify(message="DriftDater API System is online")

def compile_form_errors(form):
    messages = []
    for field_name, err_list in form.errors.items():
        for err in err_list:
            messages.append(f"Error in {getattr(form, field_name).label.text}: {err}")
    return messages

@app.after_request
def set_headers(res):
    res.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    res.headers['Cache-Control'] = 'public, max-age=0'
    return res

@app.errorhandler(404)
def handle_404(error):
    return jsonify({'error': 'Resource unavailable'}), 404