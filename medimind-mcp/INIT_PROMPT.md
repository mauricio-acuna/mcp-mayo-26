# 🚀 MediMind MCP - Initial Setup Prompt for Claude Sonnet 4.5

Copy and paste this entire prompt to Claude Sonnet 4.5 to initialize the project:

---

## Context

You are an expert **healthcare software engineer** and **clinical informatics specialist** with deep knowledge of:
- **Healthcare Standards**: FHIR R4, HL7 v2, DICOM, ICD-10, CPT, LOINC, SNOMED CT
- **Compliance**: HIPAA, SOC 2, HITRUST, FDA regulations for medical software
- **Technology**: Python 3.11+, FastAPI, healthcare ML models (BioGPT, scispaCy)
- **Security**: AES-256 encryption, PHI de-identification, audit logging

I need you to help me build **MediMind MCP** - a HIPAA-compliant clinical decision support system that integrates with EHRs (Epic, Cerner) and assists physicians with diagnosis, drug safety, and documentation.

## Project Overview

**Product**: MediMind MCP - AI-Powered Clinical Intelligence  
**Tech Stack**: 
- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Database**: PostgreSQL 16 (encrypted), MongoDB (clinical notes), Redis
- **Healthcare APIs**: FHIR R4, HL7 v2, SMART on FHIR OAuth
- **AI Models**: BioGPT (diagnosis), scispaCy (NER), XGBoost (risk prediction)
- **Compliance**: HIPAA, SOC 2 Type II (in progress), encryption everywhere

**⚠️ CRITICAL**: This system handles **PHI (Protected Health Information)**. Every design decision must prioritize patient privacy and HIPAA compliance.

## What I Need You To Do

I have the complete PRD (Product Requirements Document) in `PRD.md` which contains:
- HIPAA-compliant architecture
- FHIR R4 client implementation
- Drug interaction checker (DrugBank integration)
- Database schema with encryption
- Clinical validation testing framework
- Security and compliance checklists

**Your mission**: Help me build this HIPAA-compliant system incrementally, with security and clinical safety as top priorities.

## Phase 1: HIPAA-Compliant Foundation (START HERE)

### 1. Project Structure Setup

Create the structure from `PRD.md`:
```
medimind-mcp/
├── mcp-server/
│   ├── src/
│   │   ├── main.py              # FastAPI app with HIPAA audit
│   │   ├── settings.py          # Pydantic settings (all secrets here)
│   │   ├── fhir/
│   │   │   └── client.py        # FHIR R4 + SMART on FHIR OAuth
│   │   ├── tools/
│   │   │   ├── patient_context.py
│   │   │   ├── differential_diagnosis.py
│   │   │   ├── drug_interactions.py
│   │   │   └── clinical_scores.py
│   │   ├── ai/
│   │   │   ├── biogpt.py        # Diagnostic AI
│   │   │   └── scispacy_ner.py  # Named entity recognition
│   │   ├── security/
│   │   │   ├── encryption.py    # AES-256 + KMS
│   │   │   ├── audit.py         # Immutable audit logs
│   │   │   └── deidentify.py    # PHI removal (Presidio)
│   │   └── db/
│   │       ├── models.py        # SQLAlchemy models
│   │       └── migrations/      # Alembic
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── clinical_validation/ # 100+ test cases
│   └── requirements.txt
├── compliance/
│   ├── HIPAA_CHECKLIST.md
│   ├── BAA_TEMPLATE.md          # Business Associate Agreement
│   ├── BREACH_RESPONSE.md
│   └── SECURITY_AUDIT.md
├── infra/                       # AWS HIPAA-compliant
└── docker-compose.yml
```

### 2. Core Dependencies

**requirements.txt** (Python 3.11+):
```python
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Healthcare Standards
fhir.resources==7.1.0            # FHIR R4 models
hl7apy==1.3.5                    # HL7 v2 parser
pydicom==2.4.3                   # DICOM imaging

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9           # PostgreSQL
motor==3.3.2                     # MongoDB async
redis==5.0.1

# Security & Encryption
cryptography==41.0.7             # AES-256
python-jose[cryptography]==3.3.0 # JWT
passlib[bcrypt]==1.7.4
presidio-analyzer==2.2.33        # PHI de-identification
presidio-anonymizer==2.2.33

# AI/ML
transformers==4.35.0             # BioGPT
spacy==3.7.2
scispacy==0.5.3                  # Medical NER
torch==2.1.0
xgboost==2.0.2

# HTTP Clients
httpx==0.25.2                    # Async HTTP (for FHIR)
aiohttp==3.9.1

# Utilities
python-dotenv==1.0.0
pydantic-settings==2.1.0
```

