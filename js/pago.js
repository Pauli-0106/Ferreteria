// Validación de Tarjeta con RegEx mejorado
const validarTarjeta = (numero) => /^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$/.test(numero); // Visa/Mastercard

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('formulario-pago');
  const productoInfo = document.getElementById('producto-info');

  // Mostrar producto seleccionado
  const params = new URLSearchParams(window.location.search);
  if(params.has('producto') && params.has('precio')) {
    productoInfo.innerHTML = `
      <h3>🛒 Producto Seleccionado:</h3>
      <p>${decodeURIComponent(params.get('producto'))} - $${params.get('precio')}</p>
      <hr>
    `;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Elementos UI
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    const submitBtn = form.querySelector('button');
    submitBtn.disabled = true;
    form.appendChild(spinner);

    try {
      // Simular delay de red
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Validaciones
      const datos = {
        numero: form.numero.value.replace(/\s/g, ''),
        titular: form.titular.value.trim(),
        fecha: new Date(form.fecha.value),
        cvv: form.cvv.value
      };

      if (!validarTarjeta(datos.numero)) throw new Error('Tarjeta no válida. Use Visa/Mastercard');
      if (datos.fecha < new Date()) throw new Error('Fecha de expiración inválida');
      if (!/^[A-Za-z\sáéíóúÁÉÍÓÚñÑ]+$/.test(datos.titular)) throw new Error('Nombre en tarjeta inválido');

      // Éxito
      form.classList.add('oculto');
      document.getElementById('mensaje-exito').classList.add('visible');
      
      setTimeout(() => {
        window.location.href = `confirmacion.html?producto=${params.get('producto')}`;
      }, 3000);

    } catch (error) {
      mostrarError(error.message, form);
    } finally {
      spinner.remove();
      submitBtn.disabled = false;
    }
  });
});

function mostrarError(mensaje, contenedor) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-mensaje';
  errorDiv.textContent = mensaje;
  contenedor.insertBefore(errorDiv, contenedor.lastElementChild);
  
  setTimeout(() => errorDiv.remove(), 5000);
}