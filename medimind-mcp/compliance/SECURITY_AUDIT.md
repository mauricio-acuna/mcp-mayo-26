# 📋 Procedimientos de Auditoría de Seguridad - MediMind MCP

**Compliance**: HIPAA §164.308(a)(8) - Evaluation  
**Frecuencia**: Trimestral (cada 3 meses)  
**Responsable**: Chief Information Security Officer (CISO)

---

## 🎯 Objetivos de Auditoría

1. **Verificar cumplimiento HIPAA** al 100%
2. **Identificar vulnerabilidades** antes de que sean explotadas
3. **Validar controles de seguridad** (encryption, audit logs, access controls)
4. **Documentar evidencia** para reguladores y certificaciones (SOC 2, HITRUST)
5. **Mejorar continuamente** la postura de seguridad

---

## 📅 Calendario de Auditorías

### Auditorías Internas (Cada 3 meses)
- **Q1 (Enero-Marzo)**: Auditoría completa + Penetration testing
- **Q2 (Abril-Junio)**: Auditoría de seguimiento
- **Q3 (Julio-Septiembre)**: Auditoría completa + Table-top exercise
- **Q4 (Octubre-Diciembre)**: Auditoría de seguimiento + Preparación para auditoría externa

### Auditorías Externas (Anuales)
- **SOC 2 Type II**: Contratar firma (Deloitte, PwC, EY) - Costo: $50K-150K
- **HITRUST**: Auditoría completa - Costo: $100K-300K
- **Penetration Testing**: Firma especializada (Rapid7, Coalfire) - Costo: $25K-75K

---

## ✅ Checklist de Auditoría Técnica

### 1. Encriptación (30 minutos)

**Objetivo**: Verificar que TODO el PHI está encriptado en reposo y en tránsito

```bash
# =====================================
# PASO 1: Verificar Encriptación en Base de Datos
# =====================================

# Conectar a PostgreSQL
psql -h localhost -U medimind -d medimind

# Verificar que PHI está encriptado (debe verse como texto cifrado)
SELECT id, first_name_encrypted, last_name_encrypted 
FROM patients 
LIMIT 5;

# ✅ PASS: Si ves strings como "gAAAAABh3Kc..." (Fernet ciphertext)
# ❌ FAIL: Si ves nombres en texto plano como "John", "María"

# Verificar SSL habilitado
SHOW ssl;
-- Debe retornar: on

# Verificar que conexiones usan SSL
SELECT datname, usename, ssl, client_addr 
FROM pg_stat_ssl 
JOIN pg_stat_activity ON pg_stat_ssl.pid = pg_stat_activity.pid;

# ✅ PASS: Columna "ssl" = t (true)
# ❌ FAIL: Columna "ssl" = f (false)

# =====================================
# PASO 2: Verificar Encriptación en Tránsito (TLS)
# =====================================

# Test conexión HTTPS (debe usar TLS 1.3)
curl -vI https://api.medimind.com/health 2>&1 | grep -i tls

# ✅ PASS: "TLSv1.3" o "TLSv1.2"
# ❌ FAIL: "TLSv1.0" o "SSLv3" (inseguros)

# Verificar certificado válido
echo | openssl s_client -connect api.medimind.com:443 -servername api.medimind.com 2>/dev/null | \
  openssl x509 -noout -dates

# ✅ PASS: notAfter fecha futura (certificado no expirado)
# ❌ FAIL: notAfter fecha pasada

# =====================================
# PASO 3: Verificar Encryption Keys
# =====================================

# Verificar que ENCRYPTION_KEY existe y es válido
python -c "
from cryptography.fernet import Fernet
import os
key = os.getenv('ENCRYPTION_KEY')
assert key, 'ENCRYPTION_KEY not set!'
assert len(key) == 44, 'Invalid key length'
f = Fernet(key.encode())
# Test encrypt/decrypt
plaintext = 'Test PHI'
ciphertext = f.encrypt(plaintext.encode())
decrypted = f.decrypt(ciphertext).decode()
assert decrypted == plaintext, 'Encryption broken!'
print('✅ Encryption key valid')
"

# =====================================
# PASO 4: Verificar Backups Encriptados
# =====================================

# Listar backups en S3 (ejemplo)
aws s3 ls s3://medimind-backups/ --recursive

# Verificar encriptación server-side
aws s3api head-object \
  --bucket medimind-backups \
  --key backup-2025-11-13.sql.gz.enc \
  --query ServerSideEncryption

# ✅ PASS: "AES256" o "aws:kms"
# ❌ FAIL: null (sin encriptación)
```

