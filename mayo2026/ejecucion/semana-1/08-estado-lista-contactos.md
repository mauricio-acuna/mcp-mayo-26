# Estado agregado de lista de contactos

> No incluir nombres ni empresas concretas aqui. La lista real vive en
> `_local/validacion/semana-1/01-tracker-contactos.local.md`.

**Fecha:** 2026-05-08

## Preparacion

| Elemento | Estado |
|---|---|
| Fuentes de busqueda | Completo |
| Organizaciones objetivo | Completo |
| Workflow de investigacion de personas | Completo |
| Tracker local con 30 filas | Completo |
| Mensajes locales generados | Completo |
| Revision automatica de mensajes | Preparada por script |
| Plan local de envio por lotes | Preparado por script |
| Config local con firma, franjas y links | Pendiente |
| Envio de mensajes | Pendiente |
| Llamadas agendadas | Pendiente |
| Llamadas realizadas | Pendiente |

## Distribucion cualitativa

La lista local cubre:

- Healthtech / datos clinicos / FHIR.
- Fintech / insurtech / activos digitales.
- MCP real en empresas de developer tooling, observabilidad e infraestructura.
- Seguridad, GRC, IAM, auditoria y gobierno de IA.
- Consultoria top-tier con cyber / trusted AI.

## Siguiente bloqueo

Antes de enviar mensajes falta rellenar `_local/validacion/semana-1/CONFIG.local.md`:

- Nombre de firma.
- LinkedIn URL.
- Calendly / Cal.com URL.
- Dos franjas concretas.
- Link al borrador de capitulo o recurso prometido.
- Link al spec / checklist si se va a ofrecer.

Despues:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\generate-mensajes-validacion.ps1
powershell -ExecutionPolicy Bypass -File .\tools\check-mensajes-validacion.ps1
powershell -ExecutionPolicy Bypass -File .\tools\generate-plan-envio-validacion.ps1
```

Revisar `_local/validacion/semana-1/mensajes-generados.local.md` a mano antes
de enviar. Si un mensaje parece generico, corregir la personalizacion o
descartar el contacto.
