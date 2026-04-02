function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
    }
    return token;
}

async function submitReview(token, placeId, rating, comment) {
    const apiReviewUrl = `http://127.0.0.1:5000/places/${placeId}/reviews`;
    try {
        const response = await fetch(apiReviewUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: parseInt(rating),
                comment: comment
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert(`Failed to submit review: ${errorData.message || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred. Please try again.');
    }
}

async function fetchPlaces(token) {
    const apiPlacesUrl = 'http://127.0.0.1:5000/places';
    try {
        const response = await fetch(apiPlacesUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            window.allPlaces = places;
            displayPlaces(places);
        } else {
            console.error('Error fetching places');
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p><strong>Price:</strong> $${place.price_per_night} / night</p>
            <p><strong>Location:</strong> ${place.city_name}, ${place.country_name}</p>
            <button onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function filterPlaces(countryName) {
    if (!window.allPlaces) return;
    
    if (countryName === "all" || countryName === "") {
        displayPlaces(window.allPlaces);
    } else {
        const filtered = window.allPlaces.filter(place => place.country_name === countryName);
        displayPlaces(filtered);
    }
}

async function fetchPlaceDetails(token, placeId) {
    const apiPlaceUrl = `http://127.0.0.1:5000/places/${placeId}`;
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(apiPlaceUrl, { method: 'GET', headers: headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);

            if (token) {
                const addReviewSection = document.getElementById('add-review');
                const addReviewLink = document.getElementById('add-review-link');
                if (addReviewSection && addReviewLink) {
                    addReviewSection.style.display = 'block';
                    addReviewLink.href = `add_review.html?id=${placeId}`;
                }
            }
        } else {
            console.error("Error fetching place details");
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function displayPlaceDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    if (detailsContainer) {
        detailsContainer.innerHTML = `
            <h1>${place.name}</h1>
            <p><strong>Price:</strong> $${place.price_per_night} / night</p>
            <p><strong>Location:</strong> ${place.city_name}, ${place.country_name}</p>
            <p><strong>Description:</strong> ${place.description}</p>
        `;
    }

    const reviewsContainer = document.getElementById('reviews-container');
    if (reviewsContainer) {
        reviewsContainer.innerHTML = '';
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                reviewsContainer.innerHTML += `<p><strong>Rating: ${review.rating}/5</strong> - ${review.comment}</p>`;
            });
        } else {
            reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if (path.includes('add_review.html')) {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();
        const reviewForm = document.getElementById('review-form');

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                
                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('review-text').value;

                if (!placeId) {
                    alert("Error: Place ID not found.");
                    return;
                }

                await submitReview(token, placeId, rating, comment);
            });
        }
    }

    if (path.includes('login.html')) {
        const loginForm = document.getElementById('login-form');

        if (loginForm) {
            loginForm.addEventListener('submit', async (event) => {
                event.preventDefault(); 
                
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const apiLoginUrl = 'http://127.0.0.1:5000/login'; 

                try {
                    const response = await fetch(apiLoginUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email: email, password: password })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        const token = data.access_token || data.token; 

                        if (token) {
                            document.cookie = `token=${token}; path=/; max-age=86400`;
                            window.location.href = 'index.html';
                        } else {
                            alert("No token received from backend.");
                        }
                    } else {
                        alert('Invalid email or password.');
                    }
                } catch (error) {
                    console.error('Login error:', error);
                    alert('Could not connect to server.');
                }
            });
        }
    }

    if (path.includes('place.html')) {
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            alert("Error: Place ID not found.");
            window.location.href = 'index.html';
            return;
        }
        
        const token = getCookie('token');
        fetchPlaceDetails(token, placeId);
    }

    if (path === '/' || path.includes('index.html')) {
        const token = checkAuthentication();
        if (!token) return;

        fetchPlaces(token);

        const countryFilter = document.getElementById('country-filter');
        if (countryFilter) {
            countryFilter.addEventListener('change', (event) => {
                filterPlaces(event.target.value);
            });
        }
    }
});