**Documentar Resultados**:
```markdown
## Auditoría de Encriptación - 2025-11-13

✅ PHI encriptado en PostgreSQL (100% de columnas sensibles)
✅ SSL/TLS 1.3 habilitado en todas las conexiones
✅ Certificado HTTPS válido hasta 2026-03-15
✅ ENCRYPTION_KEY válida y funcional
✅ Backups encriptados con AES-256
❌ HALLAZGO: Redis no tiene password (CRÍTICO)

**Acción Correctiva**: Agregar --requirepass a Redis en docker-compose.yml
**Responsable**: DevOps Team
**Fecha Límite**: 2025-11-15
```

---

### 2. Audit Logs (45 minutos)

**Objetivo**: Verificar que CADA acceso a PHI está registrado e inmutable

```sql
-- =====================================
-- PASO 1: Verificar Registro de Accesos
-- =====================================

-- ¿Cuántos logs de acceso a PHI en últimos 30 días?
SELECT COUNT(*) as total_phi_accesses
FROM audit_logs
WHERE phi_accessed = true
  AND timestamp > CURRENT_DATE - INTERVAL '30 days';

-- ✅ PASS: Si hay logs (sistema usado activamente)
-- ⚠️ WARNING: Si 0 logs pero hay usuarios activos (posible fallo de auditoría)

-- ¿Logs cubren todas las operaciones críticas?
SELECT action, COUNT(*) as count
FROM audit_logs
WHERE timestamp > CURRENT_DATE - INTERVAL '7 days'
GROUP BY action
ORDER BY count DESC;

-- Debe incluir: PATIENT_VIEW, PATIENT_SEARCH, DATA_EXPORT, 
--               LOGIN_SUCCESS, LOGIN_FAILURE, PHI_DECRYPT, etc.

-- =====================================
-- PASO 2: Verificar Inmutabilidad
-- =====================================

-- Intentar modificar un log (DEBE FALLAR)
UPDATE audit_logs 
SET action = 'MODIFIED' 
WHERE id = (SELECT id FROM audit_logs LIMIT 1);

-- ✅ PASS: Error "Permission denied" o trigger bloqueando UPDATE
-- ❌ FAIL: Update exitoso (logs son mutables - CRÍTICO)

-- Intentar eliminar un log (DEBE FALLAR)
DELETE FROM audit_logs WHERE id = (SELECT id FROM audit_logs LIMIT 1);

-- ✅ PASS: Error "Permission denied"
-- ❌ FAIL: Delete exitoso (CRÍTICO - violación HIPAA)

-- =====================================
-- PASO 3: Verificar Retención de 7 Años
-- =====================================

-- ¿Cuál es el log más antiguo?
SELECT MIN(timestamp) as oldest_log, 
       EXTRACT(YEAR FROM AGE(CURRENT_DATE, MIN(timestamp))) as years_retained
FROM audit_logs;

-- ✅ PASS: years_retained >= 7 (después de 7 años de operación)
-- ⚠️ WARNING: Si < 7 años pero sistema tiene > 7 años (logs eliminados)

-- Verificar tamaño de tabla (no debe crecer indefinidamente)
SELECT 
    pg_size_pretty(pg_total_relation_size('audit_logs')) as total_size,
    COUNT(*) as total_rows
FROM audit_logs;

-- Planificar archivado si > 100GB o > 100M rows

-- =====================================
-- PASO 4: Verificar Calidad de Datos
-- =====================================

-- ¿Hay logs sin user_id? (debe ser 0)
SELECT COUNT(*) as logs_without_user
FROM audit_logs
WHERE user_id IS NULL OR user_id = '';

-- ✅ PASS: 0 logs sin user
-- ❌ FAIL: > 0 (no se puede auditar quién accedió)

-- ¿Hay logs sin IP address? (debe ser 0)
SELECT COUNT(*) as logs_without_ip
FROM audit_logs
WHERE ip_address IS NULL OR ip_address = '';

-- ✅ PASS: 0 logs sin IP
-- ⚠️ WARNING: > 0 (dificulta investigaciones forenses)
```

