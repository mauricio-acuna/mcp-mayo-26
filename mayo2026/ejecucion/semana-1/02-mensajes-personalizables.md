# Mensajes personalizables — Semana 1

> Plantillas con huecos `{...}` que **siempre** se rellenan antes de enviar. Sin huecos sin rellenar.

## Anatomía de la personalización

Cada mensaje tiene 3 huecos:

1. `{tema concreto}` — algo que el contacto publicó, dijo o construyó en los últimos 90 días. Verificable y referenciable.
2. `{país/sector específico}` — más estrecho que "España" o "tech": "fintech española post-MiCA", "healthtech mexicano", "banca privada europea".
3. `{empresa}` o `{evento concreto}` — referencia a algo de su contexto presente.

Si no encuentras los 3 en 90 segundos: ese contacto no merece el mensaje. Cambia de contacto, no de mensaje.

---

## Variante A · LinkedIn Toque 1 (conexión)

**Para perfiles donde tienes una pieza de contenido reciente que referenciar:**

> Hola {nombre}, leí tu {post / charla / repo / artículo} sobre {tema concreto} y me interesó mucho el ángulo de {detalle específico, no genérico}. Estoy investigando cómo equipos en {país/sector específico} están asegurando sus servidores MCP en producción y quería conectar contigo. Sin pitch — me interesa el espacio.

**Para perfiles sin contenido público reciente pero con rol claro:**

> Hola {nombre}, vi que lideras {equipo concreto} en {empresa} y que tocáis {área concreta donde la IA ya entró}. Estoy haciendo investigación sobre cómo equipos en {país/sector} están abordando la seguridad de sus servidores MCP. Conectamos? No vendo nada, solo me interesa el panorama.

**Para perfiles de devrel / contributors OSS de proyectos MCP:**

> Hola {nombre}, vi tu contribución a {proyecto concreto, ej. servidor MCP en GitHub}. Estoy escribiendo material en español sobre seguridad de MCP en producción y querría conectar para intercambiar perspectivas. Sin agenda comercial.

---

## Variante B · LinkedIn Toque 2 (post-aceptación, día +3)

> Gracias por aceptar, {nombre}.
>
> Te dejo dos cosas, sin coste y sin pedir nada a cambio:
>
> 1. Borrador del capítulo "Modelo de amenazas de un MCP server" — {link al PDF en Notion público o R2}.
> 2. Spec abierto **OWASP MCP Top 10** que estoy coordinando — {link GitHub}.
>
> Si en {empresa} ya tenéis algún MCP server en producción, en piloto o en evaluación: me encantaría hacerte 5 preguntas (literal, 25 min) para entender cómo lo enfocáis. A cambio comparto contigo el agregado de las entrevistas al final.
>
> ¿Tienes hueco {franja concreta, ej. "miércoles 12:30 o jueves 16:00"}?

> 💡 Ofrecer 2 huecos concretos sube la tasa de respuesta vs "cuando puedas". Pero deja que el Calendly también esté disponible: `{calendly url}`.

---

## Variante C · Email frío (cuando no aceptan en LinkedIn)

**Asunto** (probar A/B después de 15 envíos):
- A: `seguridad MCP en {empresa}`
- B: `25 min sobre tu MCP server`

> Hola {nombre},
>
> Vi que en {empresa} estáis trabajando con {referencia verificable: producto, charla, oferta de empleo, post}.
>
> Estoy escribiendo material técnico en español sobre cómo asegurar servidores Model Context Protocol antes y durante producción, y querría escuchar cómo lo estáis enfocando. 25 minutos por Zoom, sin pitch.
>
> A cambio te paso:
> – Borrador del capítulo "Modelo de amenazas de un MCP server".
> – Acceso early al spec OWASP MCP Top 10.
>
> Si te encaja: {calendly url} — o respóndeme con un hueco que te vaya.
>
> Gracias,
> {tu nombre}
> {linkedin url}

---

## Variante D · Bump (día +10 si no responden)

**LinkedIn:**

> {nombre}, vi que {evento muy concreto: lanzasteis X / contratasteis a Y / publicaste Z}. Si en algún momento queréis una segunda mirada externa sobre la seguridad del stack MCP en {empresa}, me dices. Si no, ningún problema — me callo.

**Email:**

> Hola {nombre}, sé que el inbox es lo que es. Tres líneas:
>
> – Llamada de 25 min, sin venta.
> – Te paso material útil aunque no haya fit.
> – Si no eres tú, ¿alguien en {empresa} a quien deba escribir?

---

## Variante E · Cierre limpio (día +21)

> Cierro hilo para no ser pesado. Te dejo el spec OWASP MCP Top 10 por si en algún momento te resulta útil: {link}. Si en 6 meses tiene sentido retomar, escríbeme. Suerte con {iniciativa concreta}.

---

## Plantilla de email post-llamada (a enviar en los 60 min siguientes)

**Asunto:** Lo que comentamos + lo prometido

> {nombre},
>
> Gracias por los 25 minutos. Apunto lo que te llevas:
>
> 📄 Capítulo 1 del libro: {link}
> ✅ Checklist de seguridad MCP: {link}
> 🔗 Spec OWASP MCP Top 10: {link}
>
> {1-2 frases referenciando algo concreto que él/ella dijo: "tu punto sobre X me parece muy fino, lo voy a meter en el cap. 3"}.
>
> Cuando tenga el agregado de las entrevistas (en ~2 semanas) te lo paso. Si en algún momento queréis profundizar en {algo concreto que mencionó como dolor}, ya sabes dónde encontrarme.
>
> Y si conoces a alguien más con quien debiera hablar sobre esto, te agradezco la presentación.
>
> {firma}

---

## Reglas de oro

1. **Cero copia-pega sin personalizar.** Si los 3 huecos no están rellenos: no se envía.
2. **Sin emojis decorativos.** Cero. Resta seriedad técnica.
3. **Sin "espero que estés bien".** Va directo al grano.
4. **Sin links de tracking visibles.** Si usas UTMs, que el usuario no los vea.
5. **Una pregunta por mensaje.** Más de una y no responde a ninguna.
6. **Si alguien responde "no tengo MCP todavía":** agradécelo, mándale igual el material y pídele 1 contacto. No insistas en la llamada.
