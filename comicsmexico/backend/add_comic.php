<?php
include "db_connect.php";

$data = json_decode(file_get_contents("php://input"), true);
$titulo = $data['titulo'];
$numero = $data['numero'];
$editorial = $data['editorial'];
$descripcion = $data['descripcion'];

$conn = getDBConnection();
$stmt = $conn->prepare("INSERT INTO comics (titulo, numero, editorial, descripcion) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $titulo, $numero, $editorial, $descripcion);
$stmt->execute();

$id = $stmt->insert_id;
$stmt->close();
echo json_encode(["id" => $id]);
?>
