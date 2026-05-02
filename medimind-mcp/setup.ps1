# ==========================================
# MediMind MCP - Development Setup Script
# ==========================================
# 
# This script automates Phase 1 setup:
# 1. Generate encryption keys
# 2. Create .env file
# 3. Install Python dependencies
# 4. Start Docker infrastructure
# 5. Initialize database
# 
# ⚠️ Run from project root directory
# ==========================================

$ErrorActionPreference = "Stop"

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  MediMind MCP - HIPAA-Compliant Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# ==========================================
# Check Prerequisites
# ==========================================
Write-Host "[1/7] Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -notmatch "Python 3\.1[1-9]") {
        Write-Host "❌ Python 3.11+ required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Install Python 3.11+ first." -ForegroundColor Red
    exit 1
}

# Check Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check Docker Compose
try {
    $composeVersion = docker-compose --version 2>&1
    Write-Host "✅ Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose not found." -ForegroundColor Red
    exit 1
}

Write-Host ""

# ==========================================
# Generate Encryption Keys
# ==========================================
Write-Host "[2/7] Generating encryption keys..." -ForegroundColor Yellow

$ENCRYPTION_KEY = python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
$SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"

Write-Host "✅ Encryption keys generated" -ForegroundColor Green
Write-Host "   ENCRYPTION_KEY: $($ENCRYPTION_KEY.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "   SECRET_KEY: $($SECRET_KEY.Substring(0, 20))..." -ForegroundColor Gray
Write-Host ""

# ==========================================
# Create .env File
# ==========================================
Write-Host "[3/7] Creating .env file..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists. Backing up..." -ForegroundColor Yellow
    Move-Item -Path ".env" -Destination ".env.backup" -Force
}

# Generate random passwords
$POSTGRES_PASSWORD = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})
$MONGO_PASSWORD = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})
$REDIS_PASSWORD = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})

# Create .env file
@"
# ==========================================
# MediMind MCP - Environment Configuration
# ⚠️ NEVER COMMIT THIS FILE!
# ==========================================

# Environment
ENVIRONMENT=development
DEBUG=True

# Database (ENCRYPTED!)
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
MONGO_PASSWORD=$MONGO_PASSWORD
REDIS_PASSWORD=$REDIS_PASSWORD

DATABASE_URL=postgresql://medimind:$POSTGRES_PASSWORD@localhost:5432/medimind?sslmode=require
MONGODB_URL=mongodb://medimind:$MONGO_PASSWORD@localhost:27017/medimind?authSource=admin
REDIS_URL=redis://:$REDIS_PASSWORD@localhost:6379/0

# FHIR Server (Epic Sandbox)
# TODO: Register at https://fhir.epic.com/Developer/Apps
FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4
FHIR_CLIENT_ID=your_epic_sandbox_client_id
FHIR_CLIENT_SECRET=your_epic_sandbox_client_secret
FHIR_REDIRECT_URI=http://localhost:8000/auth/fhir/callback

# External APIs (Development)
PUBMED_API_KEY=development_placeholder
DRUGBANK_API_KEY=development_placeholder
UPTODATE_API_KEY=

# Security (GENERATED!)
ENCRYPTION_KEY=$ENCRYPTION_KEY
SECRET_KEY=$SECRET_KEY
AWS_KMS_KEY_ID=

# HIPAA Compliance
PHI_ENCRYPTION_ENABLED=True
AUDIT_LOG_RETENTION_DAYS=2555
SESSION_TIMEOUT_MINUTES=15
BREACH_NOTIFICATION_EMAIL=security@hospital.com

# AI Models
MODEL_PATH=./models
BIOGPT_MODEL=microsoft/biogpt
SCISPACY_MODEL=en_core_sci_lg
"@ | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✅ .env file created" -ForegroundColor Green
Write-Host "   ⚠️  TODO: Add Epic FHIR credentials to .env" -ForegroundColor Yellow
Write-Host ""

# ==========================================
# Create Virtual Environment
# ==========================================
Write-Host "[4/7] Setting up Python environment..." -ForegroundColor Yellow

if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate and install dependencies
Write-Host "   Installing dependencies (this may take a few minutes)..." -ForegroundColor Gray
& ".\venv\Scripts\Activate.ps1"
pip install --quiet --upgrade pip
pip install --quiet -r mcp-server/requirements.txt

Write-Host "✅ Python dependencies installed" -ForegroundColor Green
Write-Host ""

# ==========================================
# Start Docker Infrastructure
# ==========================================
Write-Host "[5/7] Starting Docker infrastructure..." -ForegroundColor Yellow

docker-compose up -d

# Wait for services to be healthy
Write-Host "   Waiting for services to be ready..." -ForegroundColor Gray
Start-Sleep -Seconds 10

$healthyServices = docker-compose ps --services --filter "status=running" | Measure-Object | Select-Object -ExpandProperty Count

if ($healthyServices -ge 3) {
    Write-Host "✅ Infrastructure started (PostgreSQL, MongoDB, Redis)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some services may not be healthy. Check: docker-compose ps" -ForegroundColor Yellow
}

Write-Host ""

# ==========================================
# Initialize Database
# ==========================================
Write-Host "[6/7] Initializing database..." -ForegroundColor Yellow

Set-Location -Path "mcp-server"

# Initialize Alembic
if (-not (Test-Path "alembic.ini")) {
    alembic init migrations
    Write-Host "✅ Alembic initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Alembic already initialized" -ForegroundColor Green
}

Write-Host "   ⚠️  TODO: Run 'alembic revision --autogenerate -m \"Initial schema\"'" -ForegroundColor Yellow
Write-Host "   ⚠️  TODO: Run 'alembic upgrade head' to apply migrations" -ForegroundColor Yellow

Set-Location -Path ".."
Write-Host ""

# ==========================================
# Final Instructions
# ==========================================
Write-Host "[7/7] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Register for Epic Sandbox:" -ForegroundColor White
Write-Host "   https://fhir.epic.com/Developer/Apps" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Add Epic credentials to .env:" -ForegroundColor White
Write-Host "   FHIR_CLIENT_ID=your_client_id" -ForegroundColor Gray
Write-Host "   FHIR_CLIENT_SECRET=your_client_secret" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Initialize database:" -ForegroundColor White
Write-Host "   cd mcp-server" -ForegroundColor Gray
Write-Host "   alembic revision --autogenerate -m 'Initial schema'" -ForegroundColor Gray
Write-Host "   alembic upgrade head" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Start FastAPI server:" -ForegroundColor White
Write-Host "   uvicorn src.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Test health check:" -ForegroundColor White
Write-Host "   Invoke-RestMethod -Uri http://localhost:8000/health" -ForegroundColor Gray
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  ⚠️  SECURITY REMINDERS:" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  • NEVER commit .env file to git" -ForegroundColor Red
Write-Host "  • Keep encryption keys secure" -ForegroundColor Red
Write-Host "  • Enable MFA for all users" -ForegroundColor Red
Write-Host "  • Review HIPAA_CHECKLIST.md regularly" -ForegroundColor Red
Write-Host ""
Write-Host "Documentation: mcp-server/README.md" -ForegroundColor Gray
Write-Host "HIPAA Checklist: compliance/HIPAA_CHECKLIST.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy coding! 🏥💙" -ForegroundColor Cyan
