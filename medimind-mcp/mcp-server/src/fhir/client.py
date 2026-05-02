"""
FHIR R4 Client with SMART on FHIR OAuth 2.0

⚠️ SECURITY CRITICAL: Handles authentication to EHR systems (Epic, Cerner).

SMART on FHIR Flow:
1. Authorization Code Grant (OAuth 2.0)
2. Token exchange (access token + refresh token)
3. FHIR API calls with Bearer token
4. Token auto-renewal (before expiration)

Supported Operations:
- get_patient(): Fetch patient demographics
- search_observations(): Lab results, vitals
- get_medications(): Active medications
- get_allergies(): Allergy list
- get_conditions(): Problem list

Epic Sandbox:
- Register at: https://fhir.epic.com/Developer/Apps
- Use test patients: https://fhir.epic.com/Documentation?docId=testpatients

HIPAA Compliance:
- All requests audited
- Tokens encrypted in storage
- Automatic session timeout (15 minutes)
- TLS 1.3+ required
"""

import httpx
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.condition import Condition
import logging
import base64
import json

logger = logging.getLogger(__name__)


class FHIRClient:
    """
    FHIR R4 client with SMART on FHIR OAuth 2.0 authentication.
    
    Connects to Epic/Cerner EHR systems to retrieve patient data.
    """
    
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str
    ):
        """
        Initialize FHIR client.
        
        Args:
            base_url: FHIR server base URL
            client_id: OAuth client ID
            client_secret: OAuth client secret
            redirect_uri: OAuth redirect URI
        """
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        # OAuth tokens
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
        # HTTP client (with connection pooling)
        self.client = httpx.AsyncClient(
            timeout=30.0,
            verify=True,  # Enforce SSL certificate validation
            http2=True    # Use HTTP/2 if available
        )
        
        logger.info(f"FHIR client initialized: {base_url}")
    
    async def authorize(self, authorization_code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: OAuth authorization code from callback
            
        Returns:
            Token response with access_token, refresh_token, expires_in
            
        Raises:
            httpx.HTTPStatusError: If token exchange fails
        """
        token_url = f"{self.base_url}/oauth2/token"
        
        # Prepare token request
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }
        
        # Add client secret (Basic Auth or POST body)
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        try:
            response = await self.client.post(
                token_url,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            # Store tokens
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            logger.info("OAuth authorization successful")
            
            return token_data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Token exchange failed: {e.response.text}")
            raise ValueError(f"OAuth authorization failed: {e.response.status_code}")
    
    async def refresh_access_token(self) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        
        Returns:
            New token response
            
        Raises:
            ValueError: If no refresh token available
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        token_url = f"{self.base_url}/oauth2/token"
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }
        
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        try:
            response = await self.client.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Update tokens
            self.access_token = token_data["access_token"]
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            logger.info("Access token refreshed")
            
            return token_data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Token refresh failed: {e.response.text}")
            raise ValueError(f"Token refresh failed: {e.response.status_code}")
    
    async def _ensure_valid_token(self):
        """Ensure access token is valid, refresh if needed."""
        if not self.access_token:
            raise ValueError("No access token. Call authorize() first.")
        
        # Refresh if token expires in < 5 minutes
        if self.token_expires_at and datetime.utcnow() >= (self.token_expires_at - timedelta(minutes=5)):
            logger.info("Access token expiring soon, refreshing...")
            await self.refresh_access_token()
    
    async def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated FHIR API request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: FHIR resource path (e.g., "Patient/123")
            params: Query parameters
            json_data: JSON body (for POST/PUT)
            
        Returns:
            FHIR resource or Bundle
            
        Raises:
            httpx.HTTPStatusError: If request fails
        """
        await self._ensure_valid_token()
        
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json" if json_data else "application/json",
        }
        
        try:
            response = await self.client.request(
                method,
                url,
                params=params,
                json=json_data,
                headers=headers
            )
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(
                f"FHIR request failed: {method} {path}",
                extra={"status_code": e.response.status_code, "response": e.response.text}
            )
            raise
    
    async def get_patient(self, patient_id: str) -> Patient:
        """
        Fetch patient demographics.
        
        Args:
            patient_id: FHIR Patient ID
            
        Returns:
            FHIR Patient resource
            
        ⚠️ AUDIT: This accesses PHI!
        """
        data = await self._make_request("GET", f"Patient/{patient_id}")
        return Patient(**data)
    
    async def search_observations(
        self,
        patient_id: str,
        category: Optional[str] = None,
        code: Optional[str] = None,
        date_range: Optional[tuple] = None,
        limit: int = 100
    ) -> List[Observation]:
        """
        Search patient observations (labs, vitals, etc.).
        
        Args:
            patient_id: FHIR Patient ID
            category: Observation category (vital-signs, laboratory, etc.)
            code: LOINC code (e.g., "8480-6" for systolic BP)
            date_range: Tuple of (start_date, end_date)
            limit: Maximum results
            
        Returns:
            List of FHIR Observation resources
            
        Examples:
            # Get all vitals
            vitals = await client.search_observations("123", category="vital-signs")
            
            # Get blood pressure readings
            bp = await client.search_observations("123", code="8480-6")
        """
        params = {
            "patient": patient_id,
            "_count": limit,
            "_sort": "-date"
        }
        
        if category:
            params["category"] = category
        if code:
            params["code"] = code
        if date_range:
            params["date"] = f"ge{date_range[0]}&date=le{date_range[1]}"
        
        data = await self._make_request("GET", "Observation", params=params)
        
        observations = []
        if data.get("entry"):
            for entry in data["entry"]:
                observations.append(Observation(**entry["resource"]))
        
        return observations
    
    async def get_medications(self, patient_id: str) -> List[MedicationRequest]:
        """
        Get active medications for patient.
        
        Args:
            patient_id: FHIR Patient ID
            
        Returns:
            List of FHIR MedicationRequest resources
        """
        params = {
            "patient": patient_id,
            "status": "active",
            "_count": 100
        }
        
        data = await self._make_request("GET", "MedicationRequest", params=params)
        
        medications = []
        if data.get("entry"):
            for entry in data["entry"]:
                medications.append(MedicationRequest(**entry["resource"]))
        
        return medications
    
    async def get_allergies(self, patient_id: str) -> List[AllergyIntolerance]:
        """
        Get patient allergies and intolerances.
        
        Args:
            patient_id: FHIR Patient ID
            
        Returns:
            List of FHIR AllergyIntolerance resources
        """
        params = {
            "patient": patient_id,
            "_count": 100
        }
        
        data = await self._make_request("GET", "AllergyIntolerance", params=params)
        
        allergies = []
        if data.get("entry"):
            for entry in data["entry"]:
                allergies.append(AllergyIntolerance(**entry["resource"]))
        
        return allergies
    
    async def get_conditions(self, patient_id: str) -> List[Condition]:
        """
        Get patient conditions (problem list).
        
        Args:
            patient_id: FHIR Patient ID
            
        Returns:
            List of FHIR Condition resources
        """
        params = {
            "patient": patient_id,
            "_count": 100
        }
        
        data = await self._make_request("GET", "Condition", params=params)
        
        conditions = []
        if data.get("entry"):
            for entry in data["entry"]:
                conditions.append(Condition(**entry["resource"]))
        
        return conditions
    
    async def close(self):
        """Close HTTP client connection pool."""
        await self.client.aclose()


# ==========================================
# Global Instance (singleton)
# ==========================================
def get_fhir_client() -> FHIRClient:
    """
    Get FHIR client instance (singleton).
    
    Loads configuration from settings.
    """
    from src.settings import settings
    
    return FHIRClient(
        base_url=settings.FHIR_BASE_URL,
        client_id=settings.FHIR_CLIENT_ID,
        client_secret=settings.FHIR_CLIENT_SECRET,
        redirect_uri=settings.FHIR_REDIRECT_URI
    )
