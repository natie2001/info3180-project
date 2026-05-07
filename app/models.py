from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Many-to-many link: user_details <-> tags
detail_tags_link = db.Table('detail_tags_link',
    db.Column('detail_id', db.Integer, db.ForeignKey('user_details.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email_address = db.Column(db.String(120), unique=True, nullable=False, index=True)
    secret_key = db.Column(db.String(255), nullable=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships mapped to the new class names
    member_info = db.relationship('UserDetail', backref='account', uselist=False, cascade='all, delete-orphan')
    outbox = db.relationship('DirectMessage', foreign_keys='DirectMessage.author_id', backref='author', lazy='dynamic')
    inbox = db.relationship('DirectMessage', foreign_keys='DirectMessage.recipient_id', backref='recipient', lazy='dynamic')
    given_swipes = db.relationship('SwipeAction', foreign_keys='SwipeAction.actor_id', backref='actor', lazy='dynamic')
    received_swipes = db.relationship('SwipeAction', foreign_keys='SwipeAction.target_id', backref='target', lazy='dynamic')
    bookmarks = db.relationship('SavedProfile', foreign_keys='SavedProfile.owner_id', backref='owner', lazy='dynamic')

    def set_password(self, raw_password):
        self.secret_key = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.secret_key, raw_password)

    def to_dict(self):
        # Keys remain the same for frontend API compatibility
        return {
            'id': self.id,
            'username': self.handle,
            'email': self.email_address,
            'created_at': self.joined_on.isoformat()
        }

class UserDetail(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    years_old = db.Column(db.Integer, nullable=False, index=True)
    about_me = db.Column(db.Text)
    city_area = db.Column(db.String(100), index=True)   
    home_parish = db.Column(db.String(100))
    sex = db.Column(db.String(20))
    seeking = db.Column(db.String(20))              
    job_title = db.Column(db.String(100))              
    connection_goal = db.Column(db.String(50))        
    display_picture = db.Column(db.String(255))
    visibility_status = db.Column(db.Boolean, default=True)
    setup_date = db.Column(db.DateTime, default=datetime.utcnow)

    tags = db.relationship('Tag', secondary=detail_tags_link, backref='details', lazy='subquery')

    def to_dict(self, include_user=True):
        return {
            'id': self.id,
            'user_id': self.member_id,
            'name': self.full_name,
            'age': self.years_old,
            'bio': self.about_me,
            'location': self.city_area,
            'parish': self.home_parish,
            'gender': self.sex,
            'looking_for': self.seeking,
            'occupation': self.job_title,
            'relationship_type': self.connection_goal,
            'profile_photo': f'/api/uploads/{self.display_picture}' if self.display_picture else None,
            'is_public': self.visibility_status,
            'created_at': self.setup_date.isoformat(),
            'interests': [t.label for t in self.tags]
        }

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)

class SwipeAction(db.Model):
    __tablename__ = 'swipe_actions'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    target_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('actor_id', 'target_id', name='unique_swipe'),)

class Connection(db.Model):
    __tablename__ = 'connections'

    id = db.Column(db.Integer, primary_key=True)
    peer_a_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    peer_b_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    formed_at = db.Column(db.DateTime, default=datetime.utcnow)

    peer_a = db.relationship('Member', foreign_keys=[peer_a_id])
    peer_b = db.relationship('Member', foreign_keys=[peer_b_id])

    __table_args__ = (db.UniqueConstraint('peer_a_id', 'peer_b_id', name='unique_connection'),)

class DirectMessage(db.Model):
    __tablename__ = 'direct_messages'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    body_text = db.Column(db.Text, nullable=False)
    dispatched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.author_id,
            'receiver_id': self.recipient_id,
            'content': self.body_text,
            'created_at': self.dispatched_at.isoformat()
        }

class SavedProfile(db.Model):
    __tablename__ = 'saved_profiles'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    bookmarked_member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('owner_id', 'bookmarked_member_id', name='unique_bookmark'),) 