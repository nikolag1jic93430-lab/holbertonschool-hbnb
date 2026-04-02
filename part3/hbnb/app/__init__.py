from flask import Flask, send_from_directory # <-- AJOUT : send_from_directory
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # <-- AJOUT : Importation de la bibliothèque CORS

# Initialisation des extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# Configuration de la sécurité pour Swagger
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Entrez votre jeton JWT de la manière suivante: Bearer <votre_token>'
    }
}

def create_app(config_class="config.DevelopmentConfig"):
    # <-- AJOUT : Configuration pour trouver le dossier static
    app = Flask(__name__, static_url_path='', static_folder='../static')
    app.config.from_object(config_class)

    # <-- AJOUT : Activation de CORS pour permettre au front-end de faire des requêtes vers l'API
    CORS(app)

    # Initialisation des applications avec l'instance Flask
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configuration de l'API avec les autorisations
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API with Auth and Database',
        doc='/api/v1/',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    # Importation des namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns  # Ajout de l'authentification

    # Ajout des namespaces à l'API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # --- AJOUT : Routes pour servir les fichiers frontend ---
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static_files(path):
        return send_from_directory(app.static_folder, path)

    return app