### 3. Settings & Configuration (CRITICAL)

**src/settings.py** (from PRD):
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Database (ENCRYPTED!)
    DATABASE_URL: str  # postgresql://user:pass@host:5432/medimind?sslmode=require
    MONGODB_URL: str
    REDIS_URL: str
    
    # FHIR Server (Epic/Cerner)
    FHIR_BASE_URL: str
    FHIR_CLIENT_ID: str
    FHIR_CLIENT_SECRET: str
    FHIR_REDIRECT_URI: str = "http://localhost:8000/auth/fhir/callback"
    
    # External APIs
    PUBMED_API_KEY: str
    DRUGBANK_API_KEY: str
    UPTODATE_API_KEY: Optional[str] = None
    
    # Security (NEVER COMMIT THESE!)
    ENCRYPTION_KEY: str  # openssl rand -base64 32
    SECRET_KEY: str      # For JWT signing
    AWS_KMS_KEY_ID: Optional[str] = None  # Production: Use KMS
    
    # HIPAA Compliance
    PHI_ENCRYPTION_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years (HIPAA requirement)
    SESSION_TIMEOUT_MINUTES: int = 15
    BREACH_NOTIFICATION_EMAIL: str
    
    # AI Models
    MODEL_PATH: str = "/models"
    BIOGPT_MODEL: str = "microsoft/biogpt"
    SCISPACY_MODEL: str = "en_core_sci_lg"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 4. FHIR Client Implementation

**src/fhir/client.py** (complete code in PRD):
- SMART on FHIR OAuth 2.0 authentication
- Methods: get_patient(), search_observations(), get_medications(), get_allergies(), get_conditions()
- Token auto-renewal
- Error handling with retries

### 5. Security Layer (MANDATORY)

**src/security/encryption.py**:
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

class EncryptionService:
    def __init__(self, key: str):
        self.key = base64.urlsafe_b64decode(key)
        self.fernet = Fernet(base64.urlsafe_b64encode(self.key[:32]))
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt PHI data (AES-256)"""
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt PHI data"""
        return self.fernet.decrypt(ciphertext.encode()).decode()
```

**src/security/audit.py**:
```python
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.models import AuditLog

class AuditLogger:
    """HIPAA-compliant audit logging (immutable)"""
    
    @staticmethod
    async def log_access(
        db: Session,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        ip_address: str,
        user_agent: str,
        phi_accessed: bool = False
    ):
        """Log every PHI access (HIPAA requirement)"""
        audit_entry = AuditLog(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            phi_accessed=phi_accessed
        )
        db.add(audit_entry)
        await db.commit()
```

**src/security/deidentify.py** (PHI removal):
```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PHIDeIdentifier:
    """Remove PHI from text (for ML training, exports)"""
    
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
    
    def deidentify(self, text: str) -> str:
        """Remove 18 HIPAA identifiers"""
        # Detect PHI entities
        results = self.analyzer.analyze(
            text=text,
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", 
                     "US_SSN", "DATE_TIME", "LOCATION", "MEDICAL_LICENSE"],
            language="en"
        )
        
        # Anonymize
        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized.text
```

### 6. Drug Interaction Checker

**src/tools/drug_interactions.py**:
- DrugBank API integration
- Check drug-drug interactions
- Check drug-allergy interactions
- Check drug-condition contraindications
- Severity levels: Critical, Major, Moderate, Minor

### 7. Database Setup (Encrypted!)

**src/db/models.py** (SQLAlchemy):
```python
from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True)
    mrn = Column(String, unique=True, nullable=False)  # Medical Record Number
    
    # All PHI encrypted at rest
    first_name_encrypted = Column(Text, nullable=False)
    last_name_encrypted = Column(Text, nullable=False)
    dob_encrypted = Column(Text, nullable=False)
    ssn_encrypted = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    ip_address = Column(String)
    user_agent = Column(Text)
    phi_accessed = Column(Boolean, default=False)
    
    # Immutable: No updates or deletes allowed (HIPAA requirement)
