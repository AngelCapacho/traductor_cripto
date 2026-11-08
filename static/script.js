// Función para cambiar de pestaña en el menú principal
function showTab(tabId) {
    // Ocultar todos los contenidos de pestañas
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Quitar estado activo de todos los botones de navegación
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));

    // Mostrar la pestaña seleccionada
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Activar el botón correspondiente
    event.currentTarget.classList.add('active');
}

// Función para mostrar/ocultar parámetros según el cifrado seleccionado
function toggleCipherInputs() {
    const cipher = document.getElementById('cipher-select').value;
    const caesarParams = document.getElementById('caesar-params');
    const subParams = document.getElementById('substitution-params');

    // Ocultar ambos parámetros por defecto
    caesarParams.classList.add('hidden');
    subParams.classList.add('hidden');

    // Mostrar el parámetro correspondiente
    if (cipher === 'caesar') {
        caesarParams.classList.remove('hidden');
    } else if (cipher === 'substitution') {
        subParams.classList.remove('hidden');
    }
}

// Función principal para procesar codificación/decodificación mediante Fetch API
async function processTranslation(action) {
    const cipher = document.getElementById('cipher-select').value;
    const inputText = document.getElementById('input-text').value;
    const outputText = document.getElementById('output-text');

    if (!inputText.trim()) {
        outputText.value = "Por favor, ingresa un texto para procesar.";
        return;
    }

    let url = `/api/${cipher}/`;
    let bodyData = { text: inputText };

    // Determinar la sub-ruta según el tipo de acción (encode/decode o encrypt/decrypt)
    if (cipher === 'caesar') {
        const shiftVal = parseInt(document.getElementById('caesar-shift').value) || 3;
        url += (action === 'encode') ? 'encrypt' : 'decrypt';
        bodyData.shift = shiftVal;
    } else if (cipher === 'substitution') {
        const keyVal = document.getElementById('sub-key').value;
        url += (action === 'encode') ? 'encrypt' : 'decrypt';
        bodyData.key = keyVal;
    } else {
        url += (action === 'encode') ? 'encode' : 'decode';
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();

        if (response.ok) {
            outputText.value = data.result;
        } else {
            // Manejar errores devueltos por la API (ej: clave de sustitución inválida)
            outputText.value = `Error: ${data.detail || 'No se pudo procesar la solicitud'}`;
        }
    } catch (error) {
        console.error('Error en la petición:', error);
        outputText.value = "Error de conexión con el servidor backend.";
    }
}

// Función para el Detector Inteligente de Patrones
async function analyzePattern() {
    const inputText = document.getElementById('detector-input').value;
    const resultsContainer = document.getElementById('detector-results');

    if (!inputText.trim()) {
        resultsContainer.innerHTML = '<p style="color: var(--text-secondary);">Por favor, ingresa una cadena de texto para analizar.</p>';
        return;
    }

    resultsContainer.innerHTML = '<p style="color: var(--text-secondary);">Analizando patrón...</p>';

    try {
        const response = await fetch('/api/detector/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText })
        });

        const data = await response.json();
        resultsContainer.innerHTML = '';

        if (data.matches && data.matches.length > 0) {
            data.matches.forEach(match => {
                const card = document.createElement('div');
                card.className = 'match-card';
                card.innerHTML = `
                    <h3 style="color: var(--primary); margin-bottom: 4px;">Formato: ${match.type}</h3>
                    <p><strong>Nivel de Confianza:</strong> ${match.confidence}</p>
                    <p style="color: var(--text-secondary); margin-top: 4px;">${match.reason}</p>
                `;
                resultsContainer.appendChild(card);
            });
        } else {
            resultsContainer.innerHTML = '<p style="color: var(--text-secondary);">No se detectó un patrón conocido con certeza.</p>';
        }
    } catch (error) {
        console.error('Error al analizar patrón:', error);
        resultsContainer.innerHTML = '<p style="color: red;">Error al comunicarse con el servidor.</p>';
    }
}

