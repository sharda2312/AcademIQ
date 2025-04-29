document.addEventListener("DOMContentLoaded", function () {
    // Password toggle functionality
    window.togglePassword = function (fieldId) {
        const input = document.getElementById(fieldId);
        const toggleBtn = input.nextElementSibling;
        
        if (input.type === "password") {
            input.type = "text";
            toggleBtn.textContent = "🙈";
        } else {
            input.type = "password";
            toggleBtn.textContent = "👁️";
        }
    };

    // Loading state functions
    function showLoading() {
        document.getElementById("registerForm").classList.add("form-dimmed");
        document.getElementById("spinnerContainer").style.display = "flex";
        document.getElementById("registerButton").disabled = true;
    }

    function hideLoading() {
        document.getElementById("registerForm").classList.remove("form-dimmed");
        document.getElementById("spinnerContainer").style.display = "none";
        document.getElementById("registerButton").disabled = false;
    }

    // Form elements
    const form = document.getElementById("registerForm");
    const responseMessage = document.getElementById("responseMessage");
    const emailInput = document.getElementById("email");
    const emailMsg = document.getElementById("emailMsg");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    
    // Get CSRF token using the Django-recommended approach
    function getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

    // Real-time password match checking
    function checkPasswordMatch() {
        if (passwordInput.value && confirmPasswordInput.value && 
            passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.setCustomValidity("Passwords do not match");
        } else {
            confirmPasswordInput.setCustomValidity("");
        }
    }

    passwordInput.addEventListener("input", checkPasswordMatch);
    confirmPasswordInput.addEventListener("input", checkPasswordMatch);

    // Email availability check
    emailInput.addEventListener("blur", function () {
        const email = emailInput.value.trim();
        if (email === "") return;

        fetch("/check-email/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()
            },
            body: JSON.stringify({ email }),
            credentials: 'same-origin' // Important for CSRF token to be sent with request
        })
        .then(response => {
            // Check if response is ok before processing JSON
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            emailMsg.textContent = data.message;
            emailMsg.style.color = data.status === "error" ? "#ff6b6b" : "#51cf66";
        })
        .catch(error => {
            console.error("Email check error:", error);
            emailMsg.textContent = "Error checking email availability. Please try again.";
            emailMsg.style.color = "#ff6b6b";
        });
    });

    // Form submission
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Get form values
        const formData = {
            first_name: document.getElementById("first_name").value.trim(),
            last_name: document.getElementById("last_name").value.trim(),
            email: emailInput.value.trim(),
            password: passwordInput.value,
            dob: document.getElementById("dob").value
        };

        // Validate required fields
        if (!Object.values(formData).every(Boolean)) {
            responseMessage.textContent = "All fields are required!";
            responseMessage.style.color = "#ff6b6b";
            return;
        }

        // Validate password match
        if (formData.password !== confirmPasswordInput.value) {
            responseMessage.textContent = "Passwords do not match!";
            responseMessage.style.color = "#ff6b6b";
            return;
        }

        showLoading();

        try {
            const response = await fetch("/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken()
                },
                body: JSON.stringify(formData),
                credentials: 'same-origin' // Important for CSRF handling
            });

            // Add explicit check for response status
            if (!response.ok) {
                // Check specifically for CSRF errors
                if (response.status === 403) {
                    throw new Error("CSRF verification failed. Please refresh the page and try again.");
                }
                throw new Error("Server error: " + response.status);
            }

            const data = await response.json();

            responseMessage.textContent = data.message;
            responseMessage.style.color = data.status === "success" ? "#51cf66" : "#ff6b6b";

            if (data.status === "success") {
                form.reset();
                emailMsg.textContent = "";

                // Redirect to the login page after successful registration
                setTimeout(() => {
                    window.location.href = "/login/";
                }, 2000);
            }
        } catch (error) {
            console.error("Registration error:", error);
            responseMessage.textContent = error.message || "An error occurred during registration. Please try again.";
            responseMessage.style.color = "#ff6b6b";
        } finally {
            hideLoading();
        }
    });
});