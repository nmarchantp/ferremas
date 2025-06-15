document.addEventListener('DOMContentLoaded', function () {
console.log("JS cargado");
  const form = document.getElementById('loginForm');

  form.addEventListener('submit', async function (e) {
    e.preventDefault(); 

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorBox = document.getElementById('loginError');
    errorBox.textContent = '';

    if (!email || !password) {
      errorBox.textContent = 'Debes completar ambos campos.';
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/clientes/login/', {
        method: 'POST',
        credentials: 'include', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {

        window.location.href = "/";
      } else {
        errorBox.textContent = data.error || 'Credenciales inválidas.';
      }
    } catch (error) {
      console.error("Error de red:", error);
      errorBox.textContent = 'No se pudo conectar con el servidor.';
    }
  });
});