<?php
include "db_connect.php";
include "config.php";

header("Content-Type: application/json");

$conn = getDBConnection();
if (!$conn) {
    echo json_encode(["error" => "Error al conectar con la base de datos"]);
    exit;
}

$sql = "
SELECT 
    c.id,
    c.titulo,
    c.numero,
    c.editorial,
    IFNULL(SUM(cv.stock), 0) AS stock_total
FROM comics c
LEFT JOIN covers cv ON cv.comic_id = c.id
WHERE c.activo = 1
GROUP BY c.id, c.titulo, c.numero, c.editorial
ORDER BY c.titulo ASC
";

$result = $conn->query($sql);

if (!$result) {
    echo json_encode(["error" => "Error en la consulta: " . $conn->error]);
    $conn->close();
    exit;
}

$comics = [];
while ($row = $result->fetch_assoc()) {
    $comics[] = $row;
}

echo json_encode($comics, JSON_UNESCAPED_UNICODE);
$conn->close();
?>
