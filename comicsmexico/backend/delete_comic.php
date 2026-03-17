<?php
require_once "config.php";
require_once "db_connect.php"; // Asegúrate de incluir este archivo

header('Content-Type: application/json');

// Validar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || !validateAPIKey($headers['Api-Key'])) {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

$data = json_decode(file_get_contents("php://input"), true);

if (!isset($data['comic_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Falta comic_id"]);
    exit;
}

$conn = getDBConnection();

$comic_id = intval($data['comic_id']);

// Primero eliminamos covers
$conn->query("DELETE FROM covers WHERE comic_id=$comic_id");

// Luego el comic
if ($conn->query("DELETE FROM comics WHERE id=$comic_id") === TRUE) {
    echo json_encode(["success" => true]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Error al eliminar comic: " . $conn->error]);
}

$conn->close();
?>
