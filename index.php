<?php
error_reporting(0);
session_start();
date_default_timezone_set("Asia/Ho_Chi_Minh");

$useragent = "Mozilla/5.0 (Linux; Android 10; Active 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36";

$txt = substr(md5(date('dmY')."toolvip".$_SERVER['REMOTE_ADDR']), 0 , 8);

// Mã hóa key trước khi gửi yêu cầu
$encoded_key = base64_encode($txt);

$linkkey = urlencode("https://luvanlong.000webhostapp.com/key.html?key=$encoded_key");

$response = requests("https://web1s.com/api?token=fdd3048e-2124-4820-90d1-208a2b26ea0d&url=".$linkkey);

if($response->status == "success" and $linkkey != '') {
    // Giải mã key sau khi nhận được yêu cầu thành công
    $decoded_key = base64_decode($txt);
    
    die(json_encode([
        "success" => '200',
        "key" => $decoded_key,
        "link" =>  $response->shortenedUrl,
        "ip" => $_SERVER['REMOTE_ADDR'],
    ]));
} else {
    die(json_encode([
        "link" =>  'Hãy Dùng Key Phí',
        "ip" => $_SERVER['REMOTE_ADDR'],
        "coun" => $so,
    ]));
}

function requests($url) {
	$ch = curl_init();
	curl_setopt_array($ch, array(
		CURLOPT_URL => $url,
		CURLOPT_CUSTOMREQUEST => "GET",
		CURLOPT_SSL_VERIFYHOST => false,
		CURLOPT_SSL_VERIFYPEER => false,
		CURLOPT_RETURNTRANSFER => true,
		CURLOPT_TIMEOUT => 15,
		CURLOPT_ENCODING => "",
		CURLOPT_FOLLOWLOCATION => true
	));
	$response = curl_exec($ch);
	return json_decode($response);
}
?>
