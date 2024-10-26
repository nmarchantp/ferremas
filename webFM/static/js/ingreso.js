// Función para mostrar/ocultar la contraseña
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');

if (passwordInput && togglePassword) {
    passwordInput.addEventListener('input', function () {
        togglePassword.style.display = this.value ? 'block' : 'none'; // Muestra el icono si hay texto
    });

    togglePassword.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
}
