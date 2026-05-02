# MCP en Producción

> Material de trabajo para el libro **MCP en Producción: Seguridad, Compliance y Operación a Escala** y para el caso de estudio asociado **MediMind MCP**.

**Estado:** en redacción / pre-lanzamiento.
**Idioma primario:** español.
**Última pivote estratégico:** abril 2026 — ver [PIVOTE_2026.md](PIVOTE_2026.md).

---

## ⚠️ Antes de hacer push

Este repositorio **debe crearse privado** en GitHub al inicio. Contiene:

- Material estratégico comercial vigente en [mayo2026/](mayo2026/) (precios, oferta de servicios, plan de outbound, plantillas de venta).
- Borradores de capítulos no publicados.
- Código de MediMind MCP en estado pre-producción, sin auditoría externa.

Cuando llegue el momento de abrir partes del trabajo (spec OWASP MCP Top 10, capítulo 1 como lead magnet, repo del libro), se moverán a repos **separados** públicos. Ver [HANDOFF.md](HANDOFF.md) §4.

Antes del primer commit, verifica:

```powershell
# No debe aparecer ningún archivo dentro de _local/
git status --ignored | Select-String "_local"

# No debe haber .env reales
Get-ChildItem -Recurse -Force -Filter .env | Where-Object { $_.FullName -notmatch '_local' }

# Confirmar que .gitignore está activo
git check-ignore -v _local/DESCARTADO
```

---

## Estructura del repo

```
mcp/
├── PIVOTE_2026.md            ← decisión estratégica vigente (abril 2026)
├── README.md                  ← este archivo
├── HANDOFF.md                 ← instrucciones para continuar el trabajo (humano u otro asistente IA)
├── LICENSE                    ← placeholder a definir
├── .gitignore
│
├── book-manuscript/           ← libro en redacción (ES)
│   ├── 00-front-matter.md
│   ├── preface.md
│   ├── how-to-read.md
│   ├── who-should-read.md
│   ├── table-of-contents.md   ← TOC vigente post-pivote
│   ├── 10-chapter-security-authentication.md
│   ├── appendix-a-protocol-spec.md
│   ├── appendix-c-troubleshooting.md
│   ├── appendix-e-security-checklist.md
│   ├── appendix-f-glossary.md
│   └── es/                    ← traducción/versión en español (consolidar)
│
├── medimind-mcp/              ← caso de estudio del libro (Python/FastAPI/FHIR)
│   ├── PRD.md
│   ├── README.md
│   ├── docker-compose.yml
│   ├── env.example
│   ├── compliance/            ← HIPAA checklist, BAA template, audit procedures
│   └── mcp-server/            ← código del servidor (estado: ~45%, sin tests)
│
├── mayo2026/                  ← REVISIÓN ESTRATÉGICA + EJECUCIÓN DEL COMBO C+A→E
│   ├── README.md              ← índice de opciones
│   ├── 00-REVISION.md         ← revisión crítica del estado tras pivote
│   ├── OPCION-A-libro-lean.md
│   ├── OPCION-B-medimind-saas.md
│   ├── OPCION-C-consultoria-mcp-security.md
│   ├── OPCION-D-curso-cohortes.md
│   ├── OPCION-E-toolkit-oss.md
│   ├── RECOMENDACION.md       ← combo recomendado + roadmap 12 meses
│   └── ejecucion/             ← entregables accionables del combo
│       ├── README.md
│       ├── 01-validacion-entrevistas.md
│       ├── 02-consultoria/    ← sales page, outbound, plantilla quick-audit
│       ├── 03-libro/          ← landing, lead magnet, esqueleto recortado
│       ├── 04-toolkit-oss/    ← spec OWASP MCP Top 10 v0.1
│       ├── 05-roadmap-y-metricas.md
│       └── semana-1/          ← kit de la primera semana de validación
│
└── _local/                    ← NO se sube a GitHub (gitignored)
    ├── validacion/            ← contactos, notas y config local de entrevistas
    ├── DESCARTADO/            ← proyectos archivados (DataBridge, MarketPulse, libro original)
    └── historico/             ← prdBASE.md, prd3.md (estrategia comercial cruda noviembre 2025)
```

