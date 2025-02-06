document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const responseMessage = document.getElementById("responseMessage");
    const emailInput = document.getElementById("email");
    const emailMsg = document.getElementById("emailMsg");

    // Get CSRF token from the hidden input field in the form
    const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

    // Function to check if the email already exists
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
            emailMsg.style.color = data.status === "error" ? "red" : "green";
        })
    });

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form from reloading the page

        const name = document.getElementById("name").value.trim();
        const email = emailInput.value.trim();
        const password = document.getElementById("password").value;
        const dob = document.getElementById("dob").value;

        if (!name || !email || !password || !dob) {
            responseMessage.textContent = "All fields are required!";
            responseMessage.style.color = "red";
            return;
        }

        fetch("/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ name, email, password, dob })
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.textContent = data.message;
            responseMessage.style.color = data.status === "success" ? "green" : "red";

            if (data.status === "success") {
                form.reset(); // Clear form fields after successful registration
                emailMsg.textContent = ""; // Clear email availability message
            }
        })
        .catch(error => {
            responseMessage.textContent = "Error registering user.";
            responseMessage.style.color = "red";
            console.error("Registration error:", error);
        });
    });
});
