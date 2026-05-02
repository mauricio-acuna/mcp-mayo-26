# Plan de Pivote — Abril 2026

> Documento de decisión estratégica. Reemplaza a [prdBASE.md](prdBASE.md) y a [BOOK_PROMPT.md](DESCARTADO/BOOK_PROMPT.md) como guía vigente del proyecto.

---

## 1. Contexto

El plan original (noviembre 2025) asumía que MCP era una tecnología emergente con escasa competencia y que un libro de 400-500 páginas con tres casos (DataBridge, MarketPulse, MediMind) tendría ventaja de *early mover* y márgenes premium en KDP.

A abril de 2026 esa tesis ya no se sostiene:

- MCP es estándar de facto (adoptado por OpenAI, Google, Microsoft, Anthropic). Hay registries oficiales y miles de servidores públicos.
- La generación de código por IA convierte en commodity el contenido tipo *"escribe tu primer MCP server"*: tools, resources, prompts, JSON-RPC, Prisma, Docker compose.
- DataBridge compite con conectores oficiales de Snowflake, Databricks, Salesforce, SAP.
- MarketPulse compite con Bloomberg/Refinitiv MCPs nativos y requiere licencias de datos caras.
- MediMind sigue protegido por la barrera regulatoria (HIPAA, FHIR, auditoría) — nicho defendible.
- El contenido en español sobre MCP empresarial sigue siendo escaso.

## 2. Decisión

| Componente | Decisión |
|---|---|
| Libro genérico "Building MCP Servers" en inglés (KDP, $39-59) | ❌ Descartar |
| Proyecto DataBridge MCP | ❌ Archivar |
| Proyecto MarketPulse MCP | ❌ Archivar |
| Proyecto MediMind MCP | ✅ Continuar como producto/caso ancla |
| Material de seguridad y compliance del libro | ✅ Conservar y expandir |
| Versión en español del libro | ✅ Reenfocar como producto principal |

## 3. Nuevo producto

**Título de trabajo:** *"MCP en Producción: Seguridad, Compliance y Operación a Escala"*  
**Caso de estudio único:** MediMind MCP (HIPAA + FHIR R4).  
**Formato:** libro corto (180-220 págs) + repositorio de código + curso opcional.  
**Idioma primario:** Español. Traducción a inglés solo si el ES valida demanda.  
**Canales:** Gumroad / Leanpub / Maven, no KDP como canal único.

### Pilares de contenido (los que la IA aún no genera bien)

1. Diseño de superficie MCP segura: principio de menor privilegio en tools y resources.
2. Compliance accionable: HIPAA, GDPR, SOC 2 traducidos a controles concretos en un MCP server.
3. PHI / datos sensibles: cifrado en tránsito y reposo, tokenización, redacción en logs.
4. Auditoría y trazabilidad de llamadas LLM → MCP → datos.
5. Observabilidad: métricas, traces distribuidos, alertas que importan.
6. Operación: blue/green, rate limiting, multi-tenant, costes.
7. Caso completo MediMind end-to-end como hilo conductor.

## 4. Qué se conserva en el repo

```
mcp/
├── PIVOTE_2026.md                 ← este documento
├── prdBASE.md                     ← contexto histórico de mercado
├── prd3.md                        ← PRD MediMind (vigente)
├── medimind-mcp/                  ← producto activo
└── book-manuscript/
    ├── 00-front-matter.md
    ├── preface.md / how-to-read.md / who-should-read.md
    ├── table-of-contents.md       ← se reescribe (ver §6)
    ├── 10-chapter-security-authentication.md
    ├── appendix-a-protocol-spec.md
    ├── appendix-c-troubleshooting.md
    ├── appendix-e-security-checklist.md   ← núcleo del nuevo libro
    ├── appendix-f-glossary.md
    └── es/  (mismos archivos)
```

## 5. Qué se mueve a `DESCARTADO/`

Archivado, no borrado, por si se rescata material puntual.

- `databridge-mcp/`, `marketpulse-mcp/`
- `prd1.md` (DataBridge), `prd2.md` (MarketPulse)
- `BOOK_PROMPT.md`, `GUIA_TECNICA_COMPLETA.md`, `index.html`
- `book-manuscript/`: capítulos 01–09, 11, 12–14, 15
- `book-manuscript/`: `amazon-listing.md`, `back-cover.md`, `appendix-b-api-docs.md`, `appendix-d-performance-benchmarks.md`
- Equivalentes en `book-manuscript/es/`

## 6. Nuevo TOC propuesto (borrador)

Ver [book-manuscript/table-of-contents.md](book-manuscript/table-of-contents.md) tras la reescritura.

```
Parte I — Por qué este libro (abril 2026)
  1. MCP ya es commodity: dónde está el valor real
  2. Modelo de amenazas de un servidor MCP en producción

Parte II — Caso MediMind
  3. Dominio: workflow clínico, FHIR R4, PHI
  4. Diseño de la superficie MCP (tools, resources, prompts mínimos)
  5. Identidad, autenticación y autorización (OAuth2 + scopes clínicos)
  6. Cifrado, tokenización y redacción de PHI

Parte III — Compliance accionable
  7. HIPAA traducido a controles técnicos
  8. Auditoría y trazabilidad LLM → MCP → EHR
  9. GDPR / SOC 2 cuando aplica

Parte IV — Operación
  10. Observabilidad (métricas, traces, logs sin PHI)
  11. Despliegue, multi-tenant y costes
  12. Manual de incidentes

Apéndices
  A. Especificación MCP relevante (referencia)
  C. Troubleshooting
  E. Checklist de seguridad
  F. Glosario
```

## 7. Próximos pasos

1. Validar el ángulo con 5 entrevistas a CTOs/arquitectos de health-tech en español.
2. Reescribir `table-of-contents.md` y `preface.md` al nuevo enfoque.
3. Redactar capítulo 1 ("MCP ya es commodity") como muestra para landing.
4. Publicar landing simple para captar emails con el capítulo 1 como lead magnet.
5. Iterar sobre MediMind para que su código respalde cada capítulo del libro.
