// Switch to the signup form when the "Create one" link is clicked
document.getElementById('signup-link').addEventListener('click', function() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('signup-form').classList.remove('hidden');
    document.getElementById('signup-tab').classList.add('active');
    document.getElementById('login-tab').classList.remove('active');
});

// Switch to the login form when the "Login" link is clicked in the signup form
document.getElementById('login-link').addEventListener('click', function() {
    document.getElementById('signup-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('login-tab').classList.add('active');
    document.getElementById('signup-tab').classList.remove('active');
});

// Optional: Add form submission handling
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Add your login handling logic here
    alert('Login Form Submitted');
});

document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Add your signup handling logic here
    alert('Signup Form Submitted');
});