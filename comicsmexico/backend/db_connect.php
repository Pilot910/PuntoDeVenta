<?php
function getDBConnection() {
    $DB_HOST = "localhost";
    $DB_USER = "root";        
    $DB_PASS = "";            
    $DB_NAME = "comicsdb";    

    $conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }
    $conn->set_charset("utf8mb4");
    return $conn;
}
?>
