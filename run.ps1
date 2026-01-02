# Check if token is set
if (-not $env:DISCORD_BOT_TOKEN) {
    $token = Read-Host "Please enter your DISCORD_BOT_TOKEN"
    $env:DISCORD_BOT_TOKEN = $token
}

Write-Host "Starting Airdrop Commander..." -ForegroundColor Cyan
Write-Host "The dashboard will be available at http://localhost:8000" -ForegroundColor Green

python bot_api.py