## Por dónde empezar a leer (orden recomendado)

1. [PIVOTE_2026.md](PIVOTE_2026.md) — qué cambió y por qué.
2. [mayo2026/README.md](mayo2026/README.md) — opciones evaluadas y combo recomendado.
3. [mayo2026/RECOMENDACION.md](mayo2026/RECOMENDACION.md) — síntesis ejecutable.
4. [HANDOFF.md](HANDOFF.md) — qué hacer ahora y qué hacer después.
5. [mayo2026/ejecucion/semana-1/README.md](mayo2026/ejecucion/semana-1/README.md) — primera semana de validación, ejecutable de inmediato.
6. [SETUP_LOCAL.md](SETUP_LOCAL.md) — entorno local, comandos de verificación y espacio privado de validación.

## Estado a abril/mayo 2026

| Área | Estado |
|---|---|
| Decisión estratégica | ✅ Pivote completado |
| Validación de mercado | ⏳ Pendiente (semana 1 preparada, sin ejecutar) |
| Material del libro | 🟡 ~30% (front matter, ToC nuevo, 1 capítulo, 4 apéndices) |
| Código MediMind | 🟡 ~45% (estructura + security/encryption/audit; sin tools clínicos, sin tests) |
| Material de ejecución (mayo2026/) | ✅ Completo, listo para usar |
| Spec OWASP MCP Top 10 | 🟡 Borrador v0.1 escrito, no publicado todavía |
| Lista de email / canal | ❌ No existe |
| Primer cliente | ❌ Pendiente |

## Decisiones pendientes (críticas)

Marcadas en [HANDOFF.md](HANDOFF.md) §1. Se necesitan para desbloquear etapas posteriores:

- [ ] Runway disponible (€ y meses sin ingresos).
- [ ] Visibilidad del repo cuando salga la validación (privado / público / split en varios repos).
- [ ] Licencia final (libro vs código vs spec — ver [LICENSE](LICENSE)).
- [ ] Datos LSSI-CE para landing/sales page (nombre, NIF/CIF, email, dirección).
- [ ] Marca personal o sub-marca para `mcp-audit`.

## Licencia

Pendiente de decisión. Ver [LICENSE](LICENSE).

Como guía:
- **Código** (MediMind, futuro `mcp-audit`): Apache-2.0 o MIT.
- **Manuscrito del libro:** all-rights-reserved hasta lanzamiento; CC-BY-NC-ND para capítulos abiertos individuales.
- **Spec OWASP MCP Top 10:** CC-BY-4.0 (alineado con OWASP).

---

## Sincronización con HANDOFF.md

Este repositorio está documentado en detalle en [HANDOFF.md](HANDOFF.md). Asegúrate de leerlo antes de realizar cualquier cambio. Las secciones clave incluyen:

- **Arquitectura actual**: Descripción de los módulos y pipeline.
- **Configuración**: Propiedades clave y valores por defecto.
- **Pendientes priorizados**: Tareas críticas con contexto y pasos sugeridos.
- **Prompt para Codex**: Instrucciones para asistentes IA.

---

## Dependencias clave

- **Git**: necesario para control local y, más adelante, publicación en repos privados/públicos separados.
- **Python 3.11**: preparado en `.venv/` para el prototipo MediMind cuando toque trabajo técnico.
- **GitHub CLI (`gh`)**: instalado para crear repos separados cuando la validación dé VERDE.
- **Docker**: pendiente; no es necesario para la Etapa 1. Instalar solo al retomar MediMind técnico.

Ver [SETUP_LOCAL.md](SETUP_LOCAL.md) para comandos exactos y estado actual del equipo.
