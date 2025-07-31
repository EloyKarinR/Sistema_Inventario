// Búsqueda de clientes
document.addEventListener('DOMContentLoaded', function() {
    const buscarClienteInput = document.getElementById('buscarCliente');
    const resultadosClientes = document.getElementById('resultadosClientes');
    let timeoutId;

    // Función para buscar clientes
    function buscarClientes(query) {
        fetch(`/buscar-clientes/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    mostrarResultadosClientes(data.clientes);
                } else {
                    console.error('Error en la búsqueda:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Función para mostrar los resultados
    function mostrarResultadosClientes(clientes) {
        resultadosClientes.innerHTML = '';
        
        if (clientes.length === 0) {
            resultadosClientes.innerHTML = `
                <div class="list-group-item text-center text-muted">
                    No se encontraron clientes
                </div>`;
            return;
        }

        clientes.forEach(cliente => {
            const elemento = document.createElement('a');
            elemento.href = '#';
            elemento.className = 'list-group-item list-group-item-action';
            elemento.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${cliente.nombre}</h6>
                    <small>${cliente.num_compras} compras</small>
                </div>
                <p class="mb-1">RUT/NIT: ${cliente.numero_impuesto}</p>
                <small>Tel: ${cliente.telefono || 'No disponible'}</small>
            `;
            
            elemento.addEventListener('click', (e) => {
                e.preventDefault();
                seleccionarCliente(cliente);
            });
            
            resultadosClientes.appendChild(elemento);
        });
    }

    // Event listener para la búsqueda con debounce
    buscarClienteInput.addEventListener('input', (e) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                buscarClientes(query);
            } else {
                resultadosClientes.innerHTML = '';
            }
        }, 300);
    });

    // Manejo del formulario de nuevo cliente
    const formNuevoCliente = document.getElementById('formNuevoCliente');
    const btnGuardarCliente = document.getElementById('guardarNuevoCliente');

    btnGuardarCliente.addEventListener('click', () => {
        const formData = {
            nombre: document.getElementById('nombreCliente').value,
            numero_impuesto: document.getElementById('numeroImpuesto').value,
            telefono: document.getElementById('telefonoCliente').value,
            correo_electronico: document.getElementById('correoCliente').value
        };

        fetch('/crear-cliente-rapido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Cerrar modal y mostrar mensaje de éxito
                const modal = bootstrap.Modal.getInstance(document.getElementById('nuevoClienteModal'));
                modal.hide();
                
                // Limpiar formulario
                formNuevoCliente.reset();
                
                // Seleccionar el cliente recién creado
                seleccionarCliente(data.cliente);
                
                // Mostrar mensaje de éxito
                mostrarMensaje('Cliente creado exitosamente', 'success');
            } else {
                mostrarMensaje(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error al crear el cliente', 'error');
        });
    });
});

// Función para obtener el token CSRF
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Función para seleccionar un cliente
function seleccionarCliente(cliente) {
    // Actualizar el campo oculto con el ID del cliente
    document.getElementById('cliente_id').value = cliente.id;
    
    // Mostrar la información del cliente seleccionado
    const clienteInfo = document.getElementById('cliente_info');
    const clienteDetalles = document.getElementById('cliente_detalles');
    
    clienteDetalles.innerHTML = `
        <strong>${cliente.nombre}</strong><br>
        RUT/NIT: ${cliente.numero_impuesto}<br>
        Tel: ${cliente.telefono || 'No disponible'}
    `;
    
    // Mostrar el div de información del cliente
    clienteInfo.style.display = 'block';
    
    // Limpiar la búsqueda
    document.getElementById('buscarCliente').value = '';
    document.getElementById('resultadosClientes').innerHTML = '';
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.querySelector('.card-body').insertBefore(alertDiv, document.querySelector('.form-group'));
    
    // Auto-cerrar después de 3 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}
