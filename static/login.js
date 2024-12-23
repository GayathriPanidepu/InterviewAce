document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

    // // Check if a user is registered
    // if (!localStorage.getItem('userRegistered')) {
    //     alert('Please register first before logging in.');
    //     window.location.href = 'register.html'; // Redirect to the registration page
    // }

    // Handle login form submission
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const loginEmail = document.getElementById('loginEmail').value;
        const loginPassword = document.getElementById('loginPassword').value;

        // Retrieve the registered user details
        const registeredUser = JSON.parse(localStorage.getItem('userRegistered'));

        // Check credentials
        if (
            registeredUser &&
            registeredUser.email === loginEmail &&
            registeredUser.password === loginPassword
        ) {
            alert('Login successful!');
            window.location.href = 'dashboard.html'; // Redirect to the dashboard or home page
        } else {
            loginError.textContent = 'Invalid email or password. Please try again.';
        }
    });
});
