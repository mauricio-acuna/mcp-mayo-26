# 🏥 MediMind MCP - Guía Completa de Implementación

**Documento para Completar Phase 1 al 100%**  
**Idioma**: Español  
**Fecha**: Noviembre 2025  
**Estado Actual**: 45% Completado  
**Meta**: 100% Phase 1 - HIPAA-Compliant Foundation

---

## 📊 Resumen Ejecutivo

### Estado Actual del Proyecto

**✅ COMPLETADO (45%)**:
- Estructura de proyecto y carpetas
- Configuración base (settings.py, .env)
- Capa de seguridad (encryption, audit, deidentify)
- Modelos de base de datos con PHI encriptado
- Cliente FHIR con SMART OAuth 2.0
- Aplicación FastAPI con middleware de auditoría
- Infraestructura Docker (PostgreSQL, MongoDB, Redis)
- Documentación básica (README, HIPAA_CHECKLIST)

**❌ PENDIENTE (55%)**:
- Documentos de compliance (BAA, BREACH_RESPONSE, SECURITY_AUDIT)
- Herramientas clínicas (drug interactions, clinical scores)
- Modelos AI/ML (BioGPT, scispaCy)
- Suite completa de tests (unit, integration, clinical validation)
- Multi-Factor Authentication (MFA)
- Endpoints API REST
- Configuración Alembic migrations
- Documentación API OpenAPI/Swagger

---

## 🎯 Objetivos de Phase 1 (100%)

### Criterios de Éxito

Según el INIT_PROMPT.md, Phase 1 está completo cuando:

- [x] FastAPI server arranca con middleware de auditoría HIPAA
- [x] Todo PHI encriptado en reposo (verificado)
- [x] Cliente FHIR autentica con Epic sandbox
- [x] Audit log registra cada acceso a PHI
- [ ] **Drug interaction checker retorna resultados** ⬅️ PENDIENTE
- [x] De-identification remueve PHI del texto
- [ ] **Tests unitarios pasan con >80% coverage** ⬅️ PENDIENTE
- [ ] **Security scan pasa (Bandit)** ⬅️ PENDIENTE
- [ ] **HIPAA checklist 100% completo** ⬅️ PENDIENTE (actualmente 45%)

---

## 📋 Plan de Trabajo Detallado

### PRIORIDAD 1: Documentos de Compliance (2-3 días)

#### 1.1. Business Associate Agreement (BAA)

**Archivo**: `compliance/BAA_TEMPLATE.md`

**Propósito**: Contrato legal requerido con todos los vendors que manejan PHI (AWS, DrugBank, Epic, etc.)

**Contenido Requerido**:

```markdown
# Plantilla de Business Associate Agreement (BAA)

## I. Definiciones
- **Covered Entity**: [Hospital/Clínica que usa MediMind]
- **Business Associate**: MediMind MCP Inc.
- **Protected Health Information (PHI)**: Definición según HIPAA §160.103

## II. Obligaciones del Business Associate

### 2.1 Uso de PHI
- Solo usar PHI para servicios especificados en el contrato
- No usar/divulgar PHI excepto según lo permitido por este acuerdo
- Implementar salvaguardas administrativas, físicas y técnicas (§164.308-312)

### 2.2 Salvaguardas de Seguridad
- Encriptación AES-256 en reposo
- TLS 1.3+ en tránsito
- Audit logging inmutable con retención de 7 años
- MFA para todos los usuarios
- Backups encriptados diarios

### 2.3 Reporte de Incidentes
- Notificar a Covered Entity dentro de 24 horas de descubrir una brecha
- Proporcionar documentación completa del incidente
- Cooperar en investigaciones y notificaciones a pacientes/HHS

## III. Sub-contratistas Permitidos
- AWS (con BAA firmado): Hosting de infraestructura
- DrugBank: API de interacciones de medicamentos
- Epic Systems: Integración FHIR

## IV. Duración y Terminación
- Vigencia: [Fecha inicio] a [Fecha fin]
- Terminación por incumplimiento con 30 días de aviso
- Al terminar: Devolver/destruir todo PHI según instrucciones

## V. Indemnización
- Business Associate indemnizará a Covered Entity por violaciones de HIPAA
- Límite de responsabilidad: $10,000,000 USD
- Seguro de cyber-liability requerido

## VI. Firmas
[Espacios para firmas de ambas partes con fecha]
```

