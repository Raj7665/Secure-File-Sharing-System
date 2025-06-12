// main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('main.js loaded successfully!');

    // Example: Add a subtle animation or interaction
    const messages = document.querySelectorAll('.flashes li');
    messages.forEach(message => {
        message.style.opacity = '1'; // Ensure visibility
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';
            // Remove the message after the transition to clean up the DOM
            setTimeout(() => message.remove(), 500);
        }, 5000); // Messages disappear after 5 seconds
    });

    // You can add more interactive elements here later
    // For example, dynamic form validation, AJAX calls, etc.
});
