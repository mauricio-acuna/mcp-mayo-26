# MediMind MCP - Healthcare Clinical Decision Support

**Tagline:** "AI-Powered Clinical Intelligence at the Point of Care"

## Overview

MediMind MCP is a HIPAA-compliant Model Context Protocol server that assists clinicians with differential diagnosis, drug interaction checking, clinical evidence search, and automated documentation. Integrates with Epic, Cerner, and other EHR systems via FHIR.

## Key Features

- 🏥 **EHR Integration**: Epic, Cerner via FHIR R4 and HL7 v2
- 💊 **Drug Safety**: Real-time interaction checking with DrugBank
- 🔬 **Differential Diagnosis**: AI-powered analysis with BioGPT
- 📚 **Evidence Search**: PubMed, UpToDate, clinical guidelines
- 📋 **Auto-Documentation**: SOAP note generation from encounters
- 🔒 **HIPAA Compliant**: AES-256 encryption, audit logging, SOC 2

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (encrypted)
- MongoDB
- Redis 7

### Installation

```bash
# Clone repository
git clone https://github.com/company/medimind-mcp.git
cd medimind-mcp

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r mcp-server/requirements.txt

# Setup environment (HIPAA-compliant!)
cp .env.example .env
# CRITICAL: Add encryption keys, FHIR credentials

# Start infrastructure
docker-compose up -d postgres mongodb redis

# Run migrations
cd mcp-server
alembic upgrade head

# Download AI models
python scripts/download_models.py

# Start server
python src/main.py
```

Server running at `http://localhost:8000`  
API docs (dev only): `http://localhost:8000/api/docs`

### Configure Claude Desktop

```json
{
  "mcpServers": {
    "medimind": {
      "command": "medimind",
      "args": ["serve"],
      "env": {
        "MEDIMIND_API_KEY": "mm_xxx",
        "FHIR_ENDPOINT": "https://hospital.epic.com/fhir/r4"
      }
    }
  }
}
```

## Usage Examples

### Emergency Department - Chest Pain

```
Dr. Lee: "Male 58yo, chest pain × 2h, diaphoresis. What's the HEART score?"

MediMind:
→ HEART Score: 7/10 🔴 HIGH RISK
  2-week MACE risk: 50-65%
  Recommendation: Admit to cardiology
  Activate STEMI protocol
```

### Drug Interaction Check

```
Dr. Martinez: "Patient on warfarin, metoprolol, lisinopril. Can I prescribe nitrofurantoin for UTI?"

MediMind:
→ 🔴 CONTRAINDICATED
  Reasons:
  1. Renal impairment (CrCl 35 ml/min)
  2. CHF exacerbation risk
  
  Alternative: Cephalexin 500mg QID × 7 days
```

### Auto-Documentation

```
Dr. Chen: "Generate progress note for patient post-op day 2 hip replacement"

MediMind:
→ [Generates complete SOAP note]
  S: Patient reports pain 3/10...
  O: Vitals stable, wound c/d/i...
  A/P: 1. S/P hip arthroplasty POD#2...
  
  [Auto-populated ICD-10, CPT codes]
```

## Documentation

- [Full PRD](./PRD.md) - Complete product requirements
- [FHIR Integration](./docs/fhir-integration.md) - EHR connectivity
- [HIPAA Compliance](./docs/hipaa-compliance.md) - Security measures
- [Clinical Validation](./docs/clinical-validation.md) - Accuracy testing
- [Deployment Guide](./docs/deployment.md) - Hospital setup

## Project Structure

```
medimind-mcp/
├── mcp-server/          # Python FastAPI server
│   ├── src/
│   │   ├── fhir/        # FHIR client
│   │   ├── ai/          # Diagnostic models
│   │   ├── security/    # HIPAA compliance
│   │   └── tools/       # MCP tools
│   └── tests/
├── compliance/          # HIPAA documentation
├── infra/               # AWS HIPAA-compliant deployment
└── scripts/             # Clinical validation scripts
```

## Development

```bash
# Run tests
pytest tests/

# Clinical validation
python scripts/clinical_case_validation.py

# HIPAA audit
python scripts/hipaa_audit.py --full

# Type checking
mypy src/

# Security scan
bandit -r src/
```

## Security & Compliance

- ✅ **HIPAA**: Encryption (AES-256), audit logging, BAAs
- ✅ **SOC 2 Type II**: In progress (Month 18 target)
- ✅ **HITRUST**: Planned (Month 24)
- ✅ **Breach Notification**: Incident response plan in place

## Pricing

- **Per Physician**: $200/mo (1-10), $150/mo (11-50), $100/mo (51+)
- **Per Bed**: $8K/mo (<200 beds), $15K/mo (200-400), $25K/mo (400+)
- **Implementation**: $25K standard, $50-100K complex
- **Specialty Modules**: $2-5K/mo (Cardiology, Oncology, Pediatrics)

## Support

- 📧 Email: support@medimind.ai
- 📞 Phone: 1-800-MEDIMIND (24/7 for production issues)
- 💬 Slack: Enterprise customers only
- 📚 Docs: https://docs.medimind.ai
- 🐛 Issues: security@medimind.ai (for security concerns)

## License

Commercial - Proprietary. Contact sales@medimind.ai for licensing.

## Regulatory Status

- **FDA**: Clinical Decision Support (CDS) - Generally exempt
- **HIPAA**: Fully compliant, BAAs available
- **SOC 2**: Type II in progress (expected Q2 2026)

## Roadmap

See [PRD.md](./PRD.md) for complete 24-week development + certification roadmap.

**Year 1 Target**: $840K ARR (7 hospitals)  
**Year 2 Target**: $3.24M ARR (18 hospitals)

---

**⚠️ IMPORTANT DISCLAIMER**

This product is intended to assist, not replace, clinical judgment. All treatment decisions remain the responsibility of licensed healthcare providers. MediMind is not a medical device and does not diagnose or treat medical conditions.
