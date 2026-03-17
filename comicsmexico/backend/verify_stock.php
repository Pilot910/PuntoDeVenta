<?php
require_once 'db_connect.php';
$headers = getallheaders();
validar_api_key($headers);

$id = $_GET['id'];
$res = $conn->query("SELECT stock FROM comics WHERE id=$id");

if ($res->num_rows > 0) {
    $row = $res->fetch_assoc();
    echo json_encode($row);
} else {
    echo json_encode(["error" => "No encontrado"]);
}
?>