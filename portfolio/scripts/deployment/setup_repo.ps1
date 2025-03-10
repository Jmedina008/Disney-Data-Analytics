# Setup script for Disney Data Portfolio repository

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Please install Git first."
    exit 1
}

# Initialize Git repository
git init

# Add remote repository (replace with your GitHub repository URL)
Write-Host "Enter your GitHub repository URL:"
$repoUrl = Read-Host
git remote add origin $repoUrl

# Create necessary directories
$directories = @(
    "data/raw",
    "data/processed",
    "data/analytics",
    "reports",
    "notebooks/disney_plus/data_collection",
    "notebooks/disney_plus/analysis",
    "notebooks/disney_plus/visualization",
    "notebooks/theme_parks/data_collection",
    "notebooks/theme_parks/analysis",
    "notebooks/theme_parks/visualization",
    "notebooks/entertainment/data_collection",
    "notebooks/entertainment/analysis",
    "notebooks/entertainment/visualization"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir
    New-Item -ItemType File -Force -Path "$dir/.gitkeep"
}

# Stage all files
git add .

# Initial commit
git commit -m "Initial commit: Project structure and core components"

# Push to main branch
Write-Host "Pushing to main branch..."
git push -u origin main

Write-Host "Repository setup complete!" 