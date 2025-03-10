# Install Node.js dependencies
npm install

# Create necessary directories if they don't exist
if (!(Test-Path "src")) {
    New-Item -ItemType Directory -Path "src"
}
if (!(Test-Path "public")) {
    New-Item -ItemType Directory -Path "public"
}

# Create environment file
$envContent = @"
REACT_APP_TMDB_API_KEY=your_tmdb_api_key_here
REACT_APP_API_URL=http://localhost:8000
"@
Set-Content -Path ".env" -Value $envContent

# Install Python dependencies for the backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r ..\requirements.txt

Write-Host "Setup completed! Please update the .env file with your actual API keys."
Write-Host "To start the development server, run: npm start" 