```

**Initialize Alembic**:
```bash
cd mcp-server
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### 8. Docker Development Environment

**docker-compose.yml** (HIPAA-compliant):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: medimind
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: medimind
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    command: >
      postgres
      -c ssl=on
      -c ssl_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
      -c ssl_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
    # HIPAA: Encryption in transit (SSL)
    
  mongodb:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: medimind
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    ports:
      - "27017:27017"
    volumes:
      - mongodb-data:/data/db
    command: mongod --auth --tlsMode requireTLS --tlsCertificateKeyFile /etc/ssl/mongodb.pem
    
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"

volumes:
  postgres-data:
  mongodb-data:
```

## Critical Implementation Guidelines

### HIPAA Compliance Checklist

**Before writing ANY code, ensure**:
- [ ] All PHI encrypted at rest (AES-256)
- [ ] All connections use TLS 1.3+ (no HTTP, only HTTPS)
- [ ] Every PHI access logged (who, what, when, why)
- [ ] Audit logs immutable (no DELETE statements)
- [ ] Session timeout: 15 minutes idle
- [ ] Minimum necessary: Only fetch data required for specific task
- [ ] BAA (Business Associate Agreement) with all vendors
- [ ] Breach notification plan documented
- [ ] PHI de-identification for ML training
- [ ] Access controls: RBAC (physician, nurse, admin)

### Security Best Practices

1. **Never log PHI** (patient names, DOB, SSN, MRN in plain text)
2. **Parameterized queries only** (prevent SQL injection)
3. **Input validation** (Pydantic models for all inputs)
4. **Rate limiting** (prevent abuse)
5. **Fail closed** (deny access on error, don't fail open)

### Clinical Safety

- **Human in the loop**: AI suggests, clinician decides
- **Confidence scores**: Always show uncertainty
- **Citations**: Link to evidence (PubMed, guidelines)
- **Red flags**: Highlight critical conditions (sepsis, MI, stroke)
- **Disclaimers**: "Not intended to replace clinical judgment"

### Error Handling

**NEVER expose internal details to users**:
```python
try:
    patient = fhir_client.get_patient(patient_id)
except Exception as e:
    # ❌ DON'T: return {"error": str(e)}  # May leak PHI
    # ✅ DO:
    logger.error(f"FHIR error: {e}", extra={"patient_id": patient_id})
    return {"error": "Unable to retrieve patient data"}
```

## Testing Requirements

### Clinical Validation (MANDATORY)

Create `tests/clinical_validation/cases/`:
- 100+ test cases with gold standard diagnoses
- Test differential diagnosis accuracy (target: >90%)
- Test drug interaction detection (target: >95%)
- Test clinical score calculations (HEART, CHADS2, etc.)

**Example test case**:
```json
{
  "case_id": "001",
  "patient_age": 58,
  "patient_sex": "M",
  "presenting_symptoms": ["chest pain", "diaphoresis", "dyspnea"],
  "vitals": {"bp": "145/90", "hr": 88, "temp": 98.6},
  "labs": {"troponin": 0.12, "d_dimer": 450},
  "ecg": "ST elevation 2mm in V2-V4",
  "expected_diagnosis": "STEMI",
  "expected_heart_score": 7,
  "expected_action": "Activate STEMI protocol"
}
```

### Security Testing

- [ ] Penetration testing (hire 3rd party)
- [ ] SQL injection attempts (all parameterized?)
- [ ] XSS attempts (FastAPI escapes by default)
- [ ] Authentication bypass attempts
- [ ] Session hijacking tests
- [ ] Encryption validation (all PHI encrypted?)

## Development Workflow

```bash
# 1. Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Generate encryption key (SAVE THIS SECURELY!)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 3. Setup .env file
cp .env.example .env
# Add encryption key, FHIR credentials, etc.

# 4. Start infrastructure
docker-compose up -d

# 5. Run migrations
alembic upgrade head

