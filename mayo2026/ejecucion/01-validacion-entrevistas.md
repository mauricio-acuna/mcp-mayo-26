# Validación — 5-7 entrevistas en semana 1

> Bloquea esto antes que cualquier otra cosa. Sin esta señal, todo lo demás es cabezonería.

## Objetivo

Responder a tres preguntas con personas reales, no con encuestas:

1. ¿Las empresas que están desplegando MCP **saben** que tienen un problema de seguridad?
2. ¿Estarían dispuestas a pagar **a quién** y **cuánto** por resolverlo?
3. ¿Lo prefieren resuelto vía consultoría, herramienta o formación?

Estas respuestas determinan si el combo C+A→E sigue vivo o si hay que pivotar a B (SaaS) o D (cohortes).

## Perfil de entrevistados

Buscar **8 perfiles distintos**, contactar 30, conseguir 5-7 llamadas.

| Perfil | Fuente para encontrarlos |
|---|---|
| CTO/CISO de fintech ES con 50-500 empleados | LinkedIn + Asociación Española de Fintech |
| Lead engineer de healthtech ES/LatAm | LinkedIn + AMETIC |
| Arquitecto de plataforma en banca/seguros ES | LinkedIn |
| Devrel/SRE de empresa con MCP server público | GitHub: buscar repos con `mcp-server` y autores ES |
| Consultor independiente de seguridad cloud | LinkedIn + ISMS Forum |
| Responsable IA en consultora top-tier (Accenture, Everis/NTT) | LinkedIn |
| CTO de scale-up SaaS ES (>€10M ARR) | StartupXplore + Crunchbase |
| Auditor SOC 2 / ENS que esté empezando con IA | ISMS Forum + ISACA Madrid |

## Mensaje de contacto (copia-pega)

**LinkedIn / DM corto:**

> Hola {nombre}, estoy investigando cómo equipos en España están abordando la seguridad de los servidores MCP que ya tienen en producción (o en planes 2026). No vendo nada — son 25 minutos de llamada para entender el panorama y comparto contigo el resumen agregado al final. ¿Tienes hueco esta o la próxima semana?

**Email frío:**

> Asunto: 25 min sobre seguridad de MCP en {empresa}
>
> Hola {nombre},
>
> Estoy escribiendo material técnico (en español) sobre cómo asegurar y operar servidores MCP en producción, y me interesaría escuchar cómo lo estáis enfocando en {empresa}.
>
> No vendo nada en esta llamada. A cambio del tiempo, te paso:
> – El borrador del capítulo "Modelo de amenazas de un MCP server".
> – Acceso early al checklist de seguridad MCP que estoy preparando.
>
> ¿Te encaja una llamada de 25 minutos esta o la próxima semana?
>
> Gracias,
> {tu nombre}

## Guion (25 min, no más)

### Bloque 0 — Encuadre (2 min)
- Agradecer.
- Recordar: no se vende nada, es investigación.
- Pedir permiso para grabar (transcripción local, no se publica).

### Bloque 1 — Contexto del entrevistado (5 min)
1. Cuéntame tu rol y qué tipo de equipo lideras.
2. ¿Qué uso de IA generativa tenéis hoy en producción? ¿Y previsto a 12 meses?
3. ¿Ya tenéis algún servidor MCP en producción, en piloto, o solo en evaluación?

### Bloque 2 — Dolor real (8 min — el bloque clave)
4. Cuando piensas en "esto tiene que pasar a producción de forma segura", ¿qué es lo primero que te preocupa?
5. ¿Quién hoy es responsable de revisar la seguridad de un MCP server en tu organización? ¿Tiene formación específica o lo improvisa?
6. ¿Habéis tenido ya algún incidente o casi-incidente relacionado con tools MCP, prompt injection o filtrado de datos al LLM?
7. ¿Tenéis algún requerimiento regulatorio (ENS, RGPD, DORA, sectorial) que ya os obligue o vaya a obligar a documentar la seguridad MCP?

### Bloque 3 — Soluciones que están considerando (5 min)
8. ¿Qué estáis haciendo hoy para mitigar esos riesgos? (interno / consultora / herramienta / nada)
9. Si mañana existiera una herramienta open-source que escaneara tu MCP server y detectara antipatrones de seguridad, ¿la usarías? ¿En qué momento del SDLC?
10. ¿Y un servicio externo de auditoría de 1 semana con informe entregable? ¿En qué rango de precio te chirriaría?

### Bloque 4 — Formato y canal (3 min)
11. Cuando aprendes algo técnico nuevo y especializado, ¿qué formato prefieres? (libro, curso en vivo, vídeo, blog, conferencia)
12. ¿En qué idioma consumes contenido técnico avanzado? ¿El español te aporta valor o es indistinto?

### Bloque 5 — Cierre y red (2 min)
13. ¿Hay alguien más con quien debería hablar sobre esto?
14. ¿Te interesa estar en la lista de pre-lanzamiento del libro/herramienta?

## Cómo registrar y decidir

Usar una tabla por entrevistado:

```
| ID | Empresa | Rol | MCP en prod? | Dolor declarado | Pagaría por... | Idioma pref |
```

### Criterios de decisión (al cerrar la 5ª entrevista)

- **Verde — seguir con C+A→E:** ≥3/5 declaran dolor concreto en seguridad MCP **y** ≥2/5 dicen que pagarían por consultoría o herramienta.
- **Ámbar — ajustar ángulo:** dolor existe pero no en MCP-security per se, sino en algo adyacente (compliance IA en general, gobernanza LLM, seguridad de agentes). Reescribir oferta sin tirar el trabajo hecho.
- **Rojo — pivotar:**
  - Si nadie tiene MCP en producción ni planes claros → re-evaluar timing (esperar 6 meses) o moverse a E (toolkit OSS) como apuesta a futuro.
  - Si todos consumen en inglés y el español no aporta → reabrir libro original en inglés.
  - Si el dolor real está en clínicas y nadie en otros sectores lo reconoce → opción B (SaaS MediMind) gana peso.

## Time-box

- Día 1: enviar 30 mensajes.
- Días 2-5: agendar y hacer las llamadas.
- Día 6: sintetizar (no más de 2 págs de notas).
- Día 7: decidir verde/ámbar/rojo y comunicarlo.

**Si en el día 7 no hay decisión escrita, parar todo el resto del plan hasta tenerla.**
