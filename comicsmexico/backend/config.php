<?php
// Configuración de API Key
define('API_KEY', '123456'); // Usa la misma que tu frontend

// Validar API Key enviada por la app
function validateAPIKey($key) {
    return $key === API_KEY;
}
?>