**Instrucciones de Implementación**:
1. Revisar con abogado especializado en HIPAA
2. Personalizar para cada vendor (AWS, DrugBank, Epic)
3. Obtener firmas antes de procesar PHI real
4. Almacenar en carpeta segura `compliance/signed_baas/`
5. Renovar anualmente o cuando cambien términos

---

#### 1.2. Plan de Respuesta a Brechas

**Archivo**: `compliance/BREACH_RESPONSE.md`

**Propósito**: Procedimiento paso a paso para responder a brechas de seguridad (requerido por HIPAA §164.404-414)

**Contenido Requerido**:

```markdown
# Plan de Respuesta a Brechas de Seguridad - MediMind MCP

## 🚨 Definición de Brecha

Según HIPAA §164.402, una brecha es:
- Adquisición, acceso, uso o divulgación de PHI no autorizada
- Que compromete la seguridad o privacidad del PHI
- Excepto: Accesos accidentales de buena fe por empleados autorizados

**Ejemplos de Brechas**:
- Laptop robada con PHI sin encriptar
- Acceso no autorizado a base de datos
- Email con PHI enviado a destinatario incorrecto
- Ataque ransomware que encripta registros médicos
- Empleado vendiendo registros médicos

## 📋 Procedimiento de Respuesta (Primeras 24 Horas)

### Fase 1: Detección y Contención (0-4 horas)

**Paso 1 - Detección**:
```bash
# Revisar logs de auditoría para accesos sospechosos
psql -h localhost -U medimind -d medimind -c \
  "SELECT * FROM audit_logs WHERE phi_accessed=true 
   AND timestamp > NOW() - INTERVAL '24 hours' 
   ORDER BY timestamp DESC;"

# Alertas automáticas de monitoring
aws cloudwatch get-metric-statistics \
  --namespace MediMind/Security \
  --metric-name UnauthorizedAccess \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S)
```

**Paso 2 - Contención Inmediata**:
- [ ] Aislar sistemas afectados (desconectar de red si necesario)
- [ ] Revocar credenciales comprometidas
- [ ] Cambiar todas las contraseñas de administrador
- [ ] Habilitar modo de solo lectura en base de datos
- [ ] Documentar TODO (screenshots, logs, timestamps)

**Paso 3 - Notificación Interna**:
```python
# Script de notificación automática
import smtplib
from email.mime.text import MIMEText

recipients = [
    "security@medimind.com",
    "ciso@medimind.com",
    "legal@medimind.com",
    "ceo@medimind.com"
]

msg = MIMEText(f"""
ALERTA DE BRECHA DE SEGURIDAD

Timestamp: {datetime.now()}
Sistema: MediMind MCP Production
Descripción: [DESCRIPCIÓN DETALLADA]
PHI Afectado: [NÚMERO DE REGISTROS]
Acciones Tomadas: [LISTA]

Equipo de Respuesta: Reunión inmediata en Zoom
""")

msg['Subject'] = '🚨 HIPAA BREACH ALERT - IMMEDIATE ACTION REQUIRED'
msg['From'] = 'alerts@medimind.com'
msg['To'] = ', '.join(recipients)

# Enviar email
```

### Fase 2: Evaluación (4-24 horas)

**Paso 4 - Análisis de Impacto**:
```sql
-- ¿Cuántos pacientes afectados?
SELECT COUNT(DISTINCT patient_id) as affected_patients
FROM audit_logs 
WHERE timestamp BETWEEN '[INICIO_BRECHA]' AND '[FIN_BRECHA]'
  AND action IN ('UNAUTHORIZED_ACCESS', 'DATA_EXPORT');

-- ¿Qué datos específicos fueron accedidos?
SELECT resource_type, COUNT(*) as access_count
FROM audit_logs
WHERE user_id = '[USUARIO_SOSPECHOSO]'
  AND phi_accessed = true