**Script de Auditoría Automatizada**:
```python
# scripts/audit_review.py
"""
Script de revisión automática de audit logs
Ejecutar: python scripts/audit_review.py --days 30 --export-pdf
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from src.settings import settings
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

async def audit_review(days: int = 30):
    """Genera reporte de auditoría de últimos N días"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    # Query audit logs
    query = text("""
        SELECT 
            DATE(timestamp) as date,
            user_id,
            action,
            COUNT(*) as access_count,
            SUM(CASE WHEN phi_accessed THEN 1 ELSE 0 END) as phi_access_count
        FROM audit_logs
        WHERE timestamp > :start_date
        GROUP BY DATE(timestamp), user_id, action
        ORDER BY date DESC, access_count DESC
    """)
    
    start_date = datetime.now() - timedelta(days=days)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"start_date": start_date})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Análisis estadístico
    print("=" * 80)
    print(f"REPORTE DE AUDITORÍA: {start_date.date()} a {datetime.now().date()}")
    print("=" * 80)
    print(f"\nTotal de eventos auditados: {len(df):,}")
    print(f"Total de accesos a PHI: {df['phi_access_count'].sum():,}")
    print(f"Usuarios únicos: {df['user_id'].nunique()}")
    print(f"\nTop 5 usuarios con más accesos a PHI:")
    print(df.groupby('user_id')['phi_access_count'].sum().sort_values(ascending=False).head())
    
    # Detectar anomalías
    print("\n" + "=" * 80)
    print("ANÁLISIS DE ANOMALÍAS")
    print("=" * 80)
    
    # Usuario con accesos anormalmente altos
    avg_access = df.groupby('user_id')['access_count'].sum().mean()
    high_access = df.groupby('user_id')['access_count'].sum()
    anomalies = high_access[high_access > avg_access * 3]  # 3x promedio
    
    if len(anomalies) > 0:
        print(f"\n⚠️  USUARIOS CON ACCESO ANÓMALO (>3x promedio):")
        for user_id, count in anomalies.items():
            print(f"   - {user_id}: {count:,} accesos (promedio: {avg_access:.0f})")
            print(f"     → Revisar manualmente: ¿Acceso legítimo o posible abuso?")
    else:
        print("\n✅ No se detectaron anomalías en patrones de acceso")
    
    # Exportar a PDF (para auditorías formales)
    generate_pdf_report(df, f"audit_report_{datetime.now().date()}.pdf")
    print(f"\n✅ Reporte exportado: audit_report_{datetime.now().date()}.pdf")

def generate_pdf_report(df, filename):
    """Genera PDF profesional para auditorías"""
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "MediMind MCP - Audit Report")
    c.drawString(100, 730, f"Generated: {datetime.now()}")
    # ... agregar tablas y gráficos
    c.save()

if __name__ == "__main__":
    asyncio.run(audit_review(days=30))
```

---

### 3. Control de Acceso (30 minutos)

**Objetivo**: Verificar que solo usuarios autorizados tienen acceso

