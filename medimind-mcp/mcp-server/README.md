# 🏥 MediMind MCP - HIPAA-Compliant Clinical Decision Support

**AI-Powered Clinical Intelligence for Hospitals and Clinics**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![HIPAA Compliant](https://img.shields.io/badge/HIPAA-Compliant-red.svg)]()
[![License](https://img.shields.io/badge/license-Proprietary-orange.svg)]()

---

## ⚠️ CRITICAL: HIPAA COMPLIANCE

**This system handles Protected Health Information (PHI).** Any breach must be reported to patients and HHS within 60 days. Penalties: $100-$50,000 per violation, criminal charges possible.

**DO NOT:**
- Commit secrets (`.env`, encryption keys) to git
- Log PHI in plain text
- Deploy without TLS/SSL
- Share credentials
- Disable audit logging

---

## 🚀 Quick Start (Development)

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (via Docker)
- Git

### 1. Clone Repository

```powershell
git clone https://github.com/yourhospital/medimind-mcp.git
cd medimind-mcp
```

### 2. Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r mcp-server/requirements.txt
```

### 3. Generate Encryption Keys

```powershell
# Generate Fernet encryption key
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"

# Generate JWT secret key
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
```

**⚠️ SAVE THESE KEYS SECURELY!** You'll need them for the `.env` file.

### 4. Configure Environment

```powershell
# Copy example environment file
copy env.example .env

# Edit .env with your keys (use notepad or VSCode)
notepad .env
```

**Required Configuration:**
- `ENCRYPTION_KEY`: From step 3
- `SECRET_KEY`: From step 3
- `POSTGRES_PASSWORD`: Choose strong password
- `MONGO_PASSWORD`: Choose strong password
- `REDIS_PASSWORD`: Choose strong password
- `FHIR_CLIENT_ID`: Epic sandbox client ID (see below)
- `FHIR_CLIENT_SECRET`: Epic sandbox client secret

### 5. Register for Epic Sandbox (FHIR Access)

1. Go to: https://fhir.epic.com/Developer/Apps
2. Create account
3. Register new app:
   - **App Name:** MediMind MCP Dev
   - **Redirect URI:** `http://localhost:8000/auth/fhir/callback`
   - **FHIR Version:** R4
   - **Scopes:** `patient/*.read`, `user/*.read`
4. Copy Client ID and Client Secret to `.env`

### 6. Start Infrastructure

```powershell
# Start PostgreSQL, MongoDB, Redis
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 7. Initialize Database

```powershell
cd mcp-server

# Initialize Alembic
alembic init migrations

# Generate initial migration
alembic revision --autogenerate -m "Initial HIPAA-compliant schema"

# Apply migration
alembic upgrade head
```

### 8. Start FastAPI Server

```powershell
# Development mode (with auto-reload)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode (no reload, optimized)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 9. Test Health Check

```powershell
# Using curl
curl http://localhost:8000/health

# Using PowerShell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "hipaa_compliant": false
}
```

---

## 📁 Project Structure

```
medimind-mcp/
├── mcp-server/                 # FastAPI backend
│   ├── src/
│   │   ├── main.py            # FastAPI app (audit middleware)
│   │   ├── settings.py        # Configuration (HIPAA defaults)
│   │   ├── fhir/
│   │   │   └── client.py      # FHIR R4 + SMART on FHIR OAuth
│   │   ├── security/
│   │   │   ├── encryption.py  # AES-256 encryption
│   │   │   ├── audit.py       # Immutable audit logs
│   │   │   └── deidentify.py  # PHI removal (Presidio)
│   │   ├── db/
│   │   │   └── models.py      # SQLAlchemy (encrypted PHI)
│   │   ├── tools/             # Clinical decision support
│   │   └── ai/                # BioGPT, scispaCy
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── clinical_validation/
│   └── requirements.txt
├── compliance/
│   ├── HIPAA_CHECKLIST.md     # ✅ Track compliance
│   ├── BAA_TEMPLATE.md        # Business Associate Agreement
│   ├── BREACH_RESPONSE.md     # Incident response plan
│   └── SECURITY_AUDIT.md      # Security audit procedures
├── docker-compose.yml         # HIPAA-compliant dev environment
└── .gitignore                 # NEVER commit secrets!
```

---

## 🔒 Security Features

### Encryption
- **At Rest:** AES-256 (Fernet) for all PHI fields
- **In Transit:** TLS 1.3+ (HTTPS only)
- **Database:** PostgreSQL SSL, MongoDB TLS

### Audit Logging
- Every PHI access logged (HIPAA §164.312(b))
- Immutable logs (no DELETE/UPDATE)
- 7-year retention (2555 days)
- User, IP, action, resource tracked

### Authentication
- SMART on FHIR OAuth 2.0
- JWT with 15-minute expiration
- TODO: Multi-factor authentication (MFA)

### De-Identification
- Microsoft Presidio (NER-based)
- HIPAA Safe Harbor (18 identifiers)
- Use for ML training, exports, logs

---

## 🧪 Testing

```powershell
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Security scan
bandit -r src/

# Type checking
mypy src/

# Code formatting
black src/
```

---

## 📊 HIPAA Compliance Status

**Phase 1 (Current):** 45% Complete

- ✅ PHI encryption at rest (AES-256)
- ✅ Audit logging (immutable)
- ✅ De-identification (Presidio)
- ✅ TLS in transit
- ✅ Session timeout (15 minutes)
- ⏳ MFA (pending)
- ⏳ BAAs with vendors (pending)
- ⏳ Risk assessment (pending)

See `compliance/HIPAA_CHECKLIST.md` for full checklist.

---

## 🔑 API Endpoints

### Health Check
```http
GET /health
```

### Authentication (SMART on FHIR)
```http
GET /auth/fhir/authorize
GET /auth/fhir/callback?code=...
```

### Patients
```http
GET /api/v1/patients/{patient_id}
GET /api/v1/patients/{patient_id}/observations
GET /api/v1/patients/{patient_id}/medications
GET /api/v1/patients/{patient_id}/allergies
```

**⚠️ All endpoints require authentication and audit PHI access.**

---

## 📝 Development Workflow

1. **Feature Branch:**
   ```powershell
   git checkout -b feature/drug-interaction-checker
   ```

2. **Implement Feature:**
   - Write code in `src/`
   - Add unit tests in `tests/unit/`
   - Update `HIPAA_CHECKLIST.md` if security-related

3. **Test:**
   ```powershell
   pytest tests/ -v
   bandit -r src/
   ```

4. **Commit (NO SECRETS!):**
   ```powershell
   git add .
   git commit -m "feat: Add drug interaction checker"
   ```

5. **Push & PR:**
   ```powershell
   git push origin feature/drug-interaction-checker
   ```

---

## 🚨 Incident Response

**If you suspect a breach:**

1. **STOP** - Immediately halt system access
2. **NOTIFY** - Email: security@hospital.com
3. **DOCUMENT** - Record all details
4. **FOLLOW** - See `compliance/BREACH_RESPONSE.md`

**Timeline:**
- Discovery to Assessment: 24 hours
- Notification to HHS: 60 days max

---

## 📚 Resources

### HIPAA Compliance
- [HHS HIPAA Portal](https://www.hhs.gov/hipaa)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [HITRUST CSF](https://hitrustalliance.net/)

### FHIR & EHR Integration
- [FHIR R4 Specification](https://hl7.org/fhir/R4/)
- [SMART on FHIR](https://docs.smarthealthit.org/)
- [Epic FHIR Documentation](https://fhir.epic.com/)

### Healthcare AI
- [BioGPT Paper](https://arxiv.org/abs/2210.10341)
- [scispaCy Documentation](https://allenai.github.io/scispacy/)
- [Clinical NLP Resources](https://github.com/Georgetown-IR-Lab/Clinical-NLP)

---

## ⚖️ Legal & Compliance

### Medical Disclaimer
> This product is intended to assist, not replace, clinical judgment. All treatment decisions remain the responsibility of licensed healthcare providers. MediMind is not a medical device and does not diagnose or treat medical conditions.

### FDA Disclaimer
> Clinical Decision Support (CDS) software is generally exempt from FDA regulation if:
> 1. Clinician can independently review basis of recommendation
> 2. Not intended to replace clinical judgment
> 3. Does not acquire/analyze data from medical devices

### HIPAA Disclaimer
> This system handles Protected Health Information (PHI). Any breach must be reported to patients and HHS within 60 days. Penalties: $100-$50,000 per violation, criminal charges possible.

---

## 👥 Team & Support

**HIPAA Security Officer:** TBD  
**Technical Lead:** TBD  
**Clinical Advisory Board:** TBD

**Support Email:** support@medimind.hospital.com  
**Security Email:** security@medimind.hospital.com  
**Emergency Hotline:** +1-XXX-XXX-XXXX

---

## 📄 License

**Proprietary - All Rights Reserved**

Copyright © 2025 MediMind Health Technologies

This software is confidential and proprietary. Unauthorized copying, distribution, or use is strictly prohibited.

---

**Let's build a system that saves lives while protecting patient privacy. 🏥💙**
