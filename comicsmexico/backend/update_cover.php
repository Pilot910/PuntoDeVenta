<?php
header('Content-Type: application/json');
include('config.php');
include('db_connect.php');

// Validar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || $headers['Api-Key'] !== '123456') {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

// Obtener datos JSON
$data = json_decode(file_get_contents("php://input"), true);
if (!$data) {
    http_response_code(400);
    echo json_encode(["error" => "JSON inválido o vacío"]);
    exit;
}

// Validar campos necesarios
if (!isset($data['cover_id'], $data['ilustracion'], $data['ruta_imagen'], $data['stock'], $data['precio'])) {
    http_response_code(400);
    echo json_encode(["error" => "Faltan campos obligatorios"]);
    exit;
}

$cover_id = intval($data['cover_id']);
$ilustracion = $data['ilustracion'];
$ruta_imagen = $data['ruta_imagen'];
$stock = intval($data['stock']);
$precio = floatval($data['precio']);

$conn = getDBConnection();

$stmt = $conn->prepare("UPDATE covers SET ilustracion=?, ruta_imagen=?, stock=?, precio=? WHERE id=?");
$stmt->bind_param("ssidi", $ilustracion, $ruta_imagen, $stock, $precio, $cover_id);

if ($stmt->execute()) {
    echo json_encode(["success" => true]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Error al actualizar la portada: " . $stmt->error]);
}

$stmt->close();
$conn->close();
?>
