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

    # --- AMENITY METHODS ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    # --- PLACE METHODS ---
    def create_place(self, place_data):
        """
        Assure-toi que place_data contient 'title' et 'price' 
        pour correspondre au Frontend.
        """
        # Si ton modèle utilise 'name' mais le front envoie 'title', on corrige ici
       # if 'title' in place_data and 'name' not in place_data:
      #      place_data['name'] = place_data['title']
        
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # On met à jour via le repo
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if not place or not amenity:
            raise ValueError("Place or Amenity not found")
            
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self.place_repo.update(place.id, {}) # Déclenche la sauvegarde
        
        return place

    # --- REVIEW METHODS ---
    def create_review(self, review_data):
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()