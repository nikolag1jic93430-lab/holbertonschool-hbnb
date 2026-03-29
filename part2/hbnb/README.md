```markdown
# 🏨 HBnB Backend - Phase 3: Persistence & Security

Welcome to the third iteration of the HBnB project. In this phase, our application graduates from a stateless, in-memory prototype to a fully persistent, secure, and production-ready RESTful API. We have integrated a relational database and a robust authentication system while maintaining our clean, three-tier architecture.

## 🚀 The Evolution: What's New?

This phase focuses on three major technical upgrades:

1. **Relational Data Storage (SQLAlchemy):** We completely replaced the temporary Python dictionaries with an SQLite database managed via SQLAlchemy. Data is now safely persisted across server restarts.
2. **Secure Passwords (Bcrypt):** Plain-text passwords are a thing of the past. Passwords are now mathematically hashed and salted before ever reaching the database.
3. **Stateless Authentication (JWT):** We introduced JSON Web Tokens to handle user sessions. Endpoints are now protected, ensuring users can only access what they are authorized to see.
4. **Role-Based Access Control & Ownership:** Built-in logic to separate regular users from Administrators, and strict rules ensuring users can only modify their own creations (Places/Reviews).

## 🏗️ System Architecture

Our application uses the **Facade Pattern** to completely isolate the API endpoints from the database logic. 

```text
[ Client (Swagger / cURL) ]
            │
            ▼ (HTTP Requests + JWT)
    [ API Presentation Layer ] ──────▶ [ Auth & RBAC Check ]
            │
            ▼
    [ Business Logic Facade ]  ──────▶ [ Bcrypt Hashing ]
            │
            ▼
   [ SQLAlchemy Repository ]
            │
            ▼
  [ SQLite Relational Database ]
```

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Framework:** Flask & Flask-RESTx
* **Database & ORM:** SQLite3, SQLAlchemy
* **Security:** Flask-JWT-Extended, Flask-Bcrypt

## 💻 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-link>
   cd hbnb/part3
   ```
2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the server:**
   ```bash
   python run.py
   ```
   *The Swagger UI is now available at `http://127.0.0.1:5000/api/v1/`.*

## 🔒 API Endpoints & Access Levels

Most endpoints now require an `Authorization: Bearer <token>` header. Here is a summary of the security rules implemented:

| Resource Area | Endpoint Example | Required Access Level | Description |
|---|---|---|---|
| **Authentication** | `POST /auth/login` | **Public** | Returns a JWT access token. |
| **Users** | `POST /users/` | **Public** | Account registration. |
| **Users** | `GET /users/` | **Admin Only** | Only admins can list all users. |
| **Places** | `POST /places/` | **Authenticated** | Any logged-in user can create a place. |
| **Places** | `PUT /places/<id>` | **Owner Only** | Must be the exact user who created the place. |
| **Amenities** | `POST /amenities/` | **Admin Only** | Only admins can manage the amenity catalog. |

## 🧠 Implementation Highlights

### 1. The ORM Mapping
Instead of manually writing SQL, we mapped our classes to database tables. For example, the `Place` model now defines its relationships natively:
* A `Place` belongs to one `User` (One-to-Many).
* A `Place` can have multiple `Amenities` (Many-to-Many).

### 2. Securing the Facade
Our `HBnBFacade` intercepts user creation to hash the password transparently:
```python
def create_user(self, user_data):
    # Passwords are hashed before database insertion
    if 'password' in user_data:
        user_data['password'] = generate_password_hash(user_data['password']).decode('utf-8')
    user = User(**user_data)
    return self.user_repo.add(user)
```

### 3. Protecting the Routes
Using decorators, we enforce security at the API layer before the Facade is even called:
```python
@jwt_required()
def put(self, place_id):
    current_user = get_jwt_identity()
    # Ownership logic here...
```

## 📚 Technical Glossary

* **JWT (JSON Web Token):** A secure, encoded string used to identify a logged-in user without the server needing to remember their session.
* **ORM (Object-Relational Mapper):** A tool (SQLAlchemy) that translates Python code into SQL queries automatically.
* **RBAC (Role-Based Access Control):** A security concept where access is granted based on the user's role (e.g., User vs Admin).
* **Salt & Hash (Bcrypt):** A cryptographic process that turns a password into an irreversible string, making data breaches harmless.
