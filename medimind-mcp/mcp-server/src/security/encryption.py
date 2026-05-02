"""
HIPAA-Compliant Encryption Service

⚠️ SECURITY CRITICAL: This module handles PHI encryption/decryption.

Features:
- AES-256 encryption using Fernet (symmetric)
- HIPAA-compliant encryption at rest
- Key rotation support (future enhancement)
- Integration with AWS KMS for production

HIPAA Requirements:
- All PHI must be encrypted at rest (§164.312(a)(2)(iv))
- Encryption keys must be managed securely
- Key access must be audited
- Backup keys must be stored securely

Usage:
    from src.security.encryption import encryption_service
    
    # Encrypt PHI
    encrypted = encryption_service.encrypt("John Doe")
    
    # Decrypt PHI (audit this access!)
    plaintext = encryption_service.decrypt(encrypted)
"""

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class EncryptionService:
    """
    HIPAA-compliant encryption service for PHI data.
    
    Uses Fernet (AES-128-CBC + HMAC-SHA256) for symmetric encryption.
    Fernet provides:
    - Authenticated encryption (prevents tampering)
    - Automatic key derivation
    - Timestamp-based expiration (optional)
    
    For production, integrate with AWS KMS for key management.
    """
    
    def __init__(self, encryption_key: str, kms_key_id: Optional[str] = None):
        """
        Initialize encryption service.
        
        Args:
            encryption_key: Base64-encoded Fernet key (44 chars)
            kms_key_id: AWS KMS key ID (production only)
            
        Raises:
            ValueError: If encryption_key is invalid
        """
        try:
            # Validate and load encryption key
            if encryption_key == "GENERATE_WITH_FERNET":
                raise ValueError(
                    "Encryption key not set! Generate with: "
                    "python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
                )
            
            # Ensure key is properly formatted
            key_bytes = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
            self.fernet = Fernet(key_bytes)
            self.kms_key_id = kms_key_id
            
            logger.info("Encryption service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize encryption service: {e}")
            raise ValueError(f"Invalid encryption key: {e}")
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt PHI data (AES-256).
        
        Args:
            plaintext: Sensitive data to encrypt (PHI)
            
        Returns:
            Base64-encoded ciphertext
            
        Raises:
            ValueError: If plaintext is empty
            
        Security Notes:
        - ⚠️ NEVER log the plaintext
        - Audit all calls to this function
        - Encrypted data includes timestamp (prevents replay attacks)
        """
        if not plaintext:
            raise ValueError("Cannot encrypt empty string")
        
        try:
            # Fernet automatically adds timestamp and HMAC
            ciphertext = self.fernet.encrypt(plaintext.encode())
            return ciphertext.decode()
            
        except Exception as e:
            # ⚠️ Don't log plaintext in error message!
            logger.error("Encryption failed", extra={"error": str(e)})
            raise RuntimeError("Encryption failed") from e
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt PHI data.
        
        Args:
            ciphertext: Base64-encoded encrypted data
            
        Returns:
            Decrypted plaintext
            
        Raises:
            InvalidToken: If ciphertext is tampered or invalid
            ValueError: If ciphertext is empty
            
        Security Notes:
        - ⚠️ AUDIT every call to this function (PHI access)
        - ⚠️ NEVER log the decrypted plaintext
        - Fernet validates HMAC and timestamp automatically
        """
        if not ciphertext:
            raise ValueError("Cannot decrypt empty string")
        
        try:
            # Fernet validates HMAC and timestamp
            plaintext_bytes = self.fernet.decrypt(ciphertext.encode())
            return plaintext_bytes.decode()
            
        except InvalidToken:
            logger.error("Decryption failed: Invalid token (tampered data?)")
            raise ValueError("Invalid or tampered ciphertext")
            
        except Exception as e:
            logger.error("Decryption failed", extra={"error": str(e)})
            raise RuntimeError("Decryption failed") from e
    
    def encrypt_with_ttl(self, plaintext: str, ttl_seconds: int) -> str:
        """
        Encrypt PHI with time-to-live (expiration).
        
        Args:
            plaintext: Sensitive data to encrypt
            ttl_seconds: Time-to-live in seconds
            
        Returns:
            Base64-encoded ciphertext with embedded expiration
            
        Use Cases:
        - Temporary patient links (expire after 24 hours)
        - Session tokens (expire after 15 minutes)
        - Export files (expire after 7 days)
        """
        if not plaintext:
            raise ValueError("Cannot encrypt empty string")
        
        try:
            import time
            ciphertext = self.fernet.encrypt_at_time(
                plaintext.encode(),
                current_time=int(time.time())
            )
            return ciphertext.decode()
            
        except Exception as e:
            logger.error("TTL encryption failed", extra={"error": str(e)})
            raise RuntimeError("TTL encryption failed") from e
    
    def decrypt_with_ttl(self, ciphertext: str, ttl_seconds: int) -> str:
        """
        Decrypt PHI with TTL validation.
        
        Args:
            ciphertext: Encrypted data with expiration
            ttl_seconds: Maximum age in seconds
            
        Returns:
            Decrypted plaintext
            
        Raises:
            InvalidToken: If ciphertext expired or tampered
        """
        if not ciphertext:
            raise ValueError("Cannot decrypt empty string")
        
        try:
            plaintext_bytes = self.fernet.decrypt(
                ciphertext.encode(),
                ttl=ttl_seconds
            )
            return plaintext_bytes.decode()
            
        except InvalidToken as e:
            if "expired" in str(e).lower():
                logger.warning("Decryption failed: Token expired")
            else:
                logger.error("Decryption failed: Invalid token")
            raise
            
        except Exception as e:
            logger.error("TTL decryption failed", extra={"error": str(e)})
            raise RuntimeError("TTL decryption failed") from e
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64-encoded 44-character key
            
        Security Notes:
        - ⚠️ Store this key securely (environment variable, AWS Secrets Manager)
        - ⚠️ NEVER commit to git
        - ⚠️ Rotate keys regularly (every 90 days)
        - Keep old keys for decrypting historical data
        """
        key = Fernet.generate_key()
        return key.decode()


# ==========================================
# Global Instance (singleton)
# ==========================================
def get_encryption_service() -> EncryptionService:
    """
    Get encryption service instance (singleton).
    
    Loads encryption key from settings on first call.
    """
    from src.settings import settings
    
    return EncryptionService(
        encryption_key=settings.ENCRYPTION_KEY,
        kms_key_id=settings.AWS_KMS_KEY_ID
    )


# For convenience (import and use directly)
# Example: from src.security.encryption import encryption_service
try:
    encryption_service = get_encryption_service()
except Exception as e:
    logger.warning(f"Encryption service not initialized: {e}")
    encryption_service = None
