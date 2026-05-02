# Lead magnet — Especificación

> El PDF gratuito que se entrega al suscribirse. Es el activo más importante del funnel A: convierte tráfico en lista propia.

## Qué entrega

Dos archivos en un único enlace de descarga:

1. **`MCP-cap1-commodity.pdf`** — Capítulo 1 del libro completo, ~12-18 págs.
2. **`MCP-checklist-seguridad-v1.pdf`** — Versión condensada del Apéndice E, ~6-8 págs en formato checklist accionable.

Ambos con:
- Maquetación profesional consistente con la portada del libro.
- Contraportada con CTA: pre-venta del libro + servicios de consultoría.
- Pie de página: URL del repo OWASP MCP Top 10.

## Por qué estos dos y no otra cosa

- **Capítulo 1** es el "por qué" estratégico. Convence al lector de que el resto del libro merece la pena.
- **Checklist** es utilidad inmediata. El lector lo guarda y lo aplica esa misma semana → asocia tu marca a "alguien que me ayudó". Sólido en compartibilidad: alguien lo manda al equipo y trae 3-5 leads más.

Cualquier otra combinación (capítulo random, "guía gratis", whitepaper) tiene peor conversión documentada en el sector.

## Contenido del capítulo 1 (recordatorio del scope)

Reutiliza directamente lo escrito en [book-manuscript/preface.md](../../../book-manuscript/preface.md) y la sección 1 del TOC. Redacción objetivo:

1. **Qué cambió entre 2024 y 2026** (1.5 págs)
   - MCP como estándar de facto.
   - Generación de código por IA: tools, resources, JSON-RPC = commodity.
2. **Por qué los tutoriales perdieron valor** (2 págs)
   - Caso real: 5 prompts y tienes un MCP server funcional.
   - Lo que la IA no resuelve: amenaza, compliance, operación.
3. **Las tres áreas defendibles** (4 págs)
   - Seguridad de la superficie MCP.
   - Compliance accionable.
   - Operación a escala.
4. **Cómo usar este libro** (2 págs)
   - Qué capítulos para qué rol.
   - Cómo ejecutar el código del repo de acompañamiento.
5. **Una promesa honesta** (1 pág)
   - Qué encontrarás y qué no.
   - Por qué cuesta €19-29 y no €99.

## Contenido del checklist condensado

Versión printable de 1 página por área:

- ☐ Diseño de tools (10 ítems).
- ☐ Diseño de resources (8 ítems).
- ☐ Autenticación / autorización (10 ítems).
- ☐ Cifrado y manejo de PHI/PII (8 ítems).
- ☐ Auditoría y logging (6 ítems).
- ☐ Operación: rate limiting, multi-tenant, observabilidad (8 ítems).

Cada ítem en formato accionable: verbo en infinitivo + criterio binario verificable.

## Plumbing técnico

Pila mínima para no perder un mes en herramientas:

| Función | Herramienta |
|---|---|
| Landing | Carrd / Astro estático en Cloudflare Pages |
| Captura email | ConvertKit / Buttondown / MailerLite (free tier) |
| Doble opt-in | Activado (RGPD-compliant) |
| Entrega del PDF | Email automático tras confirmar opt-in, link a GCS/R2 firmado |
| Tracking | Plausible Analytics (sin cookies) |

## Email de confirmación (doble opt-in)

> **Asunto:** Confirma tu email para recibir el capítulo 1
>
> Hola,
>
> Para cumplir con el RGPD necesito que confirmes que quieres recibir mis emails. Un clic abajo y te llega el capítulo + checklist al instante.
>
> [ Confirmar y descargar → ]
>
> Si no fuiste tú, ignora este mensaje y no recibirás nada más.
>
> {tu nombre}

## Email de bienvenida (post-confirmación)

> **Asunto:** Aquí están — y qué viene ahora
>
> Hola {nombre o vacío},
>
> Aquí tienes lo prometido:
>
> 📄 [Capítulo 1 — MCP ya es commodity](link)
> ✅ [Checklist de seguridad MCP v1](link)
>
> **Qué hacer con esto:**
>
> 1. Lee el capítulo de un tirón (15 min).
> 2. Pasa el checklist por tu MCP server actual o el que estés diseñando.
> 3. Si encuentras algo gordo, responde a este email — me interesa saberlo.
>
> **Qué viene:** un email cada 2 semanas con un capítulo nuevo o un análisis de un MCP real. Sin newsletters de relleno. Cancelas con un clic abajo del email.
>
> Y si tu MCP necesita una segunda mirada externa, [aquí explico cómo trabajo](link sales page).
>
> Gracias por suscribirte,
> {tu nombre}

## Métricas a observar

| Métrica | Objetivo mes 1 | Objetivo mes 3 |
|---|---|---|
| Visitas únicas / mes | 500 | 2.000 |
| Tasa de conversión (visita → email) | 8-12% | 10-15% |
| Tasa de doble opt-in confirmado | >70% | >75% |
| Suscriptores netos acumulados | 50 | 250 |
| Reply rate al email de bienvenida | 3-8% | 5-10% |

Si la conversión visita → email está por debajo de 5% al mes 1: el problema es la landing, no el lead magnet. Iterar copy del hero antes de añadir más tráfico.
