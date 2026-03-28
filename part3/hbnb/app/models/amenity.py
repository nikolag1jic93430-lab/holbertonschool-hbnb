from app import db
from app.models.base import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'Amenity'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.validate_name(name)
        self.name = name

    def validate_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name is required and max 50 characters.")