```sql
-- =====================================
-- PASO 1: Revisar Lista de Usuarios
-- =====================================

-- Listar todos los usuarios activos
SELECT id, email, role, is_active, mfa_enabled, last_login
FROM users
WHERE is_active = true
ORDER BY last_login DESC NULLS LAST;

-- ✅ Verificar manualmente:
--    - ¿Todos los usuarios son empleados actuales?
--    - ¿Roles apropiados? (no dar admin a todos)
--    - ¿MFA habilitado? (debe ser 100%)

-- =====================================
-- PASO 2: Usuarios Inactivos
-- =====================================

-- Usuarios que no han logueado en 90+ días
SELECT id, email, role, last_login,
       AGE(CURRENT_DATE, last_login) as inactive_days
FROM users
WHERE last_login < CURRENT_DATE - INTERVAL '90 days'
  AND is_active = true;

-- ⚠️ ACTION: Desactivar cuentas inactivas (reducir superficie de ataque)
UPDATE users 
SET is_active = false 
WHERE last_login < CURRENT_DATE - INTERVAL '90 days';

-- =====================================
-- PASO 3: Verificar MFA
-- =====================================

-- ¿Cuántos usuarios SIN MFA? (debe ser 0)
SELECT COUNT(*) as users_without_mfa
FROM users
WHERE is_active = true AND mfa_enabled = false;

-- ❌ FAIL: Si > 0 usuarios sin MFA (CRÍTICO para HIPAA)
-- 🔧 ACTION: Forzar MFA enrollment:
UPDATE users SET mfa_required = true WHERE mfa_enabled = false;

-- =====================================
-- PASO 4: Revisar Permisos por Rol
-- =====================================

-- Listar permisos de cada rol
SELECT r.name as role, p.resource, p.action
FROM roles r
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
ORDER BY r.name, p.resource;

-- ✅ Verificar principio de "least privilege":
--    - Admins: Full access
--    - Physicians: Read/Write patients, No system config
--    - Nurses: Read patients, Limited write
--    - Billing: Read only, No PHI (solo IDs facturación)
```

**Script de Revisión de Acceso**:
```python
# scripts/access_review.py
"""
Revisión trimestral de acceso (HIPAA requirement)
"""

from src.db.models import User, Role
from datetime import datetime, timedelta

async def quarterly_access_review():
    """
    Genera reporte de usuarios para revisión gerencial
    """
    users = await User.query.all()
    
    report = []
    for user in users:
        # Calcular último acceso a PHI
        last_phi_access = await get_last_phi_access(user.id)
        
        report.append({
            "employee_id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role.name,
            "hire_date": user.created_at,
            "last_login": user.last_login,
            "last_phi_access": last_phi_access,
            "mfa_enabled": user.mfa_enabled,
            "status": "ACTIVE" if user.is_active else "INACTIVE",
            "recommendation": get_recommendation(user, last_phi_access)
        })
    
    # Exportar a Excel para revisión de managers
    df = pd.DataFrame(report)
    df.to_excel(f"access_review_{datetime.now().date()}.xlsx", index=False)
    
    print(f"✅ Reporte generado para {len(report)} usuarios")
    print(f"   → Enviar a managers para revisión y aprobación")
    print(f"   → Deadline: 30 días")

def get_recommendation(user, last_phi_access):
    """Recomienda acción basada en uso"""
    if not user.is_active:
        return "REVOKE - Usuario inactivo"
    
    if not user.mfa_enabled:
        return "ENABLE MFA - URGENTE"
    
    if last_phi_access is None:
        return "REVIEW - Nunca accedió PHI"
    
    days_since_access = (datetime.now() - last_phi_access).days
    if days_since_access > 180:
        return "REVIEW - 180+ días sin acceso"
    
    return "APPROVE - Uso normal"
```

---

### 4. Vulnerability Scanning (60 minutos)

**Objetivo**: Identificar vulnerabilidades de seguridad en código e infraestructura

