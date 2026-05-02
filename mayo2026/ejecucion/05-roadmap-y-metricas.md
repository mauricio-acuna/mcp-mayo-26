# Roadmap operativo 12 meses + dashboard de métricas

> Versión accionable del roadmap propuesto en [RECOMENDACION.md](../RECOMENDACION.md). Pensado para revisar cada lunes (15 min) y a fondo cada 30 días.

## Hipótesis de capacidad

- 1 persona, dedicación full-time o equivalente.
- Sin equipo todavía.
- Capacidad útil semanal: ~30h productivas.
- Asignación objetivo:
  - **50%** consultoría (engagements + outbound + sales calls).
  - **25%** libro + lista (capítulos + emails).
  - **15%** OSS (spec OWASP-MCP-Top-10 → `mcp-audit` desde mes 6).
  - **10%** admin / aprendizaje / colchón.

Si la consultoría se dispara, sube a 70/15/10/5 y se acepta retraso del libro.

---

## Roadmap mes a mes

### Mes 1 — Validar y armar plataforma

**Objetivo:** decisión verde/ámbar/rojo + plataforma online.

- ✅ Ejecutar [01-validacion-entrevistas.md](01-validacion-entrevistas.md) — semana 1.
- ✅ Publicar sales page consultoría — semana 2.
- ✅ Publicar landing libro + lead magnet — semana 2.
- ✅ Empezar outbound (50 contactos / semana) — semana 3.
- ✅ Publicar borrador 0.1 OWASP MCP Top 10 en GitHub — semana 3.
- ✅ Capítulo 1 maquetado como lead magnet — semana 4.

**Hito:** primera llamada de venta agendada.

### Mes 2 — Primer ingreso

**Objetivo:** cerrar primer Quick-Audit.

- Cerrar 1 Quick-Audit (puede ser a precio launch €2.500).
- Ejecutar engagement (semanas 2-3).
- Publicar capítulo 2 a la lista.
- Mantener outbound 50/semana.
- Publicar 8 posts LinkedIn (2/semana).

**Hito:** primera factura emitida.

### Mes 3 — Repetibilidad

**Objetivo:** segundo y tercer cliente. Confirmar que no fue suerte.

- 2 Quick-Audits adicionales (uno a precio completo €4.500).
- Iterar la plantilla de informe con aprendizajes del primer engagement.
- Capítulo 3 publicado.
- Lista de email: 250 suscriptores.
- Repo OWASP MCP Top 10: 50 stars + 3 contribuidores.

**Hito:** €10k+ facturados acumulados.

### Mes 4 — Posicionamiento

**Objetivo:** dejar de prospectar a frío.

- Charla en 1 evento técnico (CommitConf, AperiTech, comunidad OWASP local).
- 1 colaboración en podcast técnico ES.
- Webinar gratuito propio "Top 5 fallos de seguridad MCP en 2026".
- Capítulo 4.
- Primer Hardening Sprint contratado (€25.000).

**Hito:** >50% de leads vienen de inbound o referidos.

### Mes 5 — Operación

**Objetivo:** profesionalizar entrega sin contratar todavía.

- Plantillas, scripts y herramientas internas pulidas.
- Contratar revisor técnico externo del libro (€800-1.000).
- Capítulo 5.
- Empezar diseño del MVP de `mcp-audit` (esqueleto + 5 reglas piloto).
- Lista: 500 suscriptores.

**Hito:** 1 día/semana liberado para escribir y hacer OSS.

### Mes 6 — Lanzamiento del libro + checkpoint mayor

**Objetivo:** vender el libro + tomar decisión sobre B/D.

- Apéndices E y F revisados y maquetados.
- Pre-venta del libro a la lista (€19) — objetivo 80 ventas (~€1.500).
- Lanzamiento general (€29).
- MVP `mcp-audit` v0.1 publicado en GitHub.
- **Checkpoint a 6 meses:** revisar dashboard (ver §siguiente). Decidir explícitamente: ¿se mantiene C+A→E? ¿se inicia D (cohorte) en mes 9? ¿se retoma B?

**Hito:** libro vendido + decisión documentada para meses 7-12.

### Mes 7-9 — Escalar lo que funciona

Ramificación según resultado del checkpoint:

**Si C escala (>€20k/mes):**
- Subir tarifas un 20%.
- Considerar contratar 1 ingeniero junior para hardening sprints.
- Mantener libro en modo "actualizaciones".
- `mcp-audit` v0.2 con 30 reglas.

**Si C estable pero no crece:**
- Lanzar D (cohorte piloto en mes 9, 10-15 alumnos a €390).
- Diversificar ingreso.

**Si C estancado y comunidad OSS arranca:**
- Volcar más esfuerzo en `mcp-audit`.
- Buscar partner técnico para acelerar.

### Mes 10-12 — Activo a 18-24 meses

**Objetivo:** transformar la operación de servicios en algo con valor residual.

