# HBnB Evolution API (Part 2)

This project is a simplified backend for an AirBnB-like application, built with Python, Flask, and Flask-RESTx. It follows a modular layered architecture and utilizes the Facade design pattern to manage communication between layers.

## Architecture

The application is built using a strict layered architecture:
1. **Presentation Layer (API)**: Handled by Flask-RESTx, exposing RESTful endpoints.
2. **Business Logic Layer**: Contains the core Python models (`User`, `Place`, `Review`, `Amenity`) and strict data validation using `@property` decorators.
3. **Persistence Layer**: Currently implemented as an In-Memory Repository, storing data in Python dictionaries for rapid development and testing.
4. **Facade Pattern**: The `HBnBFacade` acts as the single entry point between the API and the Business Logic/Persistence layers, abstracting the complexity of data manipulation and relationships.

## Installation and Execution

1. Create a virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate` (Mac/Linux) or `.\venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python3 run.py`

Access the Swagger UI documentation at: `http://127.0.0.1:5000/api/v1/`

## Business Logic Layer

The `app/models/` directory contains the core domain entities:
- **BaseModel**: Handles UUID generation and audit timestamps (`created_at`, `updated_at`).
- **User**: Manages user profiles and authentication data.
- **Place**: Represents rental properties, validating geographical coordinates and prices.
- **Review**: Captures user feedback for a specific place.
- **Amenity**: Defines features associated with places (e.g., Wi-Fi).

All entities inherit from `BaseModel` and utilize Python `@property` decorators to enforce strict data validation before state changes.

## API Endpoints

The API is fully documented via Swagger. Below are the primary endpoints available in version 1.0:

* **Users**:
  * `POST /api/v1/users/` - Create a new user
  * `GET /api/v1/users/` - Retrieve all users
  * `GET /api/v1/users/<id>` - Retrieve a user by ID
  * `PUT /api/v1/users/<id>` - Update a user
* **Amenities**:
  * `POST /api/v1/amenities/` - Create an amenity
  * `GET /api/v1/amenities/` - Retrieve all amenities
  * `GET /api/v1/amenities/<id>` - Retrieve an amenity by ID
  * `PUT /api/v1/amenities/<id>` - Update an amenity
* **Places**:
  * `POST /api/v1/places/` - Create a place (requires valid owner_id)
  * `GET /api/v1/places/` - Retrieve all places
  * `GET /api/v1/places/<id>` - Retrieve a place by ID (includes owner and amenities details)
  * `PUT /api/v1/places/<id>` - Update a place
  * `GET /api/v1/places/<id>/reviews` - Retrieve all reviews for a specific place
* **Reviews**:
  * `POST /api/v1/reviews/` - Create a review (requires valid user_id and place_id)
  * `GET /api/v1/reviews/` - Retrieve all reviews
  * `GET /api/v1/reviews/<id>` - Retrieve a review by ID
  * `PUT /api/v1/reviews/<id>` - Update a review
  * `DELETE /api/v1/reviews/<id>` - Delete a review

---

## Testing Report

This section documents the black-box testing performed on the API endpoints using `cURL`, covering both successful operations and error handling. Automated unit tests are also provided in the `tests/` directory using Python's `unittest` framework.

### 1. User Endpoints

**Test: Create a User (Success)**
* **Command:** `curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'`
* **Expected Output:** `201 Created` with user JSON object.
* **Result:** Passed.

**Test: Create a User (Invalid Email)**
* **Command:** `curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "invalid-format"}'`
* **Expected Output:** `400 Bad Request` with error message.
* **Result:** Passed. Validation logic correctly caught the format error.

### 2. Place Endpoints (Boundary Testing)

**Test: Create a Place (Invalid Price - Negative)**
* **Command:** `curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Test Place", "description": "A place", "price": -50.0, "latitude": 30.0, "longitude": 40.0, "owner_id": "VALID_ID", "amenities": []}'`
* **Expected Output:** `400 Bad Request`.
* **Result:** Passed. Model validation rejected the negative price.

**Test: Create a Place (Out of range Latitude)**
* **Command:** `curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Test Place", "description": "A place", "price": 100.0, "latitude": 150.0, "longitude": 40.0, "owner_id": "VALID_ID", "amenities": []}'`
* **Expected Output:** `400 Bad Request`.
* **Result:** Passed. The system correctly enforced the -90.0 to 90.0 latitude boundary constraint.

### 3. Error Handling

**Test: Retrieve a Non-Existent Resource**
* **Command:** `curl -X GET "http://127.0.0.1:5000/api/v1/users/fake-uuid-1234"`
* **Expected Output:** `404 Not Found`.
* **Result:** Passed. The Facade correctly returned None, triggering the 404 response.