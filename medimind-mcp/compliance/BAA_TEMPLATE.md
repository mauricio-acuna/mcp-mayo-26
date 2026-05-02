# 📄 Plantilla de Business Associate Agreement (BAA)

**Para**: Contratos HIPAA con Vendors que Manejan PHI  
**Compliance**: HIPAA §164.502(e), §164.504(e)  
**Versión**: 2.0  
**Fecha**: Noviembre 2025

---

## ⚠️ IMPORTANTE

Este es un **documento legal vinculante**. Debe ser revisado y modificado por:
1. **Abogado especializado en HIPAA** (obligatorio)
2. **Oficial de Cumplimiento** de tu organización
3. **Legal del vendor** (negociación de términos)

**NO usar este template sin revisión legal**. Las multas por BAAs incorrectos pueden llegar a **$1.5M por año**.

---

## Cuándo se Necesita un BAA

✅ **SÍ necesitas BAA con**:
- Proveedores de hosting (AWS, Google Cloud, Azure)
- APIs de datos médicos (DrugBank, Epic, Cerner)
- Servicios de backup/storage (S3, Glacier)
- Servicios de email que manejan PHI (SendGrid con nombres de pacientes)
- Consultores que acceden a tu sistema
- Firmas de pen-testing que ven datos reales

❌ **NO necesitas BAA con**:
- Servicios que NO ven PHI (Google Analytics en marketing site)
- Proveedores de office supplies
- Servicios de payroll (si NO tienen acceso a registros médicos)

---

## PLANTILLA DE BAA - VERSIÓN COMPLETA

```markdown
BUSINESS ASSOCIATE AGREEMENT (BAA)

Entre:
[NOMBRE DE LA COVERED ENTITY / HOSPITAL / CLÍNICA]
("Covered Entity")

Y:
[NOMBRE DEL VENDOR / BUSINESS ASSOCIATE]
("Business Associate")

Fecha Efectiva: _________________

---

## ARTÍCULO 1: DEFINICIONES

1.1 **Protected Health Information (PHI)**: Tiene el significado dado en 45 CFR §160.103, 
limitado a la información creada o recibida por Business Associate de o en nombre de 
Covered Entity.

1.2 **Required By Law**: Tiene el significado dado en 45 CFR §164.103.

1.3 **Secretary**: Significa el Secretario del Departamento de Salud y Servicios Humanos 
de los Estados Unidos (HHS).

1.4 **Breach**: Tiene el significado dado en 45 CFR §164.402.

1.5 **Security Incident**: Tiene el significado dado en 45 CFR §164.304.

1.6 **Unsecured PHI**: Tiene el significado dado en 45 CFR §164.402.

---

## ARTÍCULO 2: TÉRMINOS Y OBLIGACIONES DEL BUSINESS ASSOCIATE

2.1 **Uso Permitido de PHI**

El Business Associate podrá usar o divulgar PHI ÚNICAMENTE según sea necesario para:
(a) Realizar los servicios especificados en el Acuerdo Subyacente entre las partes
(b) Cumplir con obligaciones legales del Business Associate
(c) Realizar actividades de administración del Business Associate

**PROHIBIDO**:
- Usar PHI de manera inconsistente con la Regla de Privacidad HIPAA (45 CFR Part 164)
- Vender PHI sin autorización del paciente (HITECH Act §13405(d))
- Usar PHI para marketing sin autorización del paciente

2.2 **Salvaguardas Administrativas, Físicas y Técnicas**

El Business Associate implementará y mantendrá salvaguardas apropiadas de acuerdo con 
45 CFR §§164.308, 164.310 y 164.312, incluyendo:

**Salvaguardas Técnicas MÍNIMAS**:
- ✅ Encriptación AES-256 de PHI en reposo
- ✅ TLS 1.3+ para transmisión de PHI
- ✅ Unique user identification (§164.312(a)(2)(i))
- ✅ Emergency access procedures (§164.312(a)(2)(ii))
- ✅ Automatic logoff después de 15 minutos de inactividad
- ✅ Encryption and decryption (§164.312(a)(2)(iv))
- ✅ Audit controls (§164.312(b))
- ✅ Integrity controls (§164.312(c)(1))
- ✅ Transmission security (§164.312(e))

**Salvaguardas Administrativas**:
- ✅ Risk analysis anual (§164.308(a)(1)(ii)(A))
- ✅ Workforce security (background checks, HIPAA training)
- ✅ Información system activity review mensual
- ✅ Business Associate Agreements con sub-contratistas
- ✅ Contingency plan (disaster recovery)

**Salvaguardas Físicas**:
- ✅ Facility access controls (badges, logs de entrada/salida)
- ✅ Workstation security (screens locked cuando no en uso)
- ✅ Device and media controls (destrucción segura de hardware)

2.3 **Reportes de Breach e Incidentes de Seguridad**

(a) **Discovery de Breach**: Business Associate notificará a Covered Entity **dentro de 
24 horas** del discovery de un Breach de Unsecured PHI.

(b) **Contenido de Notificación**: La notificación incluirá, en la medida conocida:
   - Identificación de cada individuo afectado
   - Breve descripción del incidente (fecha, circunstancias)
   - Tipos de PHI involucrados (nombres, SSN, diagnósticos, etc.)
   - Pasos tomados para mitigar daño
   - Contacto para preguntas
   
(c) **Obligación de Notificar a Individuos**: Si Covered Entity determina que se requiere 
notificación a pacientes bajo 45 CFR §164.404, Business Associate:
   - Cooperará totalmente en la investigación
   - Proporcionará información necesaria para las notificaciones
   - Pagará todos los costos asociados (notificaciones, monitoreo de crédito, multas)

(d) **Security Incidents**: Business Associate reportará Security Incidents exitosos 
(no solo intentos bloqueados) dentro de 24 horas.

2.4 **Acceso, Enmienda y Contabilización**

(a) **Acceso**: Business Associate proporcionará acceso a PHI de un individuo dentro de 
10 días de solicitud de Covered Entity (para cumplir con §164.524).

(b) **Enmienda**: Business Associate enmendará PHI cuando Covered Entity lo solicite, 
dentro de 10 días (para cumplir con §164.526).

(c) **Accounting of Disclosures**: Business Associate documentará divulgaciones de PHI 
y proporcionará información dentro de 20 días de solicitud (para cumplir con §164.528).

**Registros Mínimos para Accounting**:
- Fecha de divulgación
- Nombre y dirección del recipiente
- Breve descripción del PHI divulgado
- Propósito de la divulgación

2.5 **Libros y Registros Disponibles**

Business Associate pondrá a disposición de Secretary (HHS) sus registros internos, libros 
y prácticas relacionados con uso/divulgación de PHI para determinar cumplimiento con 
HIPAA (45 CFR §164.504(e)(2)(ii)(H)).

---

## ARTÍCULO 3: SUB-CONTRATISTAS

3.1 **Autorización de Sub-contratistas**

Business Associate puede divulgar PHI a sub-contratistas ÚNICAMENTE si:
(a) Sub-contratista acepta por escrito (Sub-BAA) las mismas restricciones que este BAA
(b) Covered Entity es notificado del sub-contratista (lista actualizada trimestralmente)

**Sub-contratistas Pre-Aprobados** (Anexo A de este BAA):
- Amazon Web Services (AWS) - Hosting de infraestructura
- MongoDB Inc. - Base de datos de documentos clínicos
- [Agregar otros vendors autorizados]

3.2 **Responsabilidad por Sub-contratistas**

Business Associate es totalmente responsable por actos/omisiones de sub-contratistas 
relacionados con obligaciones de este BAA, como si fueran actos del Business Associate.

---

## ARTÍCULO 4: DURACIÓN Y TERMINACIÓN

4.1 **Término**

Este BAA entra en vigencia en la Fecha Efectiva y continuará hasta:
(a) Terminación del Acuerdo Subyacente, O
(b) Terminación según Artículo 4.2

4.2 **Terminación por Causa**

(a) **Por Covered Entity**: Si Covered Entity determina que Business Associate ha 
violado materialmente cualquier obligación de este BAA, Covered Entity puede:
   - Proporcionar oportunidad de curar la violación dentro de 30 días, O
   - Terminar este BAA y el Acuerdo Subyacente inmediatamente si la cura no es posible
   
(b) **Por Business Associate**: Business Associate puede terminar este BAA con 90 días 
de aviso escrito si Covered Entity solicita uso/divulgación de PHI que violaría HIPAA.

4.3 **Obligaciones al Terminar**

Dentro de 30 días de terminación, Business Associate:
(a) Devolverá o destruirá TODO PHI recibido de Covered Entity
(b) Certificará por escrito la devolución o destrucción
(c) Si devolución/destrucción no es factible, extenderá protecciones de este BAA 
    y limitará uso/divulgación

**Método de Destrucción Aceptable**:
- Hard drives: Destrucción física (trituración) O Wiping con herramienta NIST 800-88 compliant
- Backups: Encriptación de datos + destrucción de encryption keys
- Papel: Trituración cross-cut (particles < 1mm²)

---

## ARTÍCULO 5: INDEMNIZACIÓN Y RESPONSABILIDAD

5.1 **Indemnización**

Business Associate indemnizará, defenderá y eximirá de responsabilidad a Covered Entity 
de y contra todas las reclamaciones, pérdidas, responsabilidades, daños, costos y gastos 
(incluyendo honorarios razonables de abogados) que surjan de:
(a) Violación de este BAA por Business Associate
(b) Uso o divulgación no autorizada de PHI por Business Associate
(c) Breach de Unsecured PHI bajo el control del Business Associate

5.2 **Límite de Responsabilidad**

**NO APLICABLE** para violaciones de este BAA. No habrá límite de responsabilidad para:
- Multas HIPAA impuestas por HHS
- Costos de notificación a individuos
- Servicios de monitoreo de crédito para individuos afectados
- Daños a reputación de Covered Entity
- Honorarios legales

Límite de responsabilidad en Acuerdo Subyacente NO aplica a violaciones HIPAA.

5.3 **Seguro**

Business Associate mantendrá durante el término de este BAA:
- **Cyber Liability Insurance**: Mínimo $10,000,000 por incidente
- **Errors & Omissions Insurance**: Mínimo $5,000,000 por incidente
- **General Liability Insurance**: Mínimo $2,000,000 por incidente

Covered Entity debe ser nombrado como "Additional Insured" en todas las pólizas.

---

## ARTÍCULO 6: ENMIENDAS

6.1 **Enmiendas por Cambios en Ley**

Las partes enmendarán este BAA para cumplir con cambios en HIPAA, HITECH Act o 
regulaciones aplicables. Enmiendas entran en efecto automáticamente en la fecha de 
cumplimiento requerida.

6.2 **Enmiendas por Acuerdo Mutuo**

Las partes pueden enmendar este BAA por escrito firmado por ambas partes.

---

## ARTÍCULO 7: MISCELÁNEOS

7.1 **Ley Aplicable**

Este BAA se regirá por las leyes del Estado de [ESTADO], sin referencia a conflictos 
de leyes.

7.2 **Interpretación**

Cualquier ambigüedad en este BAA se resolverá a favor del significado que permite a 
Covered Entity cumplir con HIPAA.

7.3 **Supervivencia**

Obligaciones de este BAA sobreviven la terminación del Acuerdo Subyacente hasta que 
TODO PHI sea devuelto/destruido.

7.4 **No Terceros Beneficiarios**

Nada en este BAA confiere a terceras partes (incluyendo individuos cuyos PHI es usado/divulgado) 
derechos o remedios de ningún tipo.

---

## FIRMAS

**COVERED ENTITY**: [Nombre Legal de Hospital/Clínica]

Por: ____________________________________
Nombre: _________________________________
Título: _________________________________
Fecha: __________________________________


**BUSINESS ASSOCIATE**: [Nombre Legal de Vendor]

Por: ____________________________________
Nombre: _________________________________
Título: _________________________________
Fecha: __________________________________

---

## ANEXO A: SUB-CONTRATISTAS AUTORIZADOS

| Vendor | Servicio | BAA Firmado | Fecha | Vencimiento |
|--------|----------|-------------|-------|-------------|
| Amazon Web Services (AWS) | Hosting (EC2, RDS, S3) | ✅ | 2025-01-15 | 2026-01-15 |
| MongoDB Inc. | Database (MongoDB Atlas) | ✅ | 2025-02-01 | 2026-02-01 |
| DrugBank | Drug Interaction API | ⏳ Pendiente | - | - |
| Twilio | SMS notifications (MFA) | ✅ | 2025-03-10 | 2026-03-10 |
| SendGrid | Email (password resets) | ✅ | 2025-03-10 | 2026-03-10 |

**Nota**: Business Associate notificará a Covered Entity 30 días antes de agregar 
nuevos sub-contratistas que manejarán PHI.

---

## ANEXO B: TIPOS DE PHI MANEJADOS

Business Associate manejará los siguientes tipos de PHI:

☑ Nombres (First, Last, Middle)
☑ Fechas relacionadas con individuo (DOB, admission, discharge, death)
☑ Números telefónicos
☑ Direcciones (calle, ciudad, código postal, coordenadas geográficas)
☑ Emails
☑ Social Security Numbers (SSN)
☑ Medical Record Numbers (MRN)
☑ Account numbers
☑ Diagnósticos (ICD-10 codes)
☑ Medicamentos prescritos
☑ Resultados de laboratorio
☑ Notas clínicas
☑ Alergias
☐ Imágenes médicas (DICOM)
☐ Información genética
☐ Información de salud mental/sustancia abuse

**Uso Previsto**: Proveer sistema de soporte de decisiones clínicas que ayuda a médicos 
con diagnóstico diferencial, verificación de interacciones de medicamentos y cálculo de 
scores de riesgo clínico.

---

## ANEXO C: CONTACTOS PARA INCIDENTES DE SEGURIDAD

**Covered Entity**:
- Security Officer: ________________________
- Teléfono 24/7: __________________________
- Email: __________________________________

**Business Associate**:
- Security Officer: ________________________
- Teléfono 24/7: __________________________
- Email: __________________________________

**Escalación (Breach > 500 pacientes)**:
- CEO Covered Entity: _____________________
- CEO Business Associate: __________________

---

## CHECKLIST DE REVISIÓN DE BAA

Antes de firmar, verificar:

- [ ] Revisor legal especializado en HIPAA revisó el documento
- [ ] Seguro cyber-liability del vendor verificado ($10M+ coverage)
- [ ] Referencias del vendor contactadas y verificadas
- [ ] Penetration test report del vendor revisado (si disponible)
- [ ] SOC 2 Type II report del vendor obtenido (si aplica)
- [ ] Sub-contratistas del vendor listados en Anexo A
- [ ] Tipos específicos de PHI listados en Anexo B
- [ ] Procedimientos de breach notification acordados
- [ ] Costos de breach notification clarificados (vendor paga)
- [ ] Certificado de seguro recibido con Covered Entity como Additional Insured
- [ ] Plan de terminación documentado (devolución/destrucción de PHI)
- [ ] Ambas partes firmaron y fecharon
- [ ] Copia ejecutada archivada en carpeta segura: `compliance/signed_baas/`

---

**IMPORTANTE**: Renovar BAAs anualmente ANTES del vencimiento. 
BAA vencido = violación HIPAA.

**Recordatorio de Renovación**: Configurar alerta 90 días antes del vencimiento.
```

---

## 📋 Proceso de Negociación de BAA

### Paso 1: Request BAA del Vendor (Día 1)
```
Subject: HIPAA BAA Request - MediMind MCP

Dear [Vendor],

We are implementing MediMind MCP, a clinical decision support system that handles 
Protected Health Information (PHI). As part of our HIPAA compliance, we require a 
Business Associate Agreement (BAA) before we can use your services in production.

Service we're using: [Específico]
Expected PHI: [Patient names, MRN, diagnoses, medications]
Production start date: [Fecha]

Please send us:
1. Your standard BAA template
2. SOC 2 Type II report (if available)
3. Proof of cyber-liability insurance ($10M+ coverage)
4. List of your sub-contractors who may access data

Timeline: We need a signed BAA within 30 days.

Thank you,
[Tu Nombre]
Chief Information Security Officer
MediMind MCP
```

### Paso 2: Revisar BAA del Vendor (Días 2-5)
**Red Flags Comunes**:
- ❌ "Vendor no es responsable por brechas" → INACEPTABLE
- ❌ Límite de responsabilidad de $10K → Insuficiente ($10M mínimo)
- ❌ "30 días para reportar breach" → Demasiado lento (24 horas requerido)
- ❌ No menciona sub-contratistas → Pedir lista completa
- ❌ No incluye encriptación → Agregar requisitos técnicos

### Paso 3: Negociar Términos (Días 6-20)
Puntos típicos de negociación:
1. **Reporting timeline**: Vendor quiere 72 horas → Tú necesitas 24 horas
2. **Límite de responsabilidad**: Vendor propone $1M → Negociar $10M
3. **Audit rights**: Vendor rechaza → Insiste (HIPAA requiere)
4. **Sub-contractor disclosure**: Vendor no quiere listar → Insiste

### Paso 4: Firma y Archivo (Día 21-30)
- [ ] Ambas partes firman (DocuSign aceptable)
- [ ] Archivo en `compliance/signed_baas/vendor_name_2025.pdf`
- [ ] Agregar a tracking spreadsheet con fecha de vencimiento
- [ ] Configurar recordatorio de renovación (90 días antes)

---

## 💰 Costos Estimados de BAAs

| Vendor | Servicio | BAA | Costo Anual Servicio | Seguro Requerido |
|--------|----------|-----|---------------------|------------------|
| AWS | Hosting | Gratis (self-service) | $50K-500K | AWS tiene $10M+ |
| Google Cloud | Hosting | Gratis (auto-sign) | $30K-300K | Google tiene $100M+ |
| MongoDB Atlas | Database | Gratis | $0-10K | MongoDB tiene $10M+ |
| DrugBank | Drug API | **$500/año** | $2K-20K | Verificar |
| Twilio | SMS/MFA | **$200/año** | $1K-5K | Twilio tiene $5M |
| SendGrid | Email | Incluido en plan Business | $15-90/mes | SendGrid tiene $2M |

**Total Estimado de Fees de BAA**: $700-1000/año  
**Tiempo de Legal para Review**: 5-20 horas × $300-500/hora = $1,500-10,000

---

## 📚 Recursos Adicionales

### Templates Oficiales
- **HHS Sample BAA**: https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions
- **AMA BAA Guidance**: https://www.ama-assn.org/practice-management/hipaa

### Servicios de BAA Management
- **Vanta** - Auto-tracking de BAAs y renovaciones
- **Drata** - Compliance management platform
- **Secureframe** - Security compliance automation

### Abogados Especializados en HIPAA
- **Hogan Lovells** - Healthcare practice
- **McDermott Will & Emery** - Digital health
- **Foley & Lardner** - Health Care Industry Team

---

**Última actualización**: Noviembre 2025  
**Próxima revisión**: Noviembre 2026  
**Contacto**: legal@medimind.com
