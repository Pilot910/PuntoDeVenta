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

$data = json_decode(file_get_contents("php://input"), true);

if (!isset($data['items'], $data['pago_metodo'])) {
    http_response_code(400);
    echo json_encode(["error" => "Faltan datos obligatorios"]);
    exit;
}

$conn = getDBConnection();
$fecha = date("Y-m-d H:i:s");

// Insertar venta
$conn->query("INSERT INTO ventas_fisicas (fecha, metodo_pago) VALUES ('$fecha', '".$conn->real_escape_string($data['pago_metodo'])."')");
$venta_id = $conn->insert_id;

// Insertar detalle de venta y actualizar stock
foreach ($data['items'] as $item) {
    $cover_id = intval($item['cover_id']);
    $cantidad = intval($item['cantidad']);
    $conn->query("INSERT INTO detalle_ventas (venta_id, cover_id, cantidad) VALUES ($venta_id, $cover_id, $cantidad)");
    $conn->query("UPDATE covers SET stock = stock - $cantidad WHERE id=$cover_id");
}

echo json_encode(["success" => true, "venta_id" => $venta_id]);
$conn->close();
?>
