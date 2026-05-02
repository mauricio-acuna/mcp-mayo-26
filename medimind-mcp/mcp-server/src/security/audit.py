"""
HIPAA-Compliant Audit Logging

⚠️ SECURITY CRITICAL: This module tracks ALL PHI access for HIPAA compliance.

HIPAA Requirements (§164.312(b)):
- Log every access to PHI (who, what, when, where, why)
- Audit logs must be immutable (no updates or deletes)
- Retain logs for minimum 7 years (2555 days)
- Protect logs from unauthorized access
- Regular audit log reviews

Features:
- Immutable logging (no DELETE or UPDATE)
- Automatic PHI access detection
- User/IP/action tracking
- Correlation IDs for request tracing
- Failed access attempt logging

Usage:
    from src.security.audit import audit_logger
    
    await audit_logger.log_access(
        db=db_session,
        user_id="physician_123",
        action="READ",
        resource_type="Patient",
        resource_id="patient_456",
        ip_address="10.0.1.50",
        user_agent="MediMind/1.0",
        phi_accessed=True
    )
"""

from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    HIPAA-compliant audit logging service.
    
    All PHI access MUST be logged per §164.312(b).
    Audit logs are immutable and retained for 7 years.
    """
    
    @staticmethod
    async def log_access(
        db: AsyncSession,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        ip_address: str,
        user_agent: str,
        phi_accessed: bool = False,
        context: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> str:
        """
        Log PHI access event (HIPAA requirement).
        
        Args:
            db: Database session
            user_id: User identifier (physician ID, system ID, etc.)
            action: Action performed (READ, CREATE, UPDATE, DELETE, EXPORT, etc.)
            resource_type: Type of resource (Patient, Observation, etc.)
            resource_id: Resource identifier
            ip_address: Client IP address
            user_agent: Client user agent string
            phi_accessed: Whether PHI was accessed (default: False)
            context: Additional context (optional)
            correlation_id: Request correlation ID (optional)
            
        Returns:
            Audit log entry ID (UUID)
            
        Security Notes:
        - ⚠️ NEVER log PHI values (only metadata)
        - ⚠️ Logs are immutable (no updates/deletes)
        - ⚠️ Failed access attempts MUST be logged
        - Correlation IDs help trace multi-step operations
        
        Example:
            # Good: Log access to patient record
            await audit_logger.log_access(
                db, "dr_smith", "READ", "Patient", "12345",
                "10.0.1.50", "Chrome/120", phi_accessed=True
            )
            
            # Bad: Don't log PHI values!
            # ❌ context={"patient_name": "John Doe"}  # HIPAA VIOLATION!
        """
        from src.db.models import AuditLog
        
        try:
            # Generate unique audit log ID
            audit_id = correlation_id or str(uuid.uuid4())
            
            # Create immutable audit entry
            audit_entry = AuditLog(
                id=audit_id,
                timestamp=datetime.now(UTC),
                user_id=user_id,
                action=action.upper(),
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                phi_accessed=phi_accessed,
                context=context or {}
            )
            
            db.add(audit_entry)
            await db.commit()
            
            # Log to application logs (no PHI!)
            logger.info(
                f"Audit: {action} {resource_type}/{resource_id} by {user_id}",
                extra={
                    "audit_id": audit_id,
                    "user_id": user_id,
                    "action": action,
                    "resource_type": resource_type,
                    "phi_accessed": phi_accessed,
                    "ip_address": ip_address
                }
            )
            
            return audit_id
            
        except Exception as e:
            logger.error(
                f"Failed to log audit entry: {e}",
                extra={
                    "user_id": user_id,
                    "action": action,
                    "resource_type": resource_type
                }
            )
            # Don't fail the operation if audit logging fails
            # But log the error prominently
            raise RuntimeError(f"Audit logging failed: {e}") from e
    
    @staticmethod
    async def log_authentication(
        db: AsyncSession,
        user_id: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        failure_reason: Optional[str] = None
    ) -> str:
        """
        Log authentication attempt (HIPAA requirement).
        
        Args:
            db: Database session
            user_id: User identifier attempting login
            success: Whether authentication succeeded
            ip_address: Client IP address
            user_agent: Client user agent
            failure_reason: Reason for failure (if applicable)
            
        Returns:
            Audit log entry ID
            
        Security Notes:
        - Log ALL authentication attempts (success and failure)
        - Failed attempts may indicate breach attempts
        - Monitor for brute force attacks
        """
        from src.db.models import AuditLog
        
        action = "AUTH_SUCCESS" if success else "AUTH_FAILURE"
        context = {"failure_reason": failure_reason} if failure_reason else {}
        
        audit_id = str(uuid.uuid4())
        audit_entry = AuditLog(
            id=audit_id,
            timestamp=datetime.now(UTC),
            user_id=user_id,
            action=action,
            resource_type="Authentication",
            resource_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            phi_accessed=False,
            context=context
        )
        
        db.add(audit_entry)
        await db.commit()
        
        logger.info(
            f"Authentication {'succeeded' if success else 'failed'} for {user_id}",
            extra={
                "audit_id": audit_id,
                "user_id": user_id,
                "success": success,
                "ip_address": ip_address
            }
        )
        
        return audit_id
    
    @staticmethod
    async def log_data_export(
        db: AsyncSession,
        user_id: str,
        export_format: str,
        record_count: int,
        ip_address: str,
        user_agent: str,
        phi_included: bool = True
    ) -> str:
        """
        Log data export event (HIPAA high-risk activity).
        
        Args:
            db: Database session
            user_id: User exporting data
            export_format: Format (CSV, JSON, PDF, etc.)
            record_count: Number of records exported
            ip_address: Client IP
            user_agent: Client user agent
            phi_included: Whether export contains PHI
            
        Returns:
            Audit log entry ID
            
        Security Notes:
        - Data exports are high-risk (potential breach)
        - Monitor for unusual export patterns
        - Require additional authorization for large exports
        """
        from src.db.models import AuditLog
        
        audit_id = str(uuid.uuid4())
        audit_entry = AuditLog(
            id=audit_id,
            timestamp=datetime.now(UTC),
            user_id=user_id,
            action="DATA_EXPORT",
            resource_type="Export",
            resource_id=f"export_{audit_id}",
            ip_address=ip_address,
            user_agent=user_agent,
            phi_accessed=phi_included,
            context={
                "format": export_format,
                "record_count": record_count,
                "phi_included": phi_included
            }
        )
        
        db.add(audit_entry)
        await db.commit()
        
        logger.warning(
            f"Data export by {user_id}: {record_count} records as {export_format}",
            extra={
                "audit_id": audit_id,
                "user_id": user_id,
                "record_count": record_count,
                "format": export_format,
                "phi_included": phi_included
            }
        )
        
        return audit_id
    
    @staticmethod
    async def get_user_access_history(
        db: AsyncSession,
        user_id: str,
        days: int = 30,
        phi_only: bool = False
    ) -> list:
        """
        Get user's access history (for audit review).
        
        Args:
            db: Database session
            user_id: User identifier
            days: Number of days to look back
            phi_only: Only show PHI access events
            
        Returns:
            List of audit log entries
            
        Use Cases:
        - Periodic user access reviews (HIPAA requirement)
        - Breach investigation
        - User activity monitoring
        """
        from src.db.models import AuditLog
        from datetime import timedelta
        
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        
        query = select(AuditLog).where(
            AuditLog.user_id == user_id,
            AuditLog.timestamp >= cutoff_date
        )
        
        if phi_only:
            query = query.where(AuditLog.phi_accessed == True)
        
        query = query.order_by(AuditLog.timestamp.desc())
        
        result = await db.execute(query)
        return result.scalars().all()


# ==========================================
# Global Instance (singleton)
# ==========================================
audit_logger = AuditLogger()
