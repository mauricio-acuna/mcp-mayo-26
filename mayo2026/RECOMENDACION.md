# Recomendación y secuenciación

> Síntesis personal tras leer el repo y las cinco opciones. No es prescriptiva: depende de las respuestas a las preguntas abiertas en [00-REVISION.md](00-REVISION.md) §4.

## Recomendación principal: combo C + A, con E en el horizonte

### Por qué

- **C (consultoría)** monetiza ya el conocimiento que existe. Resuelve el problema de cash flow y valida el mercado con clientes que pagan, no con encuestas.
- **A (libro lean)** es marketing y portfolio para C. Reduce el alcance del libro actual a algo terminable en 12 semanas, no abierto.
- **E (toolkit OSS)** se planta en mes 6 una vez hay ingresos de C, como apuesta de medio plazo y diferenciador competitivo. La consultoría alimenta el catálogo de reglas del scanner.

Este combo evita los dos errores opuestos del repo actual:

1. Construir un libro de 200 págs sin saber si alguien lo comprará.
2. Saltar a SaaS con riesgo financiero alto sin validación de mercado.

## Por qué descarto B y D como **primer** paso

- **B (SaaS MediMind)** no es malo, pero requiere capital y full-time. Si tras 6 meses de C hay 2 clínicas pidiendo lo mismo repetidamente, **entonces** se justifica pivotar a B con mucho menos riesgo.
- **D (cohortes)** es buena opción pero requiere audiencia preexistente. Hoy no existe. A 6-9 meses de C+A+E, sí: la primera cohorte se nutre de los 500-1.000 emails de la lista y los clientes de consultoría.

## Roadmap propuesto (12 meses)

```
Mes  1 ──┬── Lanzar página de servicios (C) + landing libro (A)
         └── Outbound a 50 CTOs + 5 entrevistas validación

Mes  2 ──┬── Primer engagement quick-audit (€2.5k descuento launch)
         └── Capítulos 1-2 del libro publicados como artículos

Mes  3 ──┬── 2 engagements más a tarifa completa
         └── Lead magnet vivo, lista creciendo

Mes  4 ──┬── Spec pública "OWASP MCP Top 10" en GitHub (semilla de E)
         └── Publicación capítulos 4 y 6

Mes  5 ──┬── 3-4 clientes consultoría activos
         └── Capítulo 7 + apéndices

Mes  6 ──┬── Lanzamiento libro Gumroad + pre-venta a la lista
         └── MVP mcp-audit en GitHub (E semilla)

Mes  7-9 ── Estabilizar consultoría €15-20k/mes, 200-500 stars OSS,
            decidir si arrancar D (cohortes) o B (SaaS)

Mes 10-12 ── Si demanda B: piloto pagado en clínica.
            Si demanda D: cohorte piloto.
            Si demanda OSS: tier Cloud de mcp-audit.
```

## Métricas de decisión a 6 meses

| Métrica | Resultado | Acción |
|---|---|---|
| Ingresos consultoría | <€20k → revisar precio/canal | |
| | €20-60k → seguir, pulir oferta | |
| | >€60k → contratar 1 persona | |
| Lista email | <300 → contenido más agresivo | |
| | 300-1000 → lanzar libro | |
| | >1000 → lanzar D (cohortes) | |
| Stars `mcp-audit` | <100 → reposicionar / matar | |
| | 100-1000 → seguir invirtiendo | |
| | >1000 → priorizar E sobre todo | |

## Riesgos del combo recomendado

- **Dispersión.** Hacer C + A + E en paralelo es mucho. Mitigación: priorizar C estrictamente; A y E solo se trabajan en bloques semanales fijos.
- **Identidad de marca.** ¿"Consultor MCP-security" o "autor de libro MCP"? Resolverlo desde día 1: marca personal del autor + sub-marca del toolkit (`mcp-audit`).
- **HIPAA específico vs MCP-security genérico.** El libro y MediMind tiran hacia HIPAA; la consultoría y `mcp-audit` son agnósticos. Decidir si se sacrifica el ángulo HIPAA o si se mantiene como vertical premium dentro de la oferta general.

## Lo que debería pasar **antes** de cualquier opción

1. **5 entrevistas reales** (paso pendiente del PIVOTE). Sin esto, todas las opciones son apuestas. Bloquea una semana, contacta 30 personas en LinkedIn, haz las llamadas, transcribe, decide.
2. **Definir cuánto runway** (€ y meses) acepta el autor sin ingresos. Esto descarta opciones automáticamente:
   - <3 meses → solo C es viable.
   - 3-12 meses → C + A + E.
   - 12+ meses con capital → B también en la mesa.
3. **Decidir idioma definitivo.** Español-only limita techo. Español + inglés duplica esfuerzo. Recomendación: español primero, traducción al inglés solo cuando un activo (libro o curso) haya validado demanda.

## Resumen en una frase

**Vende consultoría desde el mes 1, escribe el libro corto como portfolio, planta `mcp-audit` como apuesta a 18 meses; archiva la idea del libro grande de 200 páginas.**
