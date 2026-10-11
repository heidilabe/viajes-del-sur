/**
 * api.js - Helper de comunicación con la API REST (fetch + JWT).
 *
 * - Gestiona los tokens en localStorage (access_token / refresh_token).
 * - Adjunta la cabecera Authorization: Bearer <token> en POST/PUT/PATCH/DELETE.
 * - Ante un 401 Unauthorized limpia los tokens y redirige a /login/.
 * - Actualiza el menú de la barra de navegación según el estado de sesión.
 */

const TOKEN_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

function setTokens(access, refresh) {
  localStorage.setItem(TOKEN_KEY, access);
  if (refresh) {
    localStorage.setItem(REFRESH_KEY, refresh);
  }
}

function clearTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

function isLoggedIn() {
  return Boolean(getToken());
}

function authHeaders() {
  const headers = {};
  const token = getToken();
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  return headers;
}

function cerrarSesion() {
  clearTokens();
  actualizarMenu();
  window.location.href = '/';
}

function requerirSesion() {
  if (!isLoggedIn()) {
    window.location.href = '/login/';
    return false;
  }
  return true;
}

/**
 * Envía una petición a la API agregando el token cuando corresponde
 * y manejando la respuesta 401 Unauthorized.
 */
async function apiFetch(url, options = {}) {
  const opts = Object.assign({}, options);
  const method = (opts.method || 'GET').toUpperCase();
  const headers = Object.assign({}, opts.headers || {});

  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    Object.assign(headers, authHeaders());
  }

  const response = await fetch(url, Object.assign({}, opts, { headers: headers }));

  if (response.status === 401) {
    clearTokens();
    actualizarMenu();
    if (!window.location.pathname.startsWith('/login/')) {
      window.location.href = '/login/';
    }
    throw new Error('Sesión expirada o no autorizada (401).');
  }

  return response;
}

/**
 * Obtiene el contenido JSON de una respuesta, lanzando un error con
 * los mensajes de validación cuando la API responde 400/404/500.
 */
async function obtenerDatos(response) {
  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    data = null;
  }

  if (!response.ok) {
    const mensaje = typeof data === 'object' && data !== null
      ? JSON.stringify(data)
      : 'Error ' + response.status;
    const error = new Error(mensaje);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

/** Inicia sesión contra /api/token/ y almacena los tokens recibidos. */
async function iniciarSesion(username, password) {
  const response = await fetch('/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username, password: password }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error('No se pudo iniciar sesión. Verifica tus credenciales.');
    error.status = response.status;
    error.data = data;
    throw error;
  }

  setTokens(data.access, data.refresh);
  actualizarMenu();
  return data;
}

/** Muestra u oculta los enlaces de sesión en el menú principal. */
function actualizarMenu() {
  const enlace = document.getElementById('menu-auth');
  if (!enlace) {
    return;
  }

  if (isLoggedIn()) {
    enlace.textContent = 'Cerrar Sesión';
    enlace.setAttribute('href', '#');
    enlace.onclick = function (evento) {
      evento.preventDefault();
      cerrarSesion();
    };
  } else {
    enlace.textContent = 'Iniciar Sesión';
    enlace.setAttribute('href', '/login/');
    enlace.onclick = null;
  }
}

/** Renderiza mensajes de éxito o error dentro de un contenedor. */
function mostrarAlerta(contenedorId, mensaje, tipo) {
  const contenedor = document.getElementById(contenedorId);
  if (!contenedor) {
    return;
  }
  contenedor.innerHTML =
    '<div class="alert alert-' + (tipo || 'info') + ' alert-dismissible fade show" role="alert">' +
    mensaje +
    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>' +
    '</div>';
}

/** Convierte la respuesta 400 de DRF en una lista de mensajes legibles. */
function erroresValidacion(data) {
  if (!data || typeof data !== 'object') {
    return ['Error de validación desconocido.'];
  }
  return Object.keys(data).map(function (campo) {
    const valor = data[campo];
    return campo + ': ' + (Array.isArray(valor) ? valor.join(' ') : String(valor));
  });
}

document.addEventListener('DOMContentLoaded', actualizarMenu);
