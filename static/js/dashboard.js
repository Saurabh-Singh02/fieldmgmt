// Function to handle button clicks
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JavaScript loaded');
    
    // Check In button functionality
    const checkInBtn = document.querySelector('.check-in-btn');
    if (checkInBtn) {
        checkInBtn.addEventListener('click', function() {
            alert('Check-in functionality would be implemented here with geolocation API');
            this.innerHTML = '<i class="fas fa-check-circle"></i> Checked In';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-success');
        });
    }
    
    // Availability toggle button
    const availabilityBtn = document.querySelector('.availability-btn');
    if (availabilityBtn) {
        // Set initial state
        const isAvailable = availabilityBtn.dataset.available === 'true';
        updateAvailabilityButton(availabilityBtn, isAvailable);
        
        availabilityBtn.addEventListener('click', function() {
            const newAvailability = !(this.dataset.available === 'true');
            
            // Simulate API call
            setTimeout(() => {
                updateAvailabilityButton(this, newAvailability);
                alert('Availability updated to: ' + (newAvailability ? 'Available' : 'Not Available'));
            }, 300);
        });
    }
    
    // Voice Notes button functionality
    const voiceNotesBtn = document.querySelector('.voice-notes-btn');
    if (voiceNotesBtn) {
        voiceNotesBtn.addEventListener('click', function() {
            alert('Voice notes functionality would be implemented here with Web Speech API');
        });
    }
    
    // All other action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action || 'perform action';
            alert(`${action} functionality would be implemented here`);
        });
    });
    
    // Helper function to update availability button
    function updateAvailabilityButton(btn, isAvailable) {
        if (isAvailable) {
            btn.innerHTML = '<i class="fas fa-toggle-on"></i> Available';
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-success');
            btn.dataset.available = 'true';
        } else {
            btn.innerHTML = '<i class="fas fa-toggle-off"></i> Not Available';
            btn.classList.remove('btn-success');
            btn.classList.add('btn-secondary');
            btn.dataset.available = 'false';
        }
    }
});

// CSRF token functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Set up AJAX CSRF token
const csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});