<?php
include "db_connect.php";

header("Content-Type: application/json");

$conn = getDBConnection();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id'] ?? null;
    $titulo = $_POST['titulo'] ?? null;
    $autor = $_POST['autor'] ?? null;
    $precio = $_POST['precio'] ?? null;
    $stock = $_POST['stock'] ?? null;
    $portada = $_POST['portada'] ?? null;

    if (!$id) {
        echo json_encode(["success" => false, "error" => "ID no proporcionado"]);
        exit;
    }

    $query = "UPDATE comics 
              SET titulo = ?, autor = ?, precio = ?, stock = ?, portada = ?
              WHERE id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ssdisi", $titulo, $autor, $precio, $stock, $portada, $id);

    if ($stmt->execute()) {
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["success" => false, "error" => $stmt->error]);
    }

    $stmt->close();
} else {
    echo json_encode(["success" => false, "error" => "Método no permitido"]);
}

$conn->close();
?>
