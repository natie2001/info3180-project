# ❤️ DriftDater

> **INFO3180 — Group 24** | A full-stack dating web application built with Vue 3 and Flask — developed at UWI Mona.

DriftDater allows users to register, create detailed profiles with photo uploads, and discover potential matches based on a compatibility algorithm. Users can like or pass on profiles, view mutual matches, and send messages to their connections.

---

## 👥 Team Members & Roles

| Name | Role | Responsibilities |
|------|------|-----------------|
| **Nathan Hansle** | Project Manager, Backend Lead, Deployment Lead | Flask REST API, database schema (SQLAlchemy), authentication logic, server deployment |
| **Shevar Roulston** | Frontend Lead, QA/Testing Lead | Vue 3 component architecture, UI/UX design, state management, feature validation |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (or SQLite for local dev)

---

### 🐍 Backend Setup

1. Navigate to the project root directory

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your `.env` file (see [Configuration](#-configuration) below)

5. Run database migrations:
   ```bash
   flask db init
   flask db migrate -m "initial"
   flask db upgrade
   ```

6. Start the Flask server:
   ```bash
   flask run --port=8080
   ```
   The API will be available at `http://localhost:8080`

---

### 🖥️ Frontend Setup

1. From the project root (where `package.json` is located), install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

---

## 🔐 Configuration

Create a `.env` file in the project root. This file is excluded from version control for security. 

```env
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8080
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost/driftdater
UPLOAD_FOLDER=app/static/uploads
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Register a new account |
| `POST` | `/api/auth/login` | Authenticate and start a session |
| `POST` | `/api/auth/logout` | End the current session |
| `GET` | `/api/auth/me` | Return current user's account and profile data |

### Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/profiles` | Create a new profile (multipart form data for photo) |
| `GET` | `/api/profiles/<user_id>` | View a specific user's profile |
| `PUT` | `/api/profiles/<user_id>` | Update your own profile |
| `GET` | `/api/uploads/<filename>` | Serve uploaded profile pictures |

### Matching & Discovery

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/browse` | Get potential matches via the compatibility algorithm |
| `POST` | `/api/like/<user_id>` | Like a user (auto-creates a match if mutual) |
| `POST` | `/api/pass/<user_id>` | Pass on a user profile |
| `GET` | `/api/matches` | List all mutual connections |

### Messaging

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/conversations` | List all active chat threads |
| `GET` | `/api/messages/<user_id>` | Retrieve message history with a match |
| `POST` | `/api/messages/<user_id>` | Send a message to a match |

### Search & Extras

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/search` | Filter users by age, location, and interests |
| `GET` | `/api/favourites` | List bookmarked profiles |
| `POST` | `/api/favourites/<user_id>` | Bookmark a profile |
| `DELETE` | `/api/favourites/<user_id>` | Remove a bookmarked profile |

---

## 🗄️ Database Schema

The application uses **6 normalized tables** (3NF):

- **users** — account credentials and metadata
- **profiles** — extended user profile info (bio, location, photo, etc.)
- **interests** — interest tags (many-to-many with profiles)
- **likes** — records of like/pass actions between users
- **matches** — confirmed mutual likes
- **messages** — chat messages between matched users
- **favourites** — bookmarked profiles

---


## ⚠️ Known Issues & Limitations

- The `app/static/uploads/` folder is tracked via `.gitkeep` — uploaded images are gitignored and will not persist across deployments
- If the browser blocks login/registration requests, ensure CORS is configured to allow credentials from `http://localhost:5173`
- An admin moderation UI page is not yet implemented; the report endpoint exists at the API level only

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Pinia State Management](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)

---

## 🎓 Acknowledgements

Built for the **INFO3180 — Web Application Development II** course at  
**The University of the West Indies, Mona**.
