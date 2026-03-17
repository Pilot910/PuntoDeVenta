<?php
header('Content-Type: application/json');
include('config.php');
include('db_connect.php');

// Validar API Key
if (!isset($_GET['api_key']) || !validateAPIKey($_GET['api_key'])) {
    echo json_encode(["error" => "API Key inválida"]);
    exit;
}

// Validar parámetro comic_id
if (!isset($_GET['comic_id'])) {
    echo json_encode(["error" => "Falta comic_id"]);
    exit;
}

$comic_id = intval($_GET['comic_id']);
$conn = getDBConnection();

// Consultar portadas (covers)
$sql = "SELECT id, ilustracion, ruta_imagen, estado_activo, stock, precio 
        FROM covers 
        WHERE comic_id = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $comic_id);
$stmt->execute();
$result = $stmt->get_result();

$covers = [];
while ($row = $result->fetch_assoc()) {
    $covers[] = $row;
}

echo json_encode($covers);

$stmt->close();
$conn->close();
?>
