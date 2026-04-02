from app import db
from app.models.base import BaseModel

# Table d'association pour la relation Many-to-Many entre Place et Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('Amenity.id', ondelete='CASCADE'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    # Attributs principaux
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Clé étrangère vers l'utilisateur (propriétaire)
    owner_id = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)

    # Relations
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id, description=None, **kwargs):
        """Initialisation avec validation des données"""
        super().__init__(**kwargs)
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coords(latitude, longitude)
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def to_dict(self):
        """
        Transforme l'objet SQLAlchemy en dictionnaire JSON.
        C'est cette méthode qui permet au Frontend d'afficher les données.
        """
        return {
            'id': self.id,
            'title': self.title,  # Utilisé par scripts.js
            'description': self.description,
            'price': self.price,  # Utilisé par scripts.js
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Inclut les reviews si elles existent
            'reviews': [review.to_dict() for review in self.reviews] if self.reviews else [],
            # Inclut les noms des amenities
            'amenities': [amenity.name for amenity in self.amenities] if self.amenities else []
        }

    # --- MÉTHODES DE VALIDATION ---

    def validate_title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and must be max 100 characters.")

    def validate_price(self, value):
        if value is None or value <= 0:
            raise ValueError("Price must be a positive value.")

    def validate_coords(self, lat, lon):
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")