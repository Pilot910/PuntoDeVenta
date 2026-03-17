<?php
include "db_connect.php";

$comic_id = $_POST['comic_id'];
$ilustracion = $_POST['ilustracion'];
$stock = $_POST['stock'];
$precio = $_POST['precio'];

// Ruta base absoluta en tu servidor XAMPP
$base_path = "C:\\xampp\\htdocs\\comicsmexico\\comicsImg\\";  // 👈 usa doble barra invertida
$target_dir = $base_path;
$target_file = $target_dir . basename($_FILES["file"]["name"]);

// Mover el archivo al directorio correcto
if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {

    // Ruta que se guardará en la base de datos (absoluta)
    $ruta_imagen = "C:\\xampp\\htdocs\\comicsmexico\\comicsImg\\" . basename($_FILES["file"]["name"]);

    $conn = getDBConnection();
    $stmt = $conn->prepare("INSERT INTO covers (comic_id, ilustracion, ruta_imagen, stock, precio, estado_activo)
                            VALUES (?, ?, ?, ?, ?, 1)");
    $stmt->bind_param("issii", $comic_id, $ilustracion, $ruta_imagen, $stock, $precio);
    $stmt->execute();
    $stmt->close();

    echo json_encode(["success" => true, "ruta_guardada" => $ruta_imagen]);
} else {
    echo json_encode(["success" => false, "error" => "Error al mover el archivo"]);
}
?>
