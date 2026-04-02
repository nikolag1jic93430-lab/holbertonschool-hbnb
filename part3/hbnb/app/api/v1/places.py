from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError

api = Namespace('places', description='Place operations')

@api.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return {'error': str(e)}, 401
    
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

# Modèle pour la validation des reviews
review_model = api.model('PlaceReview', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)')
})

@api.route('/')
class PlaceList(Resource):
    
    @api.expect(place_model, validate=False)
    @jwt_required() 
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'price': p.price
        } for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {'id': a.id, 'name': a.name} for a in place.amenities
            ],
            'reviews': [
                {
                    'id': r.id, 
                    'text': r.text, 
                    'rating': r.rating
                } for r in place.reviews
            ]
        }, 200

    @api.expect(place_model, validate=False)
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if str(place.owner.id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

# --- NOUVELLE SECTION POUR LES REVIEWS ---
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self, place_id):
        """Add a review to a specific place"""
        current_user_id = get_jwt_identity()
        review_data = api.payload

        # On vérifie si la place existe
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        try:
            # On ajoute les IDs nécessaires pour la facade
            review_data['user_id'] = current_user_id
            review_data['place_id'] = place_id
            
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenityLink(Resource):
    @jwt_required()
    def post(self, place_id, amenity_id):
        """Link an amenity to a place"""
        try:
            facade.add_amenity_to_place(place_id, amenity_id)
            return {'message': 'Amenity successfully linked to place'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400