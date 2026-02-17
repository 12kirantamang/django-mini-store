// script.js
function togglePassword() {
    const passwordField = document.getElementById('passwordField');
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Sign in attempted!');
});