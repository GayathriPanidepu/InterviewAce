document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const fileInput = document.getElementById('resume');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    // Display filename when file is selected
    fileInput.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name || 'No file selected';
        fileNameDisplay.textContent = `Selected file: ${fileName}`;
    });

    // Form validation
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let isValid = true;

        // Reset errors
        document.querySelectorAll('.error').forEach(error => error.style.display = 'none');

        // Validate username
        const username = document.getElementById('username').value;
        if (username.length < 3) {
            document.getElementById('usernameError').style.display = 'block';
            isValid = false;
        }

        // Validate email
        const email = document.getElementById('email').value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('emailError').style.display = 'block';
            isValid = false;
        }

        // Validate password
        const password = document.getElementById('password').value;
        if (password.length < 8) {
            document.getElementById('passwordError').style.display = 'block';
            isValid = false;
        }

        // Validate confirm password
        const confirmPassword = document.getElementById('confirmPassword').value;
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').style.display = 'block';
            isValid = false;
        }

        // Validate resume file
        const file = fileInput.files[0];
        if (file && !file.name.toLowerCase().endsWith('.pdf')) {
            document.getElementById('resumeError').style.display = 'block';
            isValid = false;
        }

        // If all validations pass
        if (isValid) {
            const successMessage = document.getElementById('successMessage');
            successMessage.style.display = 'block';
            form.reset();
            fileNameDisplay.textContent = '';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 3000);
        }
    });

    // Add event listeners for toggling password visibility
    document.getElementById("togglePassword").addEventListener("click", function() {
        const passwordInput = document.getElementById("password");
        const type = passwordInput.type === "password" ? "text" : "password";
        passwordInput.type = type;
        this.textContent = type === "password" ? "👁️" : "🙈"; // Change the icon
    });

    document.getElementById("toggleConfirmPassword").addEventListener("click", function() {
        const confirmPasswordInput = document.getElementById("confirmPassword");
        const type = confirmPasswordInput.type === "password" ? "text" : "password";
        confirmPasswordInput.type = type;
        this.textContent = type === "password" ? "👁️" : "🙈"; // Change the icon
    });
});
