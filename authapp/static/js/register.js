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

        console.log("Checking email:", email);

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
            console.log("Email check response:", data);
            emailMsg.textContent = data.message;
            emailMsg.style.color = data.status === "error" ? "red" : "green";
        })
        .catch(error => {
            console.error("Email check error:", error);
        });
    });

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form from reloading the page

        const first_name = document.getElementById("first_name").value.trim();
        const last_name = document.getElementById("last_name").value.trim();
        const email = emailInput.value.trim();
        const password = document.getElementById("password").value;
        const dob = document.getElementById("dob").value;

        if (!first_name || !last_name || !email || !password || !dob) {
            responseMessage.textContent = "All fields are required!";
            responseMessage.style.color = "red";
            return;
        }

        console.log("Submitting form with data:", { first_name, last_name, email, password, dob });

        fetch("/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ first_name, last_name, email, password, dob })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Registration response:", data);
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