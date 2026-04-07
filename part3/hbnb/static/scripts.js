// --- UTILITAIRES ---

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function logout() {
    // Supprime le cookie en le faisant expirer
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    alert("You have been logged out.");
    window.location.href = 'index.html';
}

function checkAuthentication(requireAuth = false, redirectUrl = 'index.html') {
    const token = getCookie('token');
    if (!token && requireAuth) {
        window.location.href = redirectUrl;
    }
    return token;
}

// --- APPELS API ---

async function submitReview(token, placeId, rating, comment) {
    const apiReviewUrl = `/api/v1/places/${placeId}/reviews`;
    try {
        const response = await fetch(apiReviewUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: parseInt(rating),
                text: comment // 'text' pour correspondre au Backend
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert(`Failed to submit review: ${errorData.error || errorData.message || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred. Please try again.');
    }
}

async function fetchPlaces(token) {
    const apiPlacesUrl = '/api/v1/places/';
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(apiPlacesUrl, { method: 'GET', headers: headers });

        if (response.ok) {
            const places = await response.json();
            window.allPlaces = places; // Sauvegarde pour le filtre local
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

async function fetchPlaceDetails(token, placeId) {
    const apiPlaceUrl = `/api/v1/places/${placeId}`;
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(apiPlaceUrl, { method: 'GET', headers: headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);

            const addReviewSection = document.getElementById('add-review');
            if (token && addReviewSection) {
                addReviewSection.style.display = 'block';
                const addReviewLink = document.getElementById('add-review-link');
                if (addReviewLink) addReviewLink.href = `add_review.html?id=${placeId}`;
            }
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// --- AFFICHAGE ---

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.title || "No Title"}</h3>
            <p><strong>Price:</strong> $${place.price || 0} / night</p>
            <p><strong>Location:</strong> ${place.city_name || "Paris"}, ${place.country_name || "France"}</p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function displayPlaceDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    if (detailsContainer) {
        // Préparation de la liste des amenities
        let amenitiesHTML = "None";
        if (place.amenities && place.amenities.length > 0) {
            amenitiesHTML = place.amenities.map(a => a.name || a).join(', ');
        }

        detailsContainer.innerHTML = `
            <h1>${place.title || "No Title"}</h1>
            <p><strong>Price:</strong> $${place.price || 0} / night</p>
            <p><strong>Location:</strong> ${place.city_name || "Paris"}, ${place.country_name || "France"}</p>
            <p><strong>Description:</strong> ${place.description || "No description available"}</p>
            <p><strong>Amenities:</strong> ${amenitiesHTML}</p>
        `;
    }

    const reviewsContainer = document.getElementById('reviews-container');
    if (reviewsContainer) {
        reviewsContainer.innerHTML = '';
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                reviewsContainer.innerHTML += `
                    <div class="review-card">
                        <p><strong>Rating: ${review.rating}/5</strong> - ${review.text || review.comment || "No comment"}</p>
                    </div>`;
            });
        } else {
            reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
        }
    }
}

// --- INITIALISATION ---

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const token = getCookie('token');

    // Gestion universelle Navbar (Login/Logout)
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    }

    // Page Add Review
    if (path.includes('add_review.html')) {
        checkAuthentication(true);
        const placeId = getPlaceIdFromURL();
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('review-text').value;
                await submitReview(token, placeId, rating, comment);
            });
        }
    }

    // Page Login
    if (path.includes('login.html')) {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                try {
                    const response = await fetch('/api/v1/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    if (response.ok) {
                        const data = await response.json();
                        document.cookie = `token=${data.access_token || data.token}; path=/; max-age=86400`;
                        window.location.href = 'index.html';
                    } else {
                        alert('Invalid credentials');
                    }
                } catch (err) { console.error(err); }
            });
        }
    }

    // Page Index & Place Details
    if (path.includes('place.html')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) fetchPlaceDetails(token, placeId);
    } else if (path === '/' || path.includes('index.html') || path === '') {
        fetchPlaces(token);

        // Filtre par prix
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const selectedPrice = event.target.value;
                
                if (!window.allPlaces) return; 

                if (selectedPrice === 'All') {
                    displayPlaces(window.allPlaces);
                } else {
                    const maxPrice = parseInt(selectedPrice, 10);
                    const filteredPlaces = window.allPlaces.filter(place => place.price <= maxPrice);
                    displayPlaces(filteredPlaces);
                }
            });
        }
    }
});