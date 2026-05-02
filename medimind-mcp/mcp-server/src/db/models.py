"""
HIPAA-Compliant Database Models

⚠️ SECURITY CRITICAL: All PHI fields are encrypted at rest.

Models:
- Patient: Patient demographics (all PHI encrypted)
- AuditLog: Immutable audit trail (HIPAA requirement)
- Encounter: Clinical encounters
- Observation: Lab results, vitals (linked to FHIR)
- Medication: Medication orders
- Allergy: Allergy/intolerance records

HIPAA Compliance:
- All PHI encrypted at rest (§164.312(a)(2)(iv))
- Audit logs immutable (no UPDATE/DELETE)
- Foreign keys maintain referential integrity
- Timestamps for created/updated tracking
"""

from sqlalchemy import (
    Column, String, DateTime, Boolean, JSON, Text,
    ForeignKey, Integer, Float, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from typing import Optional
import uuid
import enum

Base = declarative_base()


class Patient(Base):
    """
    Patient demographics (HIPAA-sensitive).
    
    All PHI fields are encrypted at rest using AES-256.
    Access to this table MUST be audited.
    """
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mrn = Column(String, unique=True, nullable=False, index=True)  # Medical Record Number
    fhir_id = Column(String, unique=True, index=True)  # FHIR Patient ID
    
    # ==========================================
    # ENCRYPTED PHI FIELDS
    # ⚠️ All values encrypted with AES-256
    # ==========================================
    first_name_encrypted = Column(Text, nullable=False)
    last_name_encrypted = Column(Text, nullable=False)
    dob_encrypted = Column(Text, nullable=False)  # Date of birth
    ssn_encrypted = Column(Text)                 # Social Security Number
    email_encrypted = Column(Text)
    phone_encrypted = Column(Text)
    address_encrypted = Column(Text)
    
    # ==========================================
    # Non-PHI Metadata (not encrypted)
    # ==========================================
    gender = Column(String(10))  # M, F, Other, Unknown
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    observations = relationship("Observation", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")
    allergies = relationship("Allergy", back_populates="patient")
    
    def __repr__(self):
        # ⚠️ NEVER expose PHI in repr!
        return f"<Patient(mrn={self.mrn}, active={self.is_active})>"


class AuditLog(Base):
    """
    Immutable audit log (HIPAA requirement).
    
    Every PHI access MUST be logged per §164.312(b).
    
    ⚠️ CRITICAL: This table is IMMUTABLE:
    - No UPDATE statements allowed
    - No DELETE statements allowed
    - Retained for minimum 7 years (2555 days)
    """
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Who accessed what
    user_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)  # READ, CREATE, UPDATE, DELETE, EXPORT
    resource_type = Column(String, nullable=False)  # Patient, Observation, etc.
    resource_id = Column(String, nullable=False)
    
    # Where and how
    ip_address = Column(String, nullable=False)
    user_agent = Column(Text)
    
    # PHI access flag (for breach investigation)
    phi_accessed = Column(Boolean, default=False, index=True)
    
    # Additional context (JSON)
    context = Column(JSON, default={})
    
    def __repr__(self):
        return f"<AuditLog({self.action} {self.resource_type}/{self.resource_id} by {self.user_id})>"


class EncounterType(str, enum.Enum):
    """Encounter types (standardized)."""
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"
    EMERGENCY = "emergency"
    VIRTUAL = "virtual"
    HOME_HEALTH = "home_health"


class EncounterStatus(str, enum.Enum):
    """Encounter status (FHIR-compliant)."""
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Encounter(Base):
    """
    Clinical encounter (visit).
    
    Links to FHIR Encounter resource.
    """
    __tablename__ = "encounters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    fhir_id = Column(String, unique=True, index=True)
    
    encounter_type = Column(SQLEnum(EncounterType), nullable=False)
    status = Column(SQLEnum(EncounterStatus), nullable=False, default=EncounterStatus.PLANNED)
    
    # Encrypted fields
    chief_complaint_encrypted = Column(Text)  # "Chest pain"
    diagnosis_encrypted = Column(Text)        # ICD-10 codes encrypted
    
    # Timestamps
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    observations = relationship("Observation", back_populates="encounter")
    
    def __repr__(self):
        return f"<Encounter({self.encounter_type}, {self.status})>"


class Observation(Base):
    """
    Clinical observations (vitals, labs, imaging).
    
    Maps to FHIR Observation resource.
    """
    __tablename__ = "observations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    encounter_id = Column(String, ForeignKey("encounters.id"), index=True)
    fhir_id = Column(String, unique=True, index=True)
    
    # LOINC code (standardized observation codes)
    loinc_code = Column(String, index=True)  # e.g., "8480-6" for systolic BP
    display_name = Column(String)            # "Systolic Blood Pressure"
    
    # Value (not encrypted - clinical data, not PHI)
    value_quantity = Column(Float)
    value_unit = Column(String)
    value_string = Column(Text)
    
    # Reference ranges
    reference_low = Column(Float)
    reference_high = Column(Float)
    
    # Interpretation (normal, high, low, critical)
    interpretation = Column(String)
    
    # When observed
    effective_datetime = Column(DateTime, nullable=False, index=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    patient = relationship("Patient", back_populates="observations")
    encounter = relationship("Encounter", back_populates="observations")
    
    def __repr__(self):
        return f"<Observation({self.display_name}: {self.value_quantity} {self.value_unit})>"


class Medication(Base):
    """
    Medication orders/prescriptions.
    
    Maps to FHIR MedicationRequest resource.
    """
    __tablename__ = "medications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    fhir_id = Column(String, unique=True, index=True)
    
    # RxNorm code (standardized drug codes)
    rxnorm_code = Column(String, index=True)
    medication_name = Column(String, nullable=False)  # "Lisinopril 10mg"
    
    # Dosage (not encrypted - clinical data)
    dosage = Column(String)
    route = Column(String)      # "Oral", "IV", etc.
    frequency = Column(String)  # "Twice daily"
    
    # Status
    status = Column(String)  # active, completed, stopped
    
    # Dates
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationships
    patient = relationship("Patient", back_populates="medications")
    
    def __repr__(self):
        return f"<Medication({self.medication_name}, {self.status})>"


class AllergySeverity(str, enum.Enum):
    """Allergy severity levels."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life-threatening"


class Allergy(Base):
    """
    Allergy and intolerance records.
    
    Maps to FHIR AllergyIntolerance resource.
    """
    __tablename__ = "allergies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    fhir_id = Column(String, unique=True, index=True)
    
    # Allergen
    allergen_code = Column(String)  # SNOMED CT code
    allergen_name = Column(String, nullable=False)  # "Penicillin"
    
    # Severity and reaction
    severity = Column(SQLEnum(AllergySeverity))
    reaction = Column(Text)  # "Hives, difficulty breathing"
    
    # Status
    is_active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    
    # Dates
    onset_date = Column(DateTime)
    recorded_date = Column(DateTime, default=lambda: datetime.now(UTC))
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationships
    patient = relationship("Patient", back_populates="allergies")
    
    def __repr__(self):
        return f"<Allergy({self.allergen_name}, {self.severity})>"


# ==========================================
# Database Helper Functions
# ==========================================

def get_encrypted_field(obj: Base, field_name: str) -> Optional[str]:
    """
    Decrypt and return PHI field value.
    
    ⚠️ AUDIT THIS ACCESS!
    
    Args:
        obj: Database model instance
        field_name: Name of encrypted field (without _encrypted suffix)
        
    Returns:
        Decrypted value or None
    """
    from src.security.encryption import encryption_service
    
    encrypted_field = f"{field_name}_encrypted"
    ciphertext = getattr(obj, encrypted_field, None)
    
    if not ciphertext:
        return None
    
    try:
        return encryption_service.decrypt(ciphertext)
    except Exception as e:
        import logging
        logging.error(f"Failed to decrypt {field_name}: {e}")
        return None


def set_encrypted_field(obj: Base, field_name: str, plaintext: str):
    """
    Encrypt and set PHI field value.
    
    Args:
        obj: Database model instance
        field_name: Name of field (without _encrypted suffix)
        plaintext: Plain text value to encrypt
    """
    from src.security.encryption import encryption_service
    
    encrypted_field = f"{field_name}_encrypted"
    
    if plaintext:
        ciphertext = encryption_service.encrypt(plaintext)
        setattr(obj, encrypted_field, ciphertext)
    else:
        setattr(obj, encrypted_field, None)
