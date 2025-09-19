// Function to handle button clicks and AJAX requests
document.addEventListener('DOMContentLoaded', function() {
    // Check In button functionality
    const checkInBtn = document.getElementById('checkInBtn');
    if (checkInBtn) {
        checkInBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;
                        
                        // Send location to server
                        fetch('/dashboard/api/check-in/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            body: `latitude=${latitude}&longitude=${longitude}`
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Check-in successful!');
                                this.innerHTML = '<i class="fas fa-check-circle"></i> Checked In';
                                this.classList.remove('btn-outline-primary');
                                this.classList.add('btn-success');
                                this.disabled = true;
                            } else {
                                alert('Check-in failed. Please try again.');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Check-in failed. Please try again.');
                        });
                    },
                    function(error) {
                        alert('Unable to get your location. Please enable location services.');
                        console.error('Geolocation error:', error);
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }
    
    // Update Availability button functionality
    const availabilityBtn = document.getElementById('availabilityBtn');
    if (availabilityBtn) {
        availabilityBtn.addEventListener('click', function() {
            const isAvailable = this.dataset.available === 'true';
            const newAvailability = !isAvailable;
            
            fetch('/dashboard/api/update-availability/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `available=${newAvailability}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.available) {
                        this.innerHTML = '<i class="fas fa-toggle-on"></i> Available';
                        this.classList.remove('btn-secondary');
                        this.classList.add('btn-success');
                        this.dataset.available = 'true';
                    } else {
                        this.innerHTML = '<i class="fas fa-toggle-off"></i> Not Available';
                        this.classList.remove('btn-success');
                        this.classList.add('btn-secondary');
                        this.dataset.available = 'false';
                    }
                } else {
                    alert('Failed to update availability. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to update availability. Please try again.');
            });
        });
    }
    
    // Voice Notes button functionality
    const voiceNotesBtn = document.getElementById('voiceNotesBtn');
    if (voiceNotesBtn && 'webkitSpeechRecognition' in window) {
        voiceNotesBtn.addEventListener('click', function() {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                voiceNotesBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
                voiceNotesBtn.classList.remove('btn-outline-primary');
                voiceNotesBtn.classList.add('btn-danger');
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                alert(`You said: ${transcript}\n\nThis would be saved to the current job.`);
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error', event.error);
                alert('Voice recognition failed. Please try again.');
            };
            
            recognition.onend = function() {
                voiceNotesBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Notes';
                voiceNotesBtn.classList.remove('btn-danger');
                voiceNotesBtn.classList.add('btn-outline-primary');
            };
            
            recognition.start();
        });
    } else if (voiceNotesBtn) {
        voiceNotesBtn.addEventListener('click', function() {
            alert('Voice recognition is not supported in your browser.');
        });
    }
    
    // Helper function to get CSRF token
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
});