GROUP BY resource_type;
```

**Criterios de Evaluación**:
- [ ] **Bajo Riesgo**: <500 pacientes, solo nombres sin SSN/diagnósticos
- [ ] **Riesgo Medio**: 500-5000 pacientes, incluye fechas nacimiento
- [ ] **Alto Riesgo**: >5000 pacientes o incluye SSN/diagnósticos sensibles

**Paso 5 - Documentación Legal**:
Crear reporte forense con:
1. Timeline exacto del incidente
2. Número de registros comprometidos
3. Tipos de PHI afectados (nombre, SSN, diagnósticos, etc.)
4. Vector de ataque utilizado
5. Vulnerabilidad explotada
6. Medidas de mitigación implementadas

### Fase 3: Notificación (24-60 horas)

**HIPAA REQUIERE**:
- **Pacientes**: Notificar dentro de **60 días** (carta certificada)
- **HHS (Dept. of Health)**: Notificar dentro de **60 días** si >500 pacientes
- **Medios**: Notificar dentro de **60 días** si >500 pacientes en un estado
- **Business Associates**: Notificar dentro de **60 días**

**Plantilla de Carta a Pacientes**:
```
[Membrete Hospital/MediMind]
[Fecha]

Estimado/a [Nombre Paciente],

Le escribimos para informarle sobre un incidente de seguridad que puede 
haber afectado la privacidad de su información médica.

¿QUÉ SUCEDIÓ?
El [Fecha], descubrimos que [Descripción del incidente]. 

¿QUÉ INFORMACIÓN FUE AFECTADA?
Su información personal incluida en este incidente: [Lista específica]

¿QUÉ ESTAMOS HACIENDO?
- [Medidas tomadas]
- Fortalecimiento de seguridad
- Cooperación con autoridades

¿QUÉ PUEDE HACER USTED?
- Revisar sus reportes de crédito gratuitamente
- Monitorear sus estados de cuenta bancarios
- Reportar actividad sospechosa

Ofrecemos 2 años de monitoreo de crédito gratuito a través de [Proveedor].

CONTACTO:
Línea directa: 1-800-XXX-XXXX (Lunes-Viernes 8am-8pm)
Email: breach-response@medimind.com

Lamentamos profundamente este incidente.

Atentamente,
[CEO/CISO Firma]
```

**Paso 6 - Notificación a HHS**:
Portal web: https://ocrportal.hhs.gov/ocr/breach/wizard_breach.jsf

Datos requeridos:
- Nombre de Covered Entity
- Número de individuos afectados
- Fecha del descubrimiento
- Tipo de PHI comprometido
- Medidas de mitigación
- ¿Notificaron a medios? (si >500 en un estado)

### Fase 4: Remediación (Semanas 2-4)

**Paso 7 - Corrección de Vulnerabilidad**:
```bash
# Ejemplo: Si la brecha fue por falta de MFA
# 1. Implementar MFA para todos los usuarios
pip install pyotp qrcode

# 2. Forzar reset de contraseñas
psql -c "UPDATE users SET password_reset_required=true;"

# 3. Auditoría de todos los accesos recientes
python scripts/audit_review.py --days 90 --suspicious-only

# 4. Penetration testing por tercero
# Contratar firma externa (Rapid7, Coalfire, etc.)
```

**Paso 8 - Actualizar Políticas**:
- [ ] Revisar y fortalecer políticas de acceso
- [ ] Entrenamiento adicional a empleados
- [ ] Implementar controles técnicos adicionales
- [ ] Actualizar este documento con lecciones aprendidas

### Fase 5: Seguimiento (Meses 1-6)

**Paso 9 - Monitoreo Post-Incidente**:
```python
# Script de monitoreo mensual
def post_breach_monitoring():
    # ¿Hay patrones de acceso inusual?
    unusual_access = db.query("""
        SELECT user_id, COUNT(*) as access_count
        FROM audit_logs
        WHERE timestamp > CURRENT_DATE - INTERVAL '30 days'
        GROUP BY user_id
        HAVING COUNT(*) > (SELECT AVG(count) * 3 FROM ...)
    """)
    
    # ¿Los controles implementados están funcionando?
    mfa_adoption = db.query("""
        SELECT 
            COUNT(*) FILTER (WHERE mfa_enabled) * 100.0 / COUNT(*) 
        FROM users
    """)
    
    # Generar reporte mensual para Board of Directors
    generate_report(unusual_access, mfa_adoption)
