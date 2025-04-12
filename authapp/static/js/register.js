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
    const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

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
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            emailMsg.textContent = data.message;
            emailMsg.style.color = data.status === "error" ? "#ff6b6b" : "#51cf66";
        })
        .catch(error => {
            console.error("Email check error:", error);
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
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify(formData)
            });

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
            responseMessage.textContent = "An error occurred during registration. Please try again.";
            responseMessage.style.color = "#ff6b6b";
        } finally {
            hideLoading();
        }
    });
});