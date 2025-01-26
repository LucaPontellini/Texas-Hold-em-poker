function showErrorMessage(message, redirectUrl) {
    document.getElementById('error-text').innerHTML = message;
    document.getElementById('error-message').style.display = 'block';
    setTimeout(function() {
        hideErrorMessage();
        window.location.href = redirectUrl;
    }, 5000); // Hide the message after 5 seconds and redirect
}

function hideErrorMessage() {
    document.getElementById('error-message').style.display = 'none';
}

// Show the error message if present
if (error_message) {
    showErrorMessage(error_message, redirect_url);
}