```

## 📞 Contactos de Emergencia

**Internos**:
- CISO: [Nombre] - [Teléfono] - [Email]
- Legal: [Nombre] - [Teléfono] - [Email]
- CEO: [Nombre] - [Teléfono] - [Email]

**Externos**:
- HHS OCR Breach Portal: https://ocrportal.hhs.gov/ocr/breach
- FBI Cyber Division: https://www.fbi.gov/investigate/cyber
- Abogado HIPAA: [Firma Legal] - [Contacto]
- Firma Forense: [Nombre] - [Contacto 24/7]
- Proveedor de Monitoreo de Crédito: [Nombre] - [Contacto]

## 💰 Estimación de Costos

**Costos Directos**:
- Investigación forense: $50,000 - $200,000
- Notificaciones a pacientes: $1 - $5 por carta
- Monitoreo de crédito (2 años): $20 - $30 por paciente/año
- Abogados: $300 - $800/hora
- Multas HHS: $100 - $50,000 por violación

**Ejemplo**: Brecha de 10,000 pacientes
- Investigación: $100,000
- Notificaciones: $50,000 (10K × $5)
- Monitoreo crédito: $600,000 (10K × $30 × 2 años)
- Legal: $200,000
- Multas estimadas: $1,000,000
- **TOTAL: ~$2,000,000**

## 📚 Referencias Legales

- HIPAA Breach Notification Rule: 45 CFR §§ 164.400-414
- HHS Guidance: https://www.hhs.gov/hipaa/for-professionals/breach-notification
- Plantillas OCR: https://www.hhs.gov/hipaa/for-professionals/breach-notification/breach-reporting

---

**IMPORTANTE**: Practicar este plan mediante simulacros trimestrales (tabletop exercises).
```

---

#### 1.3. Procedimientos de Auditoría de Seguridad

**Archivo**: `compliance/SECURITY_AUDIT.md`

**Contenido**: Ver siguiente sección...

---

### PRIORIDAD 2: Herramientas Clínicas (3-5 días)

#### 2.1. Drug Interaction Checker

**Archivo**: `mcp-server/src/tools/drug_interactions.py`

**Especificación Técnica**:

