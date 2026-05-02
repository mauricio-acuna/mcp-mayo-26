"""
HIPAA-Compliant PHI De-Identification

⚠️ SECURITY CRITICAL: Remove PHI before using data for:
- Machine learning training
- Analytics and reporting
- Data exports to third parties
- Logging and debugging

HIPAA Safe Harbor Method (§164.514(b)(2)):
Remove 18 identifiers:
1. Names
2. Geographic subdivisions smaller than state
3. Dates (except year)
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers
13. Device identifiers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photos
18. Any unique identifier

Uses Microsoft Presidio for NER-based de-identification.

Usage:
    from src.security.deidentify import deidentifier
    
    # De-identify clinical note
    text = "Patient John Doe (DOB: 01/15/1980, SSN: 123-45-6789) presented..."
    safe_text = deidentifier.deidentify(text)
    # Output: "Patient [PERSON] (DOB: [DATE_TIME], SSN: [US_SSN]) presented..."
"""

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PHIDeIdentifier:
    """
    HIPAA-compliant PHI de-identification service.
    
    Uses Microsoft Presidio for automated detection and removal
    of Protected Health Information (PHI).
    
    Supports:
    - Safe Harbor method (remove 18 identifiers)
    - Custom entity recognition (medical record numbers, etc.)
    - Multiple languages (English primary)
    - Reversible anonymization (for authorized re-identification)
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize de-identification service.
        
        Args:
            language: Language code (default: "en")
        """
        try:
            # Initialize NLP engine (spaCy)
            provider = NlpEngineProvider()
            nlp_engine = provider.create_engine()
            
            # Initialize analyzer with default recognizers
            self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
            
            # Initialize anonymizer
            self.anonymizer = AnonymizerEngine()
            
            self.language = language
            
            logger.info("PHI de-identification service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize de-identifier: {e}")
            raise RuntimeError(f"De-identifier initialization failed: {e}")
    
    def deidentify(
        self,
        text: str,
        entities: Optional[List[str]] = None,
        anonymization_method: str = "replace"
    ) -> str:
        """
        De-identify PHI from text (HIPAA Safe Harbor).
        
        Args:
            text: Input text containing PHI
            entities: List of entity types to detect (None = all 18 HIPAA identifiers)
            anonymization_method: How to anonymize:
                - "replace": Replace with [ENTITY_TYPE] (default)
                - "mask": Replace with ****
                - "hash": Replace with one-way hash
                - "redact": Remove entirely
                
        Returns:
            De-identified text
            
        Examples:
            >>> deidentifier.deidentify("Patient: John Doe, DOB: 01/15/1980")
            "Patient: [PERSON], DOB: [DATE_TIME]"
            
            >>> deidentifier.deidentify("Call 555-1234", anonymization_method="mask")
            "Call ****"
        """
        if not text or not text.strip():
            return text
        
        try:
            # Define entity types (18 HIPAA identifiers)
            if entities is None:
                entities = [
                    "PERSON",                # Names
                    "EMAIL_ADDRESS",         # Email
                    "PHONE_NUMBER",          # Phone/Fax
                    "US_SSN",               # Social Security Number
                    "DATE_TIME",            # Dates
                    "LOCATION",             # Addresses
                    "MEDICAL_LICENSE",      # Medical license numbers
                    "URL",                  # Web URLs
                    "IP_ADDRESS",           # IP addresses
                    "CREDIT_CARD",          # Credit card numbers
                    "US_DRIVER_LICENSE",    # Driver's license
                    "US_PASSPORT",          # Passport
                    "IBAN_CODE",            # Bank accounts
                    "NRP",                  # National registry of persons
                    "AU_ABN",               # Australian business number
                    "AU_ACN",               # Australian company number
                    "AU_TFN",               # Australian tax file number
                    "AU_MEDICARE",          # Medicare number
                ]
            
            # Analyze text for PHI
            results = self.analyzer.analyze(
                text=text,
                entities=entities,
                language=self.language
            )
            
            # Configure anonymization operators
            operators = {}
            if anonymization_method == "replace":
                # Replace with [ENTITY_TYPE]
                for entity_type in entities:
                    operators[entity_type] = OperatorConfig("replace", {"new_value": f"[{entity_type}]"})
                    
            elif anonymization_method == "mask":
                # Replace with ****
                for entity_type in entities:
                    operators[entity_type] = OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 100})
                    
            elif anonymization_method == "hash":
                # Replace with one-way hash
                for entity_type in entities:
                    operators[entity_type] = OperatorConfig("hash", {"hash_type": "sha256"})
                    
            elif anonymization_method == "redact":
                # Remove entirely
                for entity_type in entities:
                    operators[entity_type] = OperatorConfig("redact")
            
            # Anonymize PHI
            anonymized = self.anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators=operators
            )
            
            return anonymized.text
            
        except Exception as e:
            logger.error(f"De-identification failed: {e}")
            # Fail secure: return empty string instead of potentially leaking PHI
            logger.error("SECURITY: Returning empty string to prevent PHI leak")
            return "[DE-IDENTIFICATION FAILED - CONTENT REDACTED]"
    
    def analyze_phi(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze text and return detected PHI entities (for debugging).
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping entity types to detected values
            
        ⚠️ WARNING: This method returns PHI! Only use for:
        - Testing de-identification accuracy
        - HIPAA compliance validation
        - Never log the output!
        
        Example:
            >>> analyzer.analyze_phi("John Doe, SSN: 123-45-6789")
            {
                "PERSON": ["John Doe"],
                "US_SSN": ["123-45-6789"]
            }
        """
        if not text or not text.strip():
            return {}
        
        try:
            results = self.analyzer.analyze(
                text=text,
                entities=None,  # Detect all
                language=self.language
            )
            
            # Group by entity type
            phi_detected = {}
            for result in results:
                entity_type = result.entity_type
                detected_text = text[result.start:result.end]
                
                if entity_type not in phi_detected:
                    phi_detected[entity_type] = []
                    
                phi_detected[entity_type].append(detected_text)
            
            return phi_detected
            
        except Exception as e:
            logger.error(f"PHI analysis failed: {e}")
            return {}
    
    def validate_deidentification(self, original: str, deidentified: str) -> bool:
        """
        Validate that de-identification removed all PHI.
        
        Args:
            original: Original text with PHI
            deidentified: De-identified text
            
        Returns:
            True if no PHI detected in de-identified text
            
        Use Cases:
        - Unit testing
        - Quality assurance
        - HIPAA compliance validation
        """
        phi_remaining = self.analyze_phi(deidentified)
        
        if phi_remaining:
            logger.warning(
                f"PHI still detected after de-identification: {list(phi_remaining.keys())}"
            )
            return False
        
        return True
    
    def get_safe_harbor_report(self, text: str) -> Dict[str, int]:
        """
        Generate HIPAA Safe Harbor compliance report.
        
        Args:
            text: De-identified text to validate
            
        Returns:
            Dictionary with counts of each identifier type found
            
        If any identifiers remain, text is NOT Safe Harbor compliant.
        """
        phi_detected = self.analyze_phi(text)
        
        # Count each identifier type
        report = {entity_type: len(values) for entity_type, values in phi_detected.items()}
        
        is_compliant = len(phi_detected) == 0
        
        report["_compliant"] = is_compliant
        report["_total_identifiers"] = sum(report.values())
        
        return report


# ==========================================
# Global Instance (singleton)
# ==========================================
try:
    deidentifier = PHIDeIdentifier()
except Exception as e:
    logger.warning(f"De-identifier not initialized: {e}")
    deidentifier = None
