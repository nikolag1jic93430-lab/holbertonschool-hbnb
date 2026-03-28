import unittest
import json
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository

class TestHBnBAPI(unittest.TestCase):
    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        facade.user_repo = InMemoryRepository()
        facade.place_repo = InMemoryRepository()
        facade.review_repo = InMemoryRepository()
        facade.amenity_repo = InMemoryRepository()

    def test_create_user_valid(self):
        """Test la création d'un utilisateur valide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        """Test la création d'un utilisateur avec un email invalide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test la création d'un lieu avec une latitude hors limite (Boundary Testing)"""
        owner_res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner", "last_name": "Test", "email": "owner@test.com"
        })
        owner_id = owner_res.json['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Mars Base",
            "description": "Une description",
            "price": 1000.0,
            "latitude": 150.0,
            "longitude": 0.0,
            "owner_id": owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()