# Sales page — Consultoría MCP Security

> Copy listo para pegar en una página simple (Carrd, Framer, Astro). Tono directo, sin jerga marketinera.

---

## Hero

# Tu servidor MCP filtra datos al LLM. Te ayudo a que no.

Audito, modelo amenazas y endurezco servidores Model Context Protocol antes de que un prompt injection o un tool sobre-permisivo te cueste un incidente.

→ **[Reservar llamada de 20 min](#contacto)**

---

## El problema

En 2026, casi todas las empresas medianas tienen ya un servidor MCP en producción o en piloto. Casi ninguna lo ha mirado con ojos de seguridad.

Los problemas que encuentro repetidamente:

- **Tools sobre-permisivos** que dan al LLM acceso a más datos o acciones de los necesarios.
- **Resources que filtran PII/PHI** sin redacción ni control de acceso por fila.
- **Prompts del servidor inyectables** desde contenido controlado por el usuario final.
- **Auditoría inexistente:** no hay forma de reconstruir qué llamada del LLM acabó en qué query a la base de datos.
- **Logs con datos sensibles** que tu equipo de SRE ve sin saberlo.
- **OAuth mal implementado** o ausente, con tokens compartidos entre usuarios.
- **Sin modelo de amenazas:** se desplegó "porque funciona", sin pensar qué pasa cuando alguien lo ataca.

---

## Cómo trabajo

Tres formatos productizados. Sin proyectos abiertos, sin estimaciones eternas.

### 🔍 MCP Quick-Audit — 5 días — €4.500

Para equipos que ya tienen un MCP server desplegado y quieren saber **dónde están**.

- Revisión del código fuente del servidor (tools, resources, prompts, auth).
- Modelo de amenazas STRIDE-MCP aplicado a tu superficie real.
- Informe priorizado con 15-25 hallazgos: severidad, impacto, fix sugerido.
- 1 sesión de 90 min para presentar resultados al equipo.

**Entregable:** PDF + repo privado con ejemplos de fix por hallazgo.

→ Ideal si: tienes 1-3 MCP servers internos y nunca pasaron por revisión.

---

### 🛡️ MCP Hardening Sprint — 4 semanas — €25.000

Para equipos que ya saben qué les falta y necesitan implementarlo.

- Implementación de los 10 controles más críticos de tu Quick-Audit (o de uno previo).
- OAuth 2.1 + scopes, redacción de PHI/PII, audit log inmutable, rate limiting, mTLS, gestión de claves.
- Pipeline CI con escaneo continuo (regla SARIF integrada en tu repo).
- Documentación interna y runbooks.

**Entregable:** PRs mergeables + documentación operativa.

→ Ideal si: ya hubo un audit (mío o de otro) y no tienes capacidad interna para ejecutar los fixes.

---

### 📋 Compliance Readiness — 6-8 semanas — €45.000

Para equipos que necesitan demostrar a un auditor (ENS, SOC 2, RGPD sanitario, DORA) que su MCP server cumple.

- Mapeo de controles regulatorios → implementación técnica concreta en tu MCP.
- Evidencias auditables (logs, configuraciones, políticas) recopiladas y trazables.
- Acompañamiento durante la auditoría externa.

**Entregable:** Carpeta de evidencias + matriz de cumplimiento + 2 sesiones con tu auditor.

→ Ideal si: vas a pasar una auditoría en los próximos 6 meses y tu MCP está dentro del alcance.

---

### 🔁 Asesor mensual — desde €2.500/mes

Retainer de 1 día/semana para equipos que quieren tener a alguien revisando decisiones de seguridad MCP a medida que las toman.

→ Ideal si: estás construyendo activamente y quieres no equivocarte.

---

## Por qué yo

- Autor del libro *MCP en Producción: Seguridad y Compliance* (en redacción, capítulos publicados en abierto).
- Mantenedor del spec **OWASP MCP Top 10** (proyecto comunitario).
- {N} servidores MCP auditados en {sectores}.
- {Cualquier credencial real: HIPAA, ENS, CISSP, experiencia previa, etc.}

> ⚠ Sustituir los huecos `{...}` por datos reales antes de publicar. Si todavía no hay engagements, omitir esta sección o dejar sólo "autor del libro y del spec".

---

## Casos típicos

### Fintech ES, 80 ingenieros
> "Teníamos un MCP server que daba acceso a histórico de transacciones a un copiloto interno. El audit destapó que cualquier prompt podía pedir transacciones de otros clientes porque el filtrado se hacía en el system prompt, no en el tool. 2 semanas para arreglarlo."

### Healthtech LatAm, 40 ingenieros
> "Necesitábamos pasar un audit de RGPD sanitario y nadie había mirado el MCP. Salió un mapeo de controles que el auditor aceptó tal cual."

> ⚠ Casos ilustrativos hasta tener testimonios reales. **No publicar como reales si no lo son.**

---

## Preguntas frecuentes

**¿Trabajas con clientes fuera de España?**
Sí. Toda LatAm y Europa. Reuniones por Zoom, contratos en español o inglés.

**¿Firmas NDA antes de hablar?**
Sí, mutuo, plantilla estándar.

**¿Subcontratas?**
No para entregables técnicos. Sí para revisión legal/regulatoria cuando aplica (con socio nombrado).

**¿Cuánto tiempo desde el "sí" hasta empezar?**
Quick-Audit: 1-2 semanas. Hardening / Compliance: 3-4 semanas (cola).

**¿Aceptas equity / partial payment?**
No para Quick-Audit (precio fijo). Para Hardening puede negociarse 70% cash + 30% equity en startups con ronda cerrada.

---

## Contacto

📧 **{email}**
💼 **LinkedIn: {url}**
📅 **Calendly: {url}**

→ Llamada de descubrimiento de 20 min, sin coste, sin compromiso.

---

## Notas para implementación

- Toda la página debe caber en una scroll, mobile-first.
- CTA principal repetido 3 veces (hero, después de servicios, footer).
- Foto profesional del autor en sidebar/footer (no stock).
- Si no hay casos reales: omitir la sección o sustituir por "Próximamente: testimonios de los primeros 3 clientes — únete a la lista para verlos".
- Añadir aviso legal mínimo (LSSI-CE: nombre, NIF, dirección postal o email de contacto).