- `mcp-audit` v1.0 + lanzamiento del tier Cloud (€49/mes Team).
- Caso de éxito público de 1 cliente (con permiso).
- Charla en evento internacional (KubeCon, OWASP Global, Devoxx).
- Versión 2.0 del libro con aprendizajes de los engagements (gratis para compradores 1.0).
- Cierre de año: 200+ stars OSS, lista 1.500+, ingresos anuales €120-200k.

---

## Dashboard de métricas

> Hoja única (Notion / Google Sheets / spreadsheet). Actualización semanal en 5 min. Revisión mensual con escritura.

### Métricas de tracción (semanales)

| Métrica | Definición | Objetivo M1 | M3 | M6 | M12 |
|---|---|---|---|---|---|
| Contactos out enviados | Mensajes nuevos / semana | 50 | 50 | 30 | 10 |
| Aceptación LinkedIn | % aceptan conexión | 25% | 30% | 35% | 40% |
| Llamadas agendadas | Por semana | 1-2 | 3-5 | 3-5 | 2-3 |
| Conversión llamada → propuesta | % | 30% | 40% | 50% | 50% |
| Conversión propuesta → cierre | % | 30% | 40% | 50% | 60% |
| Suscriptores email netos | Acumulado | 50 | 250 | 500 | 1.500 |
| Conversión visita → email | % landing | 8% | 10% | 12% | 15% |
| Stars repo OSS | Acumulado | 0 | 50 | 200 | 1.000 |
| Posts LinkedIn / semana | Publicados | 2 | 2 | 2 | 1 |

### Métricas de negocio (mensuales)

| Métrica | Definición | M3 | M6 | M12 |
|---|---|---|---|---|
| MRR consultoría | Ingreso recurrente (retainers) | €0 | €2.500 | €7.500 |
| Ingreso engagement / mes | Quick-Audit + Hardening | €4.500 | €10.000 | €15.000 |
| Ingreso libro / mes | Ventas Gumroad | €0 | €1.500 (lanzamiento) | €300 |
| Ingreso OSS Cloud / mes | mcp-audit Cloud | €0 | €0 | €1.500 |
| **Ingreso total mes** | | **€4.500** | **€14.000** | **€24.500** |
| Acumulado anual | | €10.000 | €60.000 | €175.000 |

### Métricas de calidad (trimestrales)

| Métrica | Cómo medir | Objetivo |
|---|---|---|
| NPS clientes consultoría | Encuesta post-engagement | >50 |
| Re-engagement rate | % clientes que vuelven en 6m | >30% |
| Referidos / cliente | Promedio | >0.5 |
| Tiempo medio de venta | Primer contacto → contrato | <30 días |
| % capítulos del libro publicados a tiempo | vs calendario | >75% |
| Contribuidores externos al spec OSS | Acumulado | >5 al mes 6 |

### Métricas de bienestar (mensuales) — NO opcional

| Métrica | Cómo medir | Objetivo |
|---|---|---|
| Horas trabajadas / semana promedio | Toggl o equivalente | <50h |
| Días sin descanso > 1 día | Conteo | <7/mes |
| Sensación de tracción (1-10) | Diario subjetivo | >6 |

Si dos meses seguidos: trabajo >55h/sem o tracción <5 → reducir scope, no aumentar esfuerzo.

---

## Reglas de revisión

### Lunes (15 min)
- Mirar números de la semana anterior.
- Decidir foco de la semana actual (1 prioridad consultoría + 1 libro/OSS).
- Mover tarjetas en kanban personal.

### Primer lunes del mes (60 min)
- Rellenar dashboard mensual.
- Comparar con objetivos.
- Decidir 1 ajuste para el mes (no más).

### Mes 6 y mes 12 (medio día)
- Checkpoint mayor: ¿el plan sigue siendo el correcto?
- Documentar decisión por escrito (qué se mantiene, qué cambia, por qué).
- Compartir con un asesor externo o mentor para sanity check.

---

## Señales rojas que disparan replanteamiento

| Señal | A qué mes esperar | Acción |
|---|---|---|
| 0 Quick-Audits cerrados | Mes 3 | Revisar pricing, copy o canal. Si mes 4 sigue 0: pivotar. |
| Lista <100 suscriptores | Mes 3 | El lead magnet o la landing fallan. Iterar. |
| Ratio aceptación LinkedIn <15% | Mes 2 | Mensaje de outreach roto. Reescribir. |
| 0 stars en repo OSS tras 60 días | Mes 3 | Fallo de distribución. Hacer Show HN, pedir feedback en Discord MCP, postear en r/MCP. |
| Tracción subjetiva <4 dos meses | Cualquier mes | Pausar 1 semana. Hablar con mentor. Decidir si seguir. |

## Señales verdes que aceleran

| Señal | A qué mes | Acción |
|---|---|---|
| 5+ Quick-Audits cerrados | Mes 4 | Subir tarifa 20%. |
| Pipeline >€50k cualificado | Mes 5 | Empezar a buscar contratación. |
| Repo OSS >500 stars | Mes 6-9 | Acelerar `mcp-audit` Cloud. |
| 3+ peticiones del mismo vertical | Cualquier mes | Empaquetar oferta vertical específica. |