**APIs Disponibles**:
1. **DrugBank API** (Recomendado)
   - URL: https://api.drugbankplus.com/v1
   - Costo: $500-2000/mes según volumen
   - Coverage: 14,000+ medicamentos, 2M+ interacciones
   - Requiere API key (registrarse en https://drugbankplus.com/api)

2. **OpenFDA** (Gratis pero limitado)
   - URL: https://api.fda.gov/drug/event.json
   - Coverage: Solo reportes de eventos adversos
   - Sin API key necesaria
   - Rate limit: 240 requests/minuto

**Modelo de Datos**:
```python
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class InteractionSeverity(str, Enum):
    CRITICAL = "critical"  # Contraindicado - no usar juntos
    MAJOR = "major"        # Evitar combinación
    MODERATE = "moderate"  # Monitorear paciente
    MINOR = "minor"        # Precaución mínima

class DrugInteraction(BaseModel):
    drug1: str  # Nombre genérico
    drug2: str
    severity: InteractionSeverity
    description: str
    mechanism: Optional[str]  # Ej: "Ambos prolongan QT interval"
    clinical_effects: List[str]  # ["Arritmia", "Torsades de pointes"]
    management: str  # "Evitar combinación. Usar alternativa."
    evidence_level: str  # "Well-established", "Theoretical"
    sources: List[str]  # URLs a estudios/guidelines

class AllergyCheck(BaseModel):
    drug: str
    allergen: str
    cross_reactivity: bool
    severity: str
    recommendation: str
```

**Implementación Completa**:

```python
"""
Drug Interaction Checker - MediMind MCP
Integración con DrugBank API para verificar interacciones medicamentosas
"""

import httpx
from typing import List, Dict, Optional
from src.settings import settings
from src.security.audit import AuditLogger
import logging

logger = logging.getLogger(__name__)

class DrugInteractionChecker:
    """
    Verifica interacciones entre medicamentos usando DrugBank API
    
    Features:
    - Drug-drug interactions
    - Drug-allergy cross-reactivity
    - Drug-condition contraindications
    - Severity scoring (Critical/Major/Moderate/Minor)
    """
    
    def __init__(self):
        self.api_key = settings.DRUGBANK_API_KEY
        self.base_url = "https://api.drugbankplus.com/v1"
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    async def check_interactions(
        self,
        drug_list: List[str],
        patient_allergies: Optional[List[str]] = None,
        patient_conditions: Optional[List[str]] = None
    ) -> Dict:
        """
        Verifica todas las interacciones para una lista de medicamentos
        
        Args:
            drug_list: Lista de nombres de medicamentos (genéricos o comerciales)
            patient_allergies: Alergias conocidas del paciente
            patient_conditions: Condiciones médicas del paciente
            
        Returns:
            {
                "drug_drug_interactions": [...],
                "drug_allergy_conflicts": [...],
                "drug_condition_conflicts": [...],
                "severity_summary": {
                    "critical": 0,
                    "major": 2,
                    "moderate": 5,
                    "minor": 3
                },
                "recommendations": [...]
            }
        """
        results = {
            "drug_drug_interactions": [],
            "drug_allergy_conflicts": [],
            "drug_condition_conflicts": [],
            "severity_summary": {"critical": 0, "major": 0, "moderate": 0, "minor": 0},
            "recommendations": []
        }
        
        try:
            # 1. Check drug-drug interactions (pares de medicamentos)
            for i, drug1 in enumerate(drug_list):
                for drug2 in drug_list[i+1:]:
                    interaction = await self._check_drug_pair(drug1, drug2)
                    if interaction:
                        results["drug_drug_interactions"].append(interaction)
                        results["severity_summary"][interaction["severity"]] += 1
                        
                        # Si es crítico, agregar recomendación inmediata
                        if interaction["severity"] == "critical":
                            results["recommendations"].append({
                                "type": "STOP_MEDICATION",
                                "urgency": "immediate",
                                "message": f"⚠️ CRÍTICO: No administrar {drug1} con {drug2}. {interaction['management']}"
                            })
            
            # 2. Check drug-allergy conflicts
            if patient_allergies:
                for drug in drug_list:
                    for allergy in patient_allergies:
                        conflict = await self._check_allergy(drug, allergy)
                        if conflict:
                            results["drug_allergy_conflicts"].append(conflict)
                            results["recommendations"].append({
                                "type": "ALLERGY_ALERT",
                                "urgency": "immediate",
                                "message": f"🚨 ALERGIA: Paciente alérgico a {allergy}. Evitar {drug}."
                            })
            
            # 3. Check drug-condition contraindications
            if patient_conditions:
                for drug in drug_list:
                    for condition in patient_conditions:
                        conflict = await self._check_contraindication(drug, condition)
                        if conflict:
                            results["drug_condition_conflicts"].append(conflict)
                            if conflict["severity"] in ["critical", "major"]:
                                results["recommendations"].append({
                                    "type": "CONTRAINDICATION",
                                    "urgency": "high",
                                    "message": f"⚠️ CONTRAINDICADO: {drug} en paciente con {condition}."
                                })
            
            # Audit log (HIPAA requirement)
            await AuditLogger.log_access(
                db=None,  # TODO: Pasar sesión de DB
                user_id="system",
                action="DRUG_INTERACTION_CHECK",
                resource_type="DrugInteraction",
                resource_id=",".join(drug_list),
                ip_address="internal",
                user_agent="DrugInteractionChecker",
                phi_accessed=False  # No PHI en drug names
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error checking drug interactions: {e}", exc_info=True)
            # NUNCA exponer error interno al usuario (puede contener PHI)
            raise Exception("Unable to check drug interactions. Please try again.")
    
    async def _check_drug_pair(self, drug1: str, drug2: str) -> Optional[Dict]:
        """
        Verifica interacción entre 2 medicamentos específicos
        Llama a DrugBank API: GET /interactions/{drugbank_id}/interactions
        """
        try:
            # Primero, obtener DrugBank IDs para ambos medicamentos
            drug1_id = await self._get_drugbank_id(drug1)
            drug2_id = await self._get_drugbank_id(drug2)
            
            if not drug1_id or not drug2_id:
                logger.warning(f"Drug not found in DrugBank: {drug1} or {drug2}")
                return None
            
            # Consultar interacciones
            response = await self.client.get(
                f"{self.base_url}/drugs/{drug1_id}/interactions"
            )
            response.raise_for_status()
            interactions = response.json()
            
            # Buscar si drug2 está en las interacciones de drug1
            for interaction in interactions.get("data", []):
                if interaction.get("drugbank_id") == drug2_id:
                    return {
                        "drug1": drug1,
                        "drug2": drug2,
                        "severity": self._map_severity(interaction.get("severity")),
                        "description": interaction.get("description"),
                        "mechanism": interaction.get("mechanism"),
                        "clinical_effects": interaction.get("effects", []),
                        "management": interaction.get("management"),
                        "evidence_level": interaction.get("evidence_level"),
                        "sources": [
                            f"https://go.drugbank.com/drugs/{drug1_id}#interactions",
                            *interaction.get("references", [])
                        ]
                    }
            
            return None  # No interaction found
            
        except httpx.HTTPError as e:
            logger.error(f"DrugBank API error: {e}")
            return None
    
    async def _get_drugbank_id(self, drug_name: str) -> Optional[str]:
        """
        Busca el DrugBank ID para un nombre de medicamento
        Soporta nombres genéricos y comerciales
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/drugs/search",
                params={"q": drug_name, "limit": 1}
            )
            response.raise_for_status()
            results = response.json()
            
            if results.get("data"):
                return results["data"][0]["drugbank_id"]
            return None
            
        except httpx.HTTPError:
            return None
    
    async def _check_allergy(self, drug: str, allergen: str) -> Optional[Dict]:
        """
        Verifica si un medicamento tiene reactividad cruzada con una alergia
        Ejemplo: Paciente alérgico a penicilina → alerta con amoxicilina
        """
        # Mapeo de familias de medicamentos con reactividad cruzada
        CROSS_REACTIVITY_MAP = {
            "penicillin": ["amoxicillin", "ampicillin", "penicillin g", "penicillin v"],
            "sulfa": ["sulfamethoxazole", "sulfasalazine", "sulfadiazine"],
            "cephalosporin": ["cephalexin", "ceftriaxone", "cefazolin"],
            # ... agregar más familias
        }
        
        drug_lower = drug.lower()
        allergen_lower = allergen.lower()
        
        # Verificar reactividad cruzada
        for family, drugs in CROSS_REACTIVITY_MAP.items():
            if allergen_lower in drugs and drug_lower in drugs:
                return {
                    "drug": drug,
                    "allergen": allergen,
                    "cross_reactivity": True,
                    "family": family,
                    "severity": "critical",
                    "recommendation": f"CONTRAINDICADO. Paciente alérgico a {allergen}. NO usar {drug} (misma familia: {family})."
                }
        
        return None
    
    async def _check_contraindication(self, drug: str, condition: str) -> Optional[Dict]:
        """
        Verifica si un medicamento está contraindicado en una condición médica
        Ejemplo: Beta-blockers en asma severo
        """
        try:
            drug_id = await self._get_drugbank_id(drug)
            if not drug_id:
                return None
            
            response = await self.client.get(
                f"{self.base_url}/drugs/{drug_id}/contraindications"
            )
            response.raise_for_status()
            contraindications = response.json()
            
            # Buscar si la condición del paciente está contraindicada
            for ci in contraindications.get("data", []):
                if condition.lower() in ci.get("condition", "").lower():
                    return {
                        "drug": drug,
                        "condition": condition,
                        "severity": ci.get("severity", "major"),
                        "rationale": ci.get("rationale"),
                        "alternatives": ci.get("alternatives", []),
                        "monitoring": ci.get("monitoring_requirements")
                    }
            
            return None
            
        except httpx.HTTPError:
            return None
    
    def _map_severity(self, api_severity: str) -> str:
        """Mapea severity de DrugBank a nuestro enum"""
        mapping = {
            "contraindicated": "critical",
            "major": "major",
            "moderate": "moderate",
            "minor": "minor"
        }
        return mapping.get(api_severity.lower(), "moderate")
    
    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()

# Singleton global
drug_checker = DrugInteractionChecker()
```

**Testing**:
```python
# tests/unit/test_drug_interactions.py
import pytest
from src.tools.drug_interactions import DrugInteractionChecker

@pytest.mark.asyncio
async def test_warfarin_aspirin_interaction():
    """Test critical interaction: Warfarin + Aspirin (bleeding risk)"""
    checker = DrugInteractionChecker()
    
    result = await checker.check_interactions(
        drug_list=["warfarin", "aspirin"],
        patient_allergies=[],
        patient_conditions=[]
    )
    
    # Should detect critical interaction
    assert len(result["drug_drug_interactions"]) > 0
    assert result["severity_summary"]["critical"] >= 1
    assert any("bleeding" in i["description"].lower() 
              for i in result["drug_drug_interactions"])
    
    await checker.close()

@pytest.mark.asyncio
async def test_penicillin_allergy_alert():
    """Test allergy cross-reactivity: Penicillin allergy → Amoxicillin alert"""
    checker = DrugInteractionChecker()
    
    result = await checker.check_interactions(
        drug_list=["amoxicillin"],
        patient_allergies=["penicillin"],
        patient_conditions=[]
    )
    
    # Should detect allergy conflict
    assert len(result["drug_allergy_conflicts"]) > 0
    assert "penicillin" in result["drug_allergy_conflicts"][0]["family"]
    
    await checker.close()
```

**Integración en FastAPI**:
```python
# src/main.py
from src.tools.drug_interactions import drug_checker

@app.post("/api/v1/check-interactions")
async def check_drug_interactions(
    drugs: List[str],
    allergies: Optional[List[str]] = None,
    conditions: Optional[List[str]] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint para verificar interacciones medicamentosas
    
    Requiere autenticación (JWT token)
    Audita cada llamada (HIPAA compliance)
    """
    # Audit log
    await AuditLogger.log_access(
        db=db,
        user_id=current_user.id,
        action="CHECK_DRUG_INTERACTIONS",
        resource_type="DrugInteraction",
        resource_id=",".join(drugs),
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        phi_accessed=False
    )
    
    # Check interactions
    results = await drug_checker.check_interactions(
        drug_list=drugs,
        patient_allergies=allergies,
        patient_conditions=conditions
    )
    
    return results
```

**Alternativa Sin API (Usando Base de Datos Local)**:

Si no tienes presupuesto para DrugBank API, puedes usar datasets públicos:

1. **DrugBank Open Data** (gratuito, limitado):
   - https://go.drugbank.com/releases/latest
   - Descarga XML con 14,000+ drugs
   - Parsea y carga en PostgreSQL

2. **RxNorm** (NLM, gratuito):
   - https://www.nlm.nih.gov/research/umls/rxnorm
   - Mapeo de nombres comerciales → genéricos

3. **FDA Adverse Events** (OpenFDA):
   - API gratuita con millones de reportes
   - Detecta interacciones por co-ocurrencia estadística

```python
# Implementación con base de datos local
class LocalDrugInteractionChecker:
    """
    Usa base de datos local en lugar de API
    Más económico pero requiere mantenimiento de datos
    """
    
    async def check_interactions(self, drug_list: List[str]) -> Dict:
        # Query a PostgreSQL
        query = """
            SELECT d1.name as drug1, d2.name as drug2,
                   i.severity, i.description, i.mechanism
            FROM drug_interactions i
            JOIN drugs d1 ON i.drug1_id = d1.id
            JOIN drugs d2 ON i.drug2_id = d2.id
            WHERE d1.name = ANY($1) AND d2.name = ANY($1)
        """
        
        interactions = await db.fetch(query, drug_list)
        
        return self._format_results(interactions)
```

---

#### 2.2. Clinical Score Calculators

**Archivo**: `mcp-server/src/tools/clinical_scores.py`

**Scores a Implementar**:

1. **HEART Score** (Chest Pain → Cardiac Risk)
2. **CHADS2-VASc** (Stroke Risk in Atrial Fibrillation)
3. **Wells Criteria** (DVT/PE Probability)
4. **CURB-65** (Pneumonia Severity)
5. **qSOFA** (Sepsis Screening)
6. **CHA2DS2-VASc** (Stroke risk)
7. **HAS-BLED** (Bleeding risk on anticoagulation)

**Implementación Completa**: (Ver archivo separado por longitud - continúa en PRIORIDAD 3)

---

## CONTINÚA EN SIGUIENTE SECCIÓN...

(El documento continúa con 40+ páginas adicionales cubriendo:
- PRIORIDAD 3: AI/ML Models (BioGPT, scispaCy)
- PRIORIDAD 4: Testing Completo
- PRIORIDAD 5: MFA Implementation
- PRIORIDAD 6: API Endpoints REST
- PRIORIDAD 7: Alembic Migrations
- Diagramas de Arquitectura
- Scripts de Deployment
- Guías de Troubleshooting)

**Nota**: Este es un documento extenso. ¿Quieres que continúe con las siguientes prioridades o prefieres archivos separados para cada componente?
