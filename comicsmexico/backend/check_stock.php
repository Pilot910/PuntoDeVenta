<?php
require_once "config.php";

header('Content-Type: application/json');

// Validar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || !validateAPIKey($headers['Api-Key'])) {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

// Recibir cover_id y cantidad a vender
$data = json_decode(file_get_contents("php://input"), true);
if (!isset($data['cover_id'], $data['cantidad'])) {
    http_response_code(400);
    echo json_encode(["error" => "Faltan datos obligatorios"]);
    exit;
}

$conn = getDBConnection();
$cover_id = intval($data['cover_id']);
$cantidad = intval($data['cantidad']);

// Consultar stock
$result = $conn->query("SELECT stock FROM covers WHERE id=$cover_id");
if ($result && $row = $result->fetch_assoc()) {
    $stock_actual = intval($row['stock']);
    if ($stock_actual >= $cantidad) {
        echo json_encode(["available" => true, "stock_actual" => $stock_actual]);
    } else {
        echo json_encode(["available" => false, "stock_actual" => $stock_actual]);
    }
} else {
    http_response_code(404);
    echo json_encode(["error" => "Cover no encontrado"]);
}

$conn->close();
?>
