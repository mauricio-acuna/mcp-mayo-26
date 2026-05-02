# Outbound — Secuencia de contacto (consultoría)

> Plantillas reales, sin "como sabes" ni jerga. Personalizar siempre los `{huecos}`.

## Reglas

- **Volumen objetivo mes 1:** 100 contactos nuevos / semana, 50% cualificados.
- **Canal primario:** LinkedIn DM (mejor respuesta que email frío en 2026).
- **Canal secundario:** email a través de Hunter / Apollo cuando LinkedIn no responda.
- **Nunca pitch directo** en el primer mensaje. Vender llamada, no servicio.
- **Máximo 4 toques** por contacto. Después: archivar y reintentar en 6 meses.

## Filtro de cualificación

Antes de contactar, verificar **2 de 3**:

1. La empresa menciona IA generativa, agentes, copilotos o LLMs en su web/blog/LinkedIn los últimos 90 días.
2. El contacto tiene rol técnico de decisión: CTO, VP Eng, Head of Platform, CISO, Lead Architect.
3. La empresa tiene 30+ ingenieros (proxy: tamaño en LinkedIn 100-2.000 empleados).

Si no cumple 2/3: no merece la pena el toque.

## Lista de fuentes para construir el pipeline

- LinkedIn Sales Navigator (filtro: España + título + tamaño empresa).
- GitHub: buscar `mcp-server` + filtrar por contributors con localización ES/LatAm.
- Asistentes a meetups recientes: Madrid AI, Barcelona AI, Lisbon GenAI.
- Lectores que descarguen el lead magnet (warm leads, prioritarios).
- Comunidad MCP oficial (Discord) — observar quién pregunta cosas de seguridad.

---

## Secuencia LinkedIn (4 toques en 21 días)

### Toque 1 — Día 0 — Conexión + nota

> Hola {nombre}, te leo desde hace tiempo en {tema concreto del feed o post reciente}. Estoy investigando cómo equipos en {país/sector} están asegurando sus servidores MCP en producción y quería conectar. Sin pitch — solo me interesa el espacio.

**Aceptación esperada:** 25-35%.

### Toque 2 — Día 3 (si aceptó) — Mensaje de valor

> Gracias por aceptar. Te dejo dos cosas que igual te resultan útiles, sin coste:
>
> 1. Borrador del capítulo "Modelo de amenazas de un MCP server" → {link a Notion público o PDF en lead magnet}
> 2. Spec abierto OWASP MCP Top 10 → {link GitHub}
>
> Si {empresa} ya tiene MCP en producción o piloto, me encantaría hacerte 5 preguntas (literal, 25 min) para entender cómo lo estáis enfocando. A cambio comparto contigo el resumen agregado de las entrevistas. ¿Tienes hueco esta o la próxima semana?

**Conversión esperada a llamada:** 10-15%.

### Toque 3 — Día 10 (si no respondió) — Bump específico

> {nombre}, vi que {evento muy concreto: charla, post, ronda, lanzamiento, contratación}. Si en algún momento queréis una segunda mirada externa sobre la seguridad del stack MCP, me dices. Y si no, ningún problema — me callo.

### Toque 4 — Día 21 (si no respondió) — Cierre limpio

> Cierro hilo para no ser pesado. Te dejo el {link al spec OWASP-MCP-Top-10 o capítulo más reciente}. Si en 6 meses tiene sentido retomar, escríbeme tú. Suerte con {iniciativa concreta}.

**Tras toque 4:** archivar contacto, reintento en 6 meses con excusa nueva (ej. "lanzamos `mcp-audit` v0.1, recordé tu MCP en {empresa}").

---

## Secuencia email (cuando LinkedIn no funciona)

### Email 1 — Día 0

**Asunto:** seguridad MCP en {empresa}

> Hola {nombre},
>
> Vi que en {empresa} estáis trabajando con {algo concreto sobre IA / agentes / MCP — referencia verificable}.
>
> Estoy escribiendo material técnico en español sobre cómo endurecer servidores MCP antes de pasar a producción y querría escuchar cómo lo enfocáis. 25 minutos, sin pitch.
>
> A cambio te paso el borrador del capítulo de modelo de amenazas y el spec OWASP MCP Top 10 que estoy coordinando.
>
> ¿Esta o la próxima semana?
>
> {tu nombre}
> {url linkedin}

### Email 2 — Día 5

**Asunto:** Re: seguridad MCP en {empresa}

> {nombre}, sé que el inbox es lo que es. Tres líneas:
>
> – Llamada 25 min, sin venta.
> – Te paso material útil aunque no haya fit.
> – Si no es para ti, ¿alguien en {empresa} a quien deba escribir?

### Email 3 — Día 14

**Asunto:** último toque

> Sin presión {nombre}. Cierro este hilo. Si te interesa el material que mencioné, está aquí: {link único}. Suerte.

---

## Posts orgánicos LinkedIn (apoyo al outbound)

Publicar 2 por semana. Cada post genera 3-10 conversaciones entrantes que no requieren outbound.

### Plantillas que funcionan

**1. Hallazgo concreto:**
> Hoy vi un MCP server en producción donde el tool `query_database` aceptaba SQL crudo del LLM. El "control de acceso" era confiar en que el system prompt dijera "no leas datos de otros usuarios". {explicación de 3 líneas + fix}.

**2. Antipatrón nombrado:**
> 5 antipatrones que veo en cada audit MCP: 1) tools sobre-permisivos, 2) resources sin row-level security, 3) ... {desarrollo breve}.

**3. Trozo del libro/spec:**
> Capítulo 2 del libro acaba de salir en abierto: "Modelo de amenazas de un MCP server". Link en comentarios.

**4. Pregunta directa:**
> ¿Quién en tu equipo es responsable de que tu MCP server sea seguro? Si la respuesta es "nadie en concreto", ya tienes un hallazgo.

### Reglas

- Sin emojis decorativos.
- Sin hilos artificiales de 10 párrafos.
- Sin "engagement bait" ("comenta SÍ si te interesa").
- Una idea por post. Nombre y apellido siempre, no marca.

---

## Tracking mínimo

Hoja de cálculo o Notion con columnas:

```
| Fecha | Nombre | Empresa | Canal | Toque actual | Última respuesta | Estado | Notas |
```

Estados posibles: `enviado` / `aceptado` / `respondió` / `llamada agendada` / `cliente` / `archivado` / `reintento Q4`.

Revisar semanalmente:
- Aceptación % (objetivo 25%+).
- Respuesta % tras toque 2 (objetivo 10%+).
- Llamadas agendadas / semana (objetivo 3-5).

Si los ratios están por debajo dos semanas seguidas → revisar copy, no añadir más volumen.
