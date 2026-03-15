from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

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

        # Log pour debug : affiche ce qu'on trouve en base dans ton terminal
        if user:
            print(f"Utilisateur trouvé : {user.email}")
            print(f"Mot de passe en base : {user.password}")
            print(f"Mot de passe envoyé : {data['password']}")
        else:
            print("Utilisateur non trouvé dans la base.")

        # Vérification en texte clair (temporaire pour test)
        if user and user.password == data['password']:
            access_token = create_access_token(identity={'email': user.email, 'is_admin': user.is_admin})
            return {'access_token': access_token}, 200
        
        return {'msg': 'Email ou mot de passe invalide'}, 401
