from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_bcrypt import generate_password_hash

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # --- USER METHODS ---
    def create_user(self, user_data):
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password']).decode('utf-8')
            
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # --- AMENITY METHODS ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        return self
