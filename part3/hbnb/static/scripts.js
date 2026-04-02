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

function checkAuthenticationForReview() {
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

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('add_review.html')) {
        
        const token = checkAuthenticationForReview();
        const placeId = getPlaceIdFromURL();
        const reviewForm = document.getElementById('review-form');

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault(); // Empêche le rechargement classique de la page
                
                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('review-text').value;

                // Petite sécurité supplémentaire
                if (!placeId) {
                    alert("Erreur : Impossible de trouver l'ID du logement.");
                    return;
                }

                await submitReview(token, placeId, rating, comment);
            });
        }
    }
});