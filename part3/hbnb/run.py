from app import create_app, db
# On importe les modèles ici pour que SQLAlchemy les connaisse
from app.models.user import User 
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Force la création des tables dans le fichier .db
        db.create_all()
        print("Tables créées :", db.metadata.tables.keys())
    
    app.run(debug=True)