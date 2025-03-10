# Install Node.js dependencies
npm install

# Install TypeScript type definitions
npm install --save-dev @types/react @types/react-dom @types/node @types/d3 @types/chart.js

# Install visualization libraries
npm install chart.js react-chartjs-2 d3 framer-motion

# Create .env file
$envContent = @"
NEXT_PUBLIC_API_URL=http://localhost:8000
"@
Set-Content -Path ".env.local" -Value $envContent

Write-Host "Setup completed successfully!" 