# Load .env file if it exists
if (Test-Path ".env") {
    Get-Content .env | ForEach-Object {
        if ($_ -match "=" -and -not $_.StartsWith("#")) {
            $key, $value = $_.Split('=', 2)
            $key = $key.Trim()
            $value = $value.Trim().Trim('"').Trim("'")
            if (-not [string]::IsNullOrWhiteSpace($key)) {
                $env:$key = $value
            }
        }
    }
}

# Check if token is set
if (-not $env:DISCORD_BOT_TOKEN) {
    $token = Read-Host "Please enter your DISCORD_BOT_TOKEN"
    $env:DISCORD_BOT_TOKEN = $token
}

Write-Host "Starting Airdrop Commander..." -ForegroundColor Cyan
Write-Host "The dashboard will be available at http://localhost:8000" -ForegroundColor Green

python bot_api.py

