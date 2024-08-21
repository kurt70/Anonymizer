$uri = "http://localhost:5000/anonymize"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    text = "Hei, mitt navn er Kari Nordmann, jeg bor på Storgata 5B, 0182 Oslo. Født 12. desember 1985. Telefonnummeret mitt er 99887766."
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
$response
