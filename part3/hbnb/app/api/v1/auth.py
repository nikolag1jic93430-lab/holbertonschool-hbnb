from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_bcrypt import check_password_hash

api = Namespace('auth', description='Opérations d\'authentification')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model)
    def post(self):
        """Authentifie un utilisateur et retourne un token JWT"""
        data = api.payload
        user = facade.get_user_by_email(data['email'])

        if user:
            print(f"DEBUG: Mot de passe en base -> {user.password}")
            is_valid = check_password_hash(user.password, data['password'])
            print(f"DEBUG: Comparaison Bcrypt -> {is_valid}")
        else:
            print("DEBUG: Utilisateur non trouvé dans la base")

        if user and check_password_hash(user.password, data['password']):
            
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={'is_admin': user.is_admin}
            )
            
            return {'access_token': access_token}, 200
        
        return {'msg': 'Email ou mot de passe invalide'}, 401
