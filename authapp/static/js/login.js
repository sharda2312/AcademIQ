function togglePassword() {
    let passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// Get CSRF token using the Django-recommended approach
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}

// Show loading spinner and hide it when done
function showLoading() {
    document.getElementById("loginForm").classList.add("form-dimmed");
    document.getElementById("spinnerContainer").style.display = "block";
    document.getElementById("loginButton").disabled = true;
}

function hideLoading() {
    document.getElementById("loginForm").classList.remove("form-dimmed");
    document.getElementById("spinnerContainer").style.display = "none";
    document.getElementById("loginButton").disabled = false;
}

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let responseMessage = document.getElementById("responseMessage");

    if (!email || !password) {
        responseMessage.textContent = "All fields are required!";
        responseMessage.style.color = "red";
        return;
    }
    
    // Show loading spinner
    showLoading();

    fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCsrfToken()
        },
        body: new URLSearchParams(new FormData(this)),
        credentials: 'same-origin' // Important for CSRF handling
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 403) {
                throw new Error("CSRF verification failed. Please refresh the page and try again.");
            }
            throw new Error("Server error: " + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Hide loading spinner
        hideLoading();
        
        responseMessage.textContent = data.message;
        responseMessage.style.color = data.status === "success" ? "green" : "red";

        if (data.status === "success") {
            responseMessage.textContent = "Login successful! Redirecting...";
            window.location.href = data.redirect_url; // Redirect after successful login
        }
    })
    .catch(error => {
        // Hide loading spinner even on error
        hideLoading();
        
        responseMessage.textContent = error.message || "Login failed. Please try again.";
        responseMessage.style.color = "red";
        console.error("Login error:", error);
    });
});