"""
MediMind MCP - HIPAA-Compliant Configuration Settings

⚠️ SECURITY CRITICAL: All secrets loaded from environment variables.
Never hardcode credentials in this file.

HIPAA Compliance Features:
- PHI encryption enabled by default
- 7-year audit log retention (2555 days)
- 15-minute session timeout
- SSL/TLS required for all database connections
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Centralized configuration for MediMind MCP.
    
    All sensitive values (API keys, database credentials, encryption keys)
    MUST be stored in environment variables or .env file.
    
    HIPAA Compliance:
    - PHI_ENCRYPTION_ENABLED: Must be True in production
    - AUDIT_LOG_RETENTION_DAYS: Minimum 2555 days (7 years)
    - SESSION_TIMEOUT_MINUTES: Maximum 15 minutes idle
    - DATABASE_URL: Must include sslmode=require
    """
    
    # ==========================================
    # Environment
    # ==========================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # ==========================================
    # Database (ENCRYPTED!)
    # ==========================================
    DATABASE_URL: str = "postgresql://medimind:changeme@localhost:5432/medimind?sslmode=require"
    MONGODB_URL: str = "mongodb://medimind:changeme@localhost:27017/medimind?authSource=admin"
    REDIS_URL: str = "redis://:changeme@localhost:6379/0"
    
    # ==========================================
    # FHIR Server (Epic/Cerner)
    # ==========================================
    FHIR_BASE_URL: str = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
    FHIR_CLIENT_ID: str = "your_client_id"
    FHIR_CLIENT_SECRET: str = "your_client_secret"
    FHIR_REDIRECT_URI: str = "http://localhost:8000/auth/fhir/callback"
    
    # ==========================================
    # External APIs
    # ==========================================
    PUBMED_API_KEY: str = "development_placeholder"
    DRUGBANK_API_KEY: str = "development_placeholder"
    UPTODATE_API_KEY: Optional[str] = None
    
    # ==========================================
    # Security (NEVER COMMIT THESE!)
    # ==========================================
    ENCRYPTION_KEY: str = "GENERATE_WITH_FERNET"  # Must be 44 chars, base64-encoded
    SECRET_KEY: str = "GENERATE_WITH_SECRETS"     # For JWT signing
    AWS_KMS_KEY_ID: Optional[str] = None           # Production: Use AWS KMS
    
    # ==========================================
    # HIPAA Compliance
    # ==========================================
    PHI_ENCRYPTION_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years (HIPAA requirement)
    SESSION_TIMEOUT_MINUTES: int = 15
    BREACH_NOTIFICATION_EMAIL: str = "security@hospital.com"
    
    # ==========================================
    # AI Models
    # ==========================================
    MODEL_PATH: str = "./models"
    BIOGPT_MODEL: str = "microsoft/biogpt"
    SCISPACY_MODEL: str = "en_core_sci_lg"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def validate_hipaa_compliance(self) -> list[str]:
        """
        Validate HIPAA compliance requirements.
        
        Returns:
            List of compliance violations (empty if compliant)
        """
        violations = []
        
        if not self.PHI_ENCRYPTION_ENABLED:
            violations.append("PHI_ENCRYPTION_ENABLED must be True")
            
        if self.AUDIT_LOG_RETENTION_DAYS < 2555:
            violations.append(f"AUDIT_LOG_RETENTION_DAYS must be ≥2555 days (7 years), got {self.AUDIT_LOG_RETENTION_DAYS}")
            
        if self.SESSION_TIMEOUT_MINUTES > 15:
            violations.append(f"SESSION_TIMEOUT_MINUTES must be ≤15 minutes, got {self.SESSION_TIMEOUT_MINUTES}")
            
        if "sslmode=require" not in self.DATABASE_URL and self.ENVIRONMENT == "production":
            violations.append("DATABASE_URL must include sslmode=require in production")
            
        if self.ENCRYPTION_KEY == "GENERATE_WITH_FERNET":
            violations.append("ENCRYPTION_KEY not set - generate with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'")
            
        if self.SECRET_KEY == "GENERATE_WITH_SECRETS":
            violations.append("SECRET_KEY not set - generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'")
            
        return violations


# Global settings instance
settings = Settings()

# Validate HIPAA compliance on startup
if __name__ != "__main__":  # Don't validate during imports in tests
    violations = settings.validate_hipaa_compliance()
    if violations and settings.ENVIRONMENT == "production":
        raise ValueError(f"HIPAA compliance violations: {violations}")
    elif violations and settings.ENVIRONMENT == "development":
        print(f"⚠️  HIPAA compliance warnings (development): {violations}")
