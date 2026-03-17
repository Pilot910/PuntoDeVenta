<?php
require_once "config.php";
require_once "db_connect.php";

header('Content-Type: application/json');

// Validar API Key
$headers = getallheaders();
if (!isset($headers['Api-Key']) || !validateAPIKey($headers['Api-Key'])) {
    http_response_code(401);
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

$data = json_decode(file_get_contents("php://input"), true);

if (!isset($data['items']) || !is_array($data['items']) || empty($data['items'])) {
    http_response_code(400);
    echo json_encode(["error" => "No se recibieron items para la venta"]);
    exit;
}

$metodo_pago = $data['metodo_pago'] ?? 'efectivo';
$items = $data['items'];

$conn = getDBConnection();
$conn->begin_transaction();

try {
    $errores = [];

    // 1️⃣ Validar stock suficiente
    foreach ($items as $item) {
        $cover_id = intval($item['cover_id']);
        $cantidad = intval($item['cantidad']);

        $stmt = $conn->prepare("SELECT titulo, numero, stock FROM covers c JOIN comics co ON c.comic_id = co.id WHERE c.id=?");
        $stmt->bind_param("i", $cover_id);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        $stmt->close();

        if (!$row) {
            $errores[] = "Cover ID $cover_id no encontrado";
            continue;
        }

        if ($row['stock'] < $cantidad) {
            $errores[] = "{$row['titulo']}#{$row['numero']}: solo quedan {$row['stock']} en stock";
        }
    }

    if (!empty($errores)) {
        $conn->rollback();
        echo json_encode(["success" => false, "errores" => $errores]);
        exit;
    }

    // 2️⃣ Registrar venta
    $stmt = $conn->prepare("INSERT INTO ventas_fisicas (fecha, metodo_pago) VALUES (NOW(), ?)");
    $stmt->bind_param("s", $metodo_pago);
    $stmt->execute();
    $venta_id = $stmt->insert_id;
    $stmt->close();

    // 3️⃣ Actualizar stock y registrar detalle_ventas + ajustes_stock
    foreach ($items as $item) {
        $cover_id = intval($item['cover_id']);
        $cantidad = intval($item['cantidad']);

        // Obtener stock actual
        $stmt = $conn->prepare("SELECT stock FROM covers WHERE id=?");
        $stmt->bind_param("i", $cover_id);
        $stmt->execute();
        $result = $stmt->get_result();
        $stock_actual = $result->fetch_assoc()['stock'];
        $stmt->close();

        $nuevo_stock = $stock_actual - $cantidad;

        // Actualizar covers
        $stmt = $conn->prepare("UPDATE covers SET stock=?, estado_activo=? WHERE id=?");
        $estado_activo = ($nuevo_stock <= 0) ? 0 : 1;
        $stmt->bind_param("iii", $nuevo_stock, $estado_activo, $cover_id);
        $stmt->execute();
        $stmt->close();

        // Registrar detalle_ventas
        $stmt = $conn->prepare("INSERT INTO detalle_ventas (venta_id, cover_id, cantidad) VALUES (?, ?, ?)");
        $stmt->bind_param("iii", $venta_id, $cover_id, $cantidad);
        $stmt->execute();
        $stmt->close();

        // Registrar ajustes_stock
        $motivo = "venta";
        $stmt = $conn->prepare("INSERT INTO ajustes_stock (cover_id, cantidad, motivo, fecha) VALUES (?, ?, ?, NOW())");
        $cantidad_negativa = -$cantidad;
        $stmt->bind_param("iis", $cover_id, $cantidad_negativa, $motivo);
        $stmt->execute();
        $stmt->close();
    }

    $conn->commit();
    echo json_encode(["success" => true, "venta_id" => $venta_id]);

} catch (Exception $e) {
    $conn->rollback();
    http_response_code(500);
    echo json_encode(["error" => "Error al registrar la venta: " . $e->getMessage()]);
}

$conn->close();
?>
