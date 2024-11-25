<?php

header("Access-Control-Allow-Origin: *"); // Dopuszczamy żądania z dowolnego źródła
header("Access-Control-Allow-Methods: POST, GET, OPTIONS"); // Dopuszczamy metody POST, GET i OPTIONS
header("Access-Control-Allow-Headers: Content-Type");

// Obsługa metody OPTIONS (pre-flight request)
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    http_response_code(200);
    exit;
}
// Połączenie z bazą danych (ustawić odpowiednie dane dostępu)
$servername = "localhost";
$username = "mziolkowski";
$password = "michal9012";
$dbname = "bugherd";

// Tworzenie połączenia
$conn = new mysqli($servername, $username, $password, $dbname);

// Sprawdzenie połączenia
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Odbieranie danych przesłanych POST-em
$data = json_decode(file_get_contents('php://input'), true);


if ($data) {
    // Przygotowanie zapytania SQL
    $stmt = $conn->prepare("INSERT INTO bugs (description, assignee, priority, status, timestamp, url, selector, userAgent, platform, screenResolution, windowSize, attachment, types) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sssssssssssss", 
        $data['description'],
        $data['assignee'],
        $data['priority'],
        $data['status'],
        date('Y-m-d H:i:s', strtotime($data['timestamp'])), // Przekształcenie timestamp na format DATETIME
        $data['url'],
        $data['selector'],
        $data['user_agent'],
        $data['platform'],
        $data['screen_resolution'],
        $data['window_size'],
        $data['attachment'],
        $data['types']
    );

    // Wykonanie zapytania
    if ($stmt->execute()) {
        // Sukces - zwróć status 200 OK
        http_response_code(200);
        echo json_encode(array("message" => "Report submitted successfully."));
    } else {
        // Błąd wykonania zapytania
        http_response_code(500);
        echo json_encode(array("message" => "Failed to submit report."));
    }

    // Zamknięcie połączenia i statementu
    $stmt->close();
} else {
    // Jeśli dane nie zostały przesłane poprawnie
    http_response_code(400);
    echo json_encode(array("message" => "No data received."));
}

// Zamknięcie połączenia z bazą danych
$conn->close();

?>
