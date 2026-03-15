import re
from app import db, bcrypt
from app.models.base import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'User'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='author', lazy=True, cascade="all, delete-orphan")

    def hash_password(self, password):
        """Hache le mot de passe."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie le mot de passe."""
        return bcrypt.check_password_hash(self.password, password)
