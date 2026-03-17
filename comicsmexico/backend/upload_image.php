<?php
require_once "config.php";

// Subir imagen al servidor (comicsImg/)
header('Content-Type: application/json');

// Verificar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || !validateAPIKey($headers['Api-Key'])) {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

// Verificar archivo
if (!isset($_FILES['image'])) {
    http_response_code(400);
    echo json_encode(["error" => "No se envió ninguna imagen"]);
    exit;
}

$uploadDir = "../comicsImg/"; // Ruta relativa
$file = $_FILES['image'];
$targetFile = $uploadDir . basename($file["name"]);

if (move_uploaded_file($file["tmp_name"], $targetFile)) {
    echo json_encode(["success" => true, "path" => "comicsImg/" . basename($file["name"])]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Error al subir la imagen"]);
}
?>
