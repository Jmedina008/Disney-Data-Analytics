# Start FastAPI backend
Start-Process -FilePath "python" -ArgumentList "-m uvicorn api.main:app --reload" -WorkingDirectory "."

# Start Next.js frontend
Set-Location website
npm run dev 