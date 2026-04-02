-- Admin User 
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-442b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$Z92sf5f1ADiGD./wORaHCu9I/iqHNKtEsNYvGD.Damc7qUGvaklt.', TRUE);

-- Amenities
INSERT INTO Amenity (id, name) VALUES ('788e25d2-36c5-4d2c-9a1b-123456789abc', 'WiFi');
INSERT INTO Amenity (id, name) VALUES ('92a2b3c4-d5e6-4f7g-8h9i-0j1k2l3m4n5o', 'Swimming Pool');
INSERT INTO Amenity (id, name) VALUES ('f47ac10b-58cc-4372-a567-0e02b2c3d479', 'Air Conditioning');