// Función para generar los 25 Desplazamientos César
async function generateAllShifts() {
    const inputText = document.getElementById('caesar-all-input').value;
    const shiftsContainer = document.getElementById('caesar-shifts-results');

    if (!inputText.trim()) {
        shiftsContainer.innerHTML = '<p style="color: var(--text-secondary);">Ingresa un texto para generar sus desplazamientos.</p>';
        return;
    }

    shiftsContainer.innerHTML = '<p style="color: var(--text-secondary);">Generando las 25 variantes...</p>';

    try {
        const response = await fetch('/api/caesar/all-shifts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText })
        });

        const data = await response.json();
        shiftsContainer.innerHTML = '';

        if (data.shifts) {
            Object.entries(data.shifts).forEach(([shift, text]) => {
                const card = document.createElement('div');
                card.className = 'shift-card';
                card.innerHTML = `
                    <span style="font-weight: 700; color: var(--primary);">Shift +${shift}:</span>
                    <p style="font-family: monospace; margin-top: 4px; word-break: break-all;">${text}</p>
                `;
                shiftsContainer.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error al generar desplazamientos:', error);
        shiftsContainer.innerHTML = '<p style="color: red;">Error al comunicarse con el servidor.</p>';
    }
}

// Cargar el catálogo educativo desde la API / JSON estático
async function loadCatalog() {
    const catalogContainer = document.getElementById('catalog-container');
    if (!catalogContainer) return;

    try {
        const response = await fetch('/static/../app/data/catalog.json');
        // Si se sirve mediante endpoint en main.py o ruta relativa:
        const catalogData = await response.json();

        catalogContainer.innerHTML = '';
        catalogData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'catalog-card';
            card.innerHTML = `
                <h3 style="color: var(--primary); margin-bottom: 6px;">${item.name}</h3>
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); background: var(--bg-main); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--border);">${item.category}</span>
                <p style="margin-top: 10px;"><strong>Historia:</strong> ${item.history}</p>
                <p style="margin-top: 6px;"><strong>Uso en Ciberseguridad/Informática:</strong> ${item.usage}</p>
            `;
            catalogContainer.appendChild(card);
        });
    } catch (error) {
        // Carga alternativa si catalog.json se sirve directamente o mediante endpoint
        console.warn('Cargando catálogo educativo por endpoint alternativo...');
    }
}

// Cargar el catálogo educativo desde el backend
async function loadCatalog() {
    const catalogContainer = document.getElementById('catalog-container');
    if (!catalogContainer) return;

    try {
        const response = await fetch('/api/catalog');
        const catalogData = await response.json();

        catalogContainer.innerHTML = '';
        
        if (catalogData.length === 0) {
            catalogContainer.innerHTML = '<p style="color: var(--text-secondary);">No se encontraron datos en el catálogo.</p>';
            return;
        }

        catalogData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'catalog-card';
            card.innerHTML = `
                <h3 style="color: var(--primary); margin-bottom: 6px;">${item.name}</h3>
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); background: var(--bg-main); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--border); display: inline-block;">${item.category}</span>
                <p style="margin-top: 12px; color: var(--text-primary);"><strong>Historia:</strong> ${item.history}</p>
                <p style="margin-top: 6px; color: var(--text-primary);"><strong>Uso en Ciberseguridad / Informática:</strong> ${item.usage}</p>
            `;
            catalogContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error al cargar el catálogo:', error);
        catalogContainer.innerHTML = '<p style="color: red;">Error al cargar el catálogo educativo.</p>';
    }
}

// Cargar el catálogo educativo desde el backend
async function loadCatalog() {
    const catalogContainer = document.getElementById('catalog-container');
    if (!catalogContainer) return;

    try {
        const response = await fetch('/api/catalog');
        const catalogData = await response.json();

        catalogContainer.innerHTML = '';
        
        if (catalogData.length === 0) {
            catalogContainer.innerHTML = '<p style="color: var(--text-secondary);">No se encontraron datos en el catálogo.</p>';
            return;
        }

        catalogData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'catalog-card';
            card.innerHTML = `
                <h3 style="color: var(--primary); margin-bottom: 6px;">${item.name}</h3>
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); background: var(--bg-main); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--border); display: inline-block;">${item.category}</span>
                <p style="margin-top: 12px; color: var(--text-primary);"><strong>Historia:</strong> ${item.history}</p>
                <p style="margin-top: 6px; color: var(--text-primary);"><strong>Uso en Ciberseguridad / Informática:</strong> ${item.usage}</p>
            `;
            catalogContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error al cargar el catálogo:', error);
        catalogContainer.innerHTML = '<p style="color: red;">Error al cargar el catálogo educativo.</p>';
    }
}

// Cargar catálogo al iniciar la página
async function loadCatalog() {
    const catalogContainer = document.getElementById('catalog-container');
    if (!catalogContainer) return;

    try {
        const response = await fetch('/api/catalog');
        const catalogData = await response.json();

        catalogContainer.innerHTML = '';
        
        if (catalogData.length === 0) {
            catalogContainer.innerHTML = '<p style="color: var(--text-secondary);">No se encontraron datos en el catálogo.</p>';
            return;
        }

        catalogData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'catalog-card';
            card.innerHTML = `
                <h3 style="color: var(--primary); margin-bottom: 6px;">${item.name}</h3>
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); background: var(--bg-main); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--border); display: inline-block;">${item.category}</span>
                <p style="margin-top: 12px; color: var(--text-primary);"><strong>Historia:</strong> ${item.history}</p>
                <p style="margin-top: 6px; color: var(--text-primary);"><strong>Uso en Ciberseguridad / Informática:</strong> ${item.usage}</p>
            `;
            catalogContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error al cargar el catálogo:', error);
        catalogContainer.innerHTML = '<p style="color: red;">Error al cargar el catálogo educativo.</p>';
    }
}

// Cargar catálogo al iniciar la página
document.addEventListener('DOMContentLoaded', loadCatalog);