<?php
header('Content-Type: application/json');
include('config.php');
include('db_connect.php');

// API Key fija
$api_key = "123456";

// Validar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || $headers['Api-Key'] !== $api_key) {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

// Obtener datos JSON
$data = json_decode(file_get_contents("php://input"), true);
if (!$data || !isset($data['cover_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Falta cover_id"]);
    exit;
}

$cover_id = intval($data['cover_id']);

$conn = getDBConnection();

// Eliminar cover
$stmt = $conn->prepare("DELETE FROM covers WHERE id=?");
$stmt->bind_param("i", $cover_id);

if ($stmt->execute()) {
    echo json_encode(["success" => true]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Error al eliminar la portada: ".$stmt->error]);
}

$stmt->close();
$conn->close();
?>
