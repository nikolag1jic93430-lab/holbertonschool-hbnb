from app import db
from app.models.base import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, price, latitude, longitude, description=None, **kwargs):
        super().__init__(**kwargs)
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coords(latitude, longitude)
        
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.description = description

    def validate_title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and max 100 characters.")

    def validate_price(self, value):
        if value is None or value <= 0:
            raise ValueError("Price must be a positive value.")

    def validate_coords(self, lat, lon):
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