# 6. Download AI models
python scripts/download_models.py

# 7. Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 8. Run tests
pytest tests/ -v --cov=src

# 9. HIPAA audit
python scripts/hipaa_audit.py --full
```

## Incremental Deliverables

Build in this order:
1. ✅ **Sprint 1-2** (Weeks 1-2): HIPAA foundation (encryption, audit, FHIR)
2. ⏳ **Sprint 3-4** (Weeks 3-4): Drug interaction checker + clinical scores
3. ⏳ **Sprint 5-6** (Weeks 5-6): Differential diagnosis AI (BioGPT)
4. ⏳ **Sprint 7-8** (Weeks 7-8): Clinical documentation (SOAP notes)

## Questions You Should Ask Me

Before generating code, please ask:

1. **EHR Access**: Do I have Epic/Cerner FHIR credentials? (Sandbox or production?)
2. **Encryption Keys**: Should I generate new encryption keys or do I have existing ones?
3. **Compliance Stage**: Development only, or preparing for pilot hospital?
4. **API Keys**: Do I have DrugBank, PubMed, UpToDate API keys?
5. **Deployment**: On-premise (hospital data center) or AWS (HIPAA-compliant)?
6. **Clinical Validation**: Do I have access to de-identified test cases?
7. **BAA Status**: Do I need Business Associate Agreements with vendors yet?

## Success Criteria for Phase 1

Phase 1 is complete when:
- [ ] FastAPI server starts with HIPAA audit middleware
- [ ] All PHI encrypted at rest (verified)
- [ ] FHIR client authenticates with Epic sandbox
- [ ] Audit log records every PHI access
- [ ] Drug interaction checker returns results
- [ ] De-identification removes PHI from text
- [ ] Unit tests pass with >80% coverage
- [ ] Security scan passes (Bandit)
- [ ] HIPAA checklist 100% complete

## After Phase 1

Next steps:
- BioGPT diagnostic AI integration
- Clinical score calculators (HEART, CHADS2, Wells)
- Automated SOAP note generation
- Hospital pilot deployment
- SOC 2 Type II certification
- Clinical validation study (IRB approval)

## Critical Disclaimers

**⚠️ MEDICAL DISCLAIMER**:
> This product is intended to assist, not replace, clinical judgment. All treatment decisions remain the responsibility of licensed healthcare providers. MediMind is not a medical device and does not diagnose or treat medical conditions.

**⚠️ FDA DISCLAIMER**:
> Current regulatory stance: Clinical Decision Support (CDS) software is generally exempt from FDA regulation if:
> 1. Clinician can independently review basis of recommendation
> 2. Not intended to replace clinical judgment
> 3. Does not acquire/analyze data from medical devices
> 
> If FDA disagrees, we will pursue 510(k) clearance.

**⚠️ HIPAA DISCLAIMER**:
> This system handles Protected Health Information (PHI). Any breach must be reported to patients and HHS within 60 days. Penalties: $100-$50,000 per violation, criminal charges possible.

## Your Response Format

Please respond with:
1. **Confirmation**: You understand this is a **HIPAA-compliant healthcare system**
2. **Security Acknowledgment**: Confirm you'll prioritize PHI protection
3. **Clarifying Questions**: Ask me the 7 questions above
4. **Compliance Strategy**: How you'll ensure HIPAA compliance
5. **First Deliverables**: Exactly what you'll generate first

---

**START IMPLEMENTATION**: After I answer your questions, begin with settings.py and the encryption layer. Security comes FIRST.

## Additional Context

This is a **$3.24M ARR target** product for hospitals and clinics. **Patient safety** and **compliance** are non-negotiable. One breach can bankrupt the company.

**Target Customers**: Community hospitals (100-400 beds), specialty clinics, hospital networks  
**Business Model**: $100-200/physician/month, $8-25K/month per hospital  
**Regulatory**: HIPAA (mandatory), SOC 2 (Month 18), HITRUST (Month 24), FDA (TBD)

**Sales Cycle**: 6-12 months (hospital procurement is slow)  
**Competitive Edge**: AI-native, FHIR integration, <2s response time

Let's build a system that saves lives while protecting patient privacy. Ready to start?
