
function togglePassword() {
    let passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
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

    fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams(new FormData(this))
    })
    .then(response => response.json())
    .then(data => {
        responseMessage.textContent = data.message;
        responseMessage.style.color = data.status === "success" ? "green" : "red";


        if (data.status === "success") {
            window.location.href = data.redirect_url; // Redirect after successful login
        }
    })
    .catch(error => {
        responseMessage.textContent = "Login failed. Please try again.";
        responseMessage.style.color = "red";
        console.error("Login error:", error);
    });
});
    