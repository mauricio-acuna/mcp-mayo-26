# Tabla de Contenidos (borrador post-pivote — abril 2026)

> Este TOC reemplaza al original. El libro reduce alcance: un único caso de estudio (MediMind MCP) y foco en lo que la IA generativa todavía no resuelve bien — seguridad, compliance y operación.
>
> Ver [../PIVOTE_2026.md](../PIVOTE_2026.md) para el contexto del cambio.

## Título de trabajo

**MCP en Producción: Seguridad, Compliance y Operación a Escala**
*Caso de estudio: MediMind MCP (HIPAA + FHIR R4)*

Idioma primario: español. Extensión objetivo: 180-220 págs.

---

## Front Matter

- Portada
- Créditos
- Prefacio — [preface.md](preface.md)
- Cómo leer este libro — [how-to-read.md](how-to-read.md)
- Para quién es este libro — [who-should-read.md](who-should-read.md)

---

## Parte I — Por qué este libro (abril 2026)

### Capítulo 1 · MCP ya es commodity: dónde está el valor real
- Qué cambió entre 2024 y 2026
- Por qué los tutoriales de "tu primer MCP server" perdieron valor
- Las tres áreas donde la IA generativa todavía falla
- Cómo usar este libro

### Capítulo 2 · Modelo de amenazas de un servidor MCP en producción
- Superficie de ataque específica de MCP
- Prompt injection a través de resources y tools
- Exfiltración de datos vía respuestas de tools
- Suplantación entre clientes MCP
- Matriz STRIDE aplicada a MCP

---

## Parte II — Caso MediMind

### Capítulo 3 · Dominio clínico
- Workflow del médico en consulta
- FHIR R4 esencial (Patient, Observation, Condition, MedicationRequest)
- Qué es PHI y por qué importa
- Por qué un MCP server y no una API REST tradicional

### Capítulo 4 · Diseño de la superficie MCP
- Principio de menor privilegio aplicado a tools
- Granularidad de resources sin filtrar PHI por accidente
- Prompts del servidor: cuándo sí y cuándo no
- Versionado y deprecación de tools

### Capítulo 5 · Identidad, autenticación y autorización
- OAuth 2.1 con PKCE en MCP
- SMART on FHIR scopes
- Mapeo de identidad LLM → usuario clínico
- Sesiones, refresh y revocación

### Capítulo 6 · Cifrado, tokenización y redacción de PHI
- Cifrado en tránsito (mTLS) y reposo (envelope encryption)
- Tokenización reversible para identificadores
- Redacción automática en logs y traces
- Manejo de claves: KMS / HSM

---

## Parte III — Compliance accionable

### Capítulo 7 · HIPAA traducido a controles técnicos
- Privacy Rule vs Security Rule en código
- Salvaguardas administrativas, físicas y técnicas como tickets de implementación
- BAAs y responsabilidades compartidas con proveedores LLM

### Capítulo 8 · Auditoría y trazabilidad LLM → MCP → EHR
- Esquema de eventos de auditoría inmutables
- Correlación de prompt → tool call → query SQL → respuesta
- Retención y exportación para auditores

### Capítulo 9 · GDPR y SOC 2 cuando aplica
- Derecho al olvido en sistemas con LLM
- Controles SOC 2 Type II realistas para una startup

---

## Parte IV — Operación

### Capítulo 10 · Observabilidad sin filtrar PHI
- Métricas RED y USE adaptadas a MCP
- Traces distribuidos cliente LLM → MCP → backend
- Logging estructurado con redacción
- Dashboards y alertas que importan

### Capítulo 11 · Despliegue, multi-tenant y costes
- Aislamiento por tenant en datos y cómputo
- Estrategia blue/green con migraciones FHIR
- Costes: tokens LLM + cómputo MCP + almacenamiento PHI

### Capítulo 12 · Manual de incidentes
- Detección de prompt injection en producción
- Procedimiento de brecha PHI: 60 minutos críticos
- Postmortems y aprendizaje continuo

---

## Apéndices

- **A.** Especificación MCP relevante — [appendix-a-protocol-spec.md](appendix-a-protocol-spec.md)
- **C.** Troubleshooting — [appendix-c-troubleshooting.md](appendix-c-troubleshooting.md)
- **E.** Checklist de seguridad — [appendix-e-security-checklist.md](appendix-e-security-checklist.md)
- **F.** Glosario — [appendix-f-glossary.md](appendix-f-glossary.md)

---

## Estado de redacción

| Capítulo | Estado | Origen |
|---|---|---|
| Cap. 1 | Por escribir | Nuevo |
| Cap. 2 | Por escribir | Nuevo |
| Cap. 3 | Por escribir | Reusa material de [../prd3.md](../prd3.md) |
| Cap. 4 | Por escribir | Reusa diseño MediMind |
| Cap. 5 | Reescribir desde [10-chapter-security-authentication.md](10-chapter-security-authentication.md) | Parcial |
| Cap. 6 | Por escribir | Nuevo |
| Cap. 7 | Por escribir | Nuevo |
| Cap. 8 | Por escribir | Nuevo |
| Cap. 9 | Por escribir | Nuevo |
| Cap. 10 | Por escribir | Nuevo |
| Cap. 11 | Por escribir | Nuevo |
| Cap. 12 | Por escribir | Nuevo |
| Apéndices A, C, E, F | Revisar y depurar referencias a DataBridge/MarketPulse | Conservados |