```bash
# =====================================
# PASO 1: Scan de Código con Bandit
# =====================================

# Instalar Bandit (si no está instalado)
pip install bandit

# Scan completo del código fuente
bandit -r mcp-server/src/ -f html -o security_scan.html

# Ver resultados
# ✅ PASS: 0 issues de severidad HIGH o CRITICAL
# ⚠️ WARNING: Issues de severidad MEDIUM (revisar y fix)
# ❌ FAIL: Issues de severidad HIGH/CRITICAL (fix inmediato)

# Ejemplos de vulnerabilidades comunes:
# - Hardcoded passwords (severity: HIGH)
# - SQL injection potential (severity: HIGH)
# - Uso de exec() o eval() (severity: MEDIUM)
# - Weak cryptography (severity: HIGH)

# =====================================
# PASO 2: Dependency Scanning
# =====================================

# Verificar vulnerabilidades en dependencias
pip install safety
safety check --file requirements.txt --json --output vulnerabilities.json

# Revisar CVEs encontrados
cat vulnerabilities.json | jq '.vulnerabilities[] | select(.severity == "high" or .severity == "critical")'

# 🔧 ACTION: Actualizar dependencias vulnerables
pip install --upgrade [package_name]

# =====================================
# PASO 3: Container Scanning
# =====================================

# Scan de imagen Docker con Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image medimind-mcp:latest

# ✅ PASS: 0 vulnerabilidades CRITICAL
# ⚠️ WARNING: Vulnerabilidades HIGH (parchear base image)

# =====================================
# PASO 4: Infrastructure Scan (AWS)
# =====================================

# Usar AWS Inspector (si en AWS)
aws inspector start-assessment-run \
  --assessment-template-arn arn:aws:inspector:us-east-1:123:template/xxx

# O usar ScoutSuite (gratis)
pip install scoutsuite
scout aws --report-dir ./security-audit-$(date +%F)

# Revisar hallazgos en security-audit-*/index.html
```

**Automatizar Scans en CI/CD**:
```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sundays

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r mcp-server/src/ -f json -o bandit-report.json
          
      - name: Check vulnerabilities
        run: |
          pip install safety
          safety check --file requirements.txt --json
          
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: security-scan-results
          path: |
            bandit-report.json
            vulnerabilities.json
```

---

### 5. Breach Simulation (Table-Top Exercise) (90 minutos)

**Objetivo**: Practicar respuesta a incidentes sin impacto real

**Escenario 1: Ransomware Attack**

```
SITUACIÓN:
Lunes 9:00 AM - Empleado reporta que no puede acceder a archivos.
Mensaje en pantalla: "Your files have been encrypted. Pay $50,000 Bitcoin."

SU EQUIPO DEBE:
1. [ ] Activar plan de respuesta (BREACH_RESPONSE.md)
2. [ ] Aislar sistemas infectados
3. [ ] Notificar a stakeholders (CEO, Legal, CISO)
4. [ ] Evaluar si PHI fue exfiltrado (revisar logs)
5. [ ] Decidir: ¿Pagar rescate o restaurar de backups?
6. [ ] Si PHI comprometido → notificar HHS y pacientes
7. [ ] Documentar TODO para auditoría

PREGUNTAS PARA DISCUTIR:
- ¿Cuánto tiempo toma restaurar de backups?
- ¿Los backups están encriptados y offsite?
- ¿Cómo comunicamos a pacientes?
- ¿Cuándo involucrar FBI?
- ¿Tenemos seguro cyber-liability?

MÉTRICAS DE ÉXITO:
- Tiempo de detección: < 4 horas
- Tiempo de contención: < 24 horas
- Notificación a leadership: < 2 horas
- Documentación completa: ✅
```

**Escenario 2: Insider Threat**

```
SITUACIÓN:
Enfermera accede a 500+ registros de pacientes en 1 hora.
No tiene justificación clínica (no están en su unidad).
Posible venta de datos en dark web.

SU EQUIPO DEBE:
1. [ ] Revisar audit logs para confirmar accesos
2. [ ] Suspender cuenta de usuario inmediatamente
3. [ ] Contactar HR y Legal
4. [ ] Preservar evidencia (no alterar logs)
5. [ ] Investigar: ¿Descargó datos? ¿Envió emails?
6. [ ] Determinar si es brecha reportable
7. [ ] Decidir acciones legales (despido, denuncia policial)

CRITERIOS PARA REPORTAR A HHS:
- ✅ SÍ: Si hay evidencia de que datos salieron del sistema
- ❌ NO: Si solo fue acceso visual sin descarga
```

---

## 📊 Reporte de Auditoría (Template)

