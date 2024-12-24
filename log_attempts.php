<?php
// Đường dẫn file JSON để lưu trữ
$logFile = 'ip_logs.json';

// Lấy dữ liệu JSON từ yêu cầu
$requestBody = file_get_contents('php://input');
$data = json_decode($requestBody, true);

if ($data) {
    // Đọc nội dung file JSON hiện có
    $logs = [];
    if (file_exists($logFile)) {
        $logs = json_decode(file_get_contents($logFile), true) ?: [];
    }

    // Thêm bản ghi mới vào mảng logs
    $logs[] = [
        'ip' => $data['ip'] ?? 'Unknown',
        'status' => $data['status'] ?? 'Unknown',
        'timestamp' => $data['timestamp'] ?? date('c')
    ];

    // Ghi lại dữ liệu vào file JSON
    file_put_contents($logFile, json_encode($logs, JSON_PRETTY_PRINT));
}

// Trả về phản hồi JSON
header('Content-Type: application/json');
echo json_encode(['status' => 'success']);
?>