```markdown
# Reporte de Auditoría de Seguridad HIPAA

**Fecha**: 2025-11-13  
**Auditor**: [Nombre, CISO]  
**Alcance**: Auditoría trimestral Q4 2025  
**Duración**: 4 horas

---

## Resumen Ejecutivo

**Status General**: ✅ COMPLIANT  
**Hallazgos Críticos**: 0  
**Hallazgos Altos**: 2  
**Hallazgos Medios**: 5  
**Recomendaciones**: 8

**Conclusión**: MediMind MCP cumple con requisitos HIPAA. 
Se identificaron 2 hallazgos de prioridad alta que requieren remediación 
dentro de 30 días.

---

## Hallazgos Detallados

### 🔴 ALTO - Usuarios sin MFA (2 hallazgos)

**Descripción**: 3 usuarios activos no tienen MFA habilitado  
**Riesgo**: Compromiso de credenciales → acceso no autorizado a PHI  
**HIPAA**: Violación de §164.312(a)(2)(i) - Unique user identification  
**Remediación**: Forzar MFA enrollment para estos usuarios  
**Responsable**: IT Security Team  
**Deadline**: 2025-11-20  
**Usuarios afectados**:
- john.doe@medimind.com
- maria.gonzalez@medimind.com
- tech-support@medimind.com

### 🔴 ALTO - Redis sin password

**Descripción**: Redis cache no tiene authentication habilitada  
**Riesgo**: Acceso no autorizado a sesiones de usuarios  
**Remediación**: Agregar --requirepass a docker-compose.yml  
**Responsable**: DevOps  
**Deadline**: 2025-11-15

### 🟡 MEDIO - Logs de auditoría sin archivo

**Descripción**: Tabla audit_logs tiene 50M registros (120GB)  
**Riesgo**: Performance degradation, costos de storage  
**Remediación**: Implementar archivado automático a S3 Glacier  
**Responsable**: Database Team  
**Deadline**: 2025-12-31

---

## Verificaciones Exitosas

✅ PHI encriptado en reposo (AES-256)  
✅ TLS 1.3 en todas las conexiones  
✅ Audit logs inmutables (triggers funcionando)  
✅ Retención de logs 7+ años  
✅ Backups encriptados y offsite  
✅ Penetration test anual completado  
✅ BAAs firmados con todos los vendors  

---

## Recomendaciones

1. **Implementar MFA universal** - Eliminar excepciones
2. **Automated vulnerability scanning** - Weekly en CI/CD
3. **Incident response drills** - Trimestral (table-top exercises)
4. **Database encryption at column level** - Mejorar granularidad
5. **Implement SIEM** - Splunk/ELK para alertas en tiempo real

---

## Próxima Auditoría

**Fecha programada**: 2026-02-15  
**Tipo**: Auditoría trimestral Q1 2026  
**Enfoque especial**: Verificar remediación de hallazgos actuales

---

**Firma Digital**: [CISO]  
**Fecha**: 2025-11-13
```

---

## 🔧 Herramientas Recomendadas

### Compliance Automation
- **Vanta** ($3K-10K/año) - SOC 2 automation
- **Drata** ($2K-8K/año) - HIPAA/SOC 2 compliance
- **TrustCloud** ($1K-5K/año) - Security questionnaires

### Security Scanning
- **Bandit** (Gratis) - Python security
- **Safety** (Gratis) - Dependency scanning
- **Trivy** (Gratis) - Container scanning
- **ScoutSuite** (Gratis) - Cloud security audit

### Penetration Testing
- **Rapid7** ($15K-50K) - Comprehensive pen testing
- **Coalfire** ($25K-100K) - HIPAA-specialized
- **HackerOne** ($10K+) - Bug bounty platform

### SIEM/Monitoring
- **Splunk** ($5K-50K/año) - Enterprise SIEM
- **ELK Stack** (Gratis self-hosted) - Log aggregation
- **Datadog** ($15-100/host/mes) - APM + Security

---

## 📚 Referencias

- **HIPAA Security Rule**: https://www.hhs.gov/hipaa/for-professionals/security
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **CIS Controls**: https://www.cisecurity.org/controls
- **OWASP Top 10**: https://owasp.org/www-project-top-ten

---

**Última actualización**: Noviembre 2025  
**Próxima revisión**: Febrero 2026
