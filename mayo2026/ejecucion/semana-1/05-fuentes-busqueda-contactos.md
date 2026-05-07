# Fuentes de busqueda de contactos - Semana 1

> Complemento operativo de `01-tracker-contactos.md`. No reemplaza el tracker:
> sirve para encontrar candidatos en bloques de 90 minutos sin improvisar.

## Regla de seleccion

Cada contacto debe cumplir al menos 2 de 3:

- Rol con decision tecnica, seguridad, plataforma, IA o compliance.
- Empresa con IA en produccion, regulacion fuerte o equipo tecnico relevante.
- Senal publica reciente que permita personalizar el mensaje en menos de 90 segundos.

Si no hay senal personalizable, descartar y pasar al siguiente.

## Fuentes por perfil

| Perfil | Fuente inicial | Que buscar |
|---|---|---|
| CTO/CISO fintech ES | AEFI | Empresas asociadas, verticales PayTech, RegTech, Lending, InsurTech, activos digitales. |
| Lead engineer healthtech ES/LatAm | AMETIC / salud digital / LinkedIn | Healthtech, FHIR, interoperabilidad, IA clinica, software sanitario. |
| Arquitecto plataforma banca/seguros | LinkedIn + bancos/aseguradoras ES | Platform engineering, cloud security, arquitectura, genAI, DORA. |
| DevRel/SRE con MCP publico | GitHub / MCP Registry | Repos con `mcp-server`, observabilidad, infra, developer tools. |
| Consultor seguridad cloud | ISMS Forum / LinkedIn | GRC, cloud security, auditoria, gobierno IA, ENS, ISO 27001, SOC 2. |
| Responsable IA en consultora | LinkedIn | GenAI, AI governance, seguridad de agentes, Responsible AI. |
| CTO scale-up SaaS ES | Startup directories / LinkedIn | SaaS B2B, ARR alto, equipos 30+ ingenieros, IA incorporada al producto. |
| Auditor SOC 2 / ENS con IA | ISMS Forum / ISACA / LinkedIn | ENS, ISO 27001, SOC 2, DORA, AI Act, auditoria de proveedores IA. |

## URLs base

- AEFI: https://www.asociacionfintech.es/
- LinkedIn AEFI: https://www.linkedin.com/company/asociaci%C3%B3n-espa%C3%B1ola-de-fintech-e-insurtech-aefi/
- ISMS Forum: https://www.ismsforum.es/
- ISMS Forum - Grupo IA: https://master.ismsforum.es/inteligencia-artificial/
- LinkedIn ISMS Forum: https://www.linkedin.com/company/ismsforum/
- MCP Registry GitHub server: https://github.com/mcp/github/github-mcp-server
- MCP Registry Netdata server: https://github.com/mcp/netdata/mcp-server

## Busquedas listas

### LinkedIn

```text
site:linkedin.com/in CTO fintech España IA seguridad
site:linkedin.com/in CISO fintech España DORA IA
site:linkedin.com/in "Head of Platform" España "generative AI"
site:linkedin.com/in "AI governance" España seguridad
site:linkedin.com/in "ENS" "IA" "ISO 27001" España
site:linkedin.com/in "FHIR" "Spain" "healthtech"
site:linkedin.com/in "MCP server" "Spain"
```

### GitHub / MCP

```text
site:github.com "mcp-server" "Spain"
site:github.com "Model Context Protocol" "Madrid"
site:github.com "mcp-server" "observability"
site:github.com "mcp-server" "security"
```

### Empresas y asociaciones

```text
site:asociacionfintech.es fintech insurtech asociado "IA"
site:ismsforum.es "Inteligencia Artificial" ciberseguridad
site:ismsforum.es ENS IA seguridad
site:ametic.es salud digital inteligencia artificial
```

## Bloque de trabajo recomendado

1. Abrir 8 pestanas, una por perfil objetivo.
2. Sacar 5 candidatos por perfil, sin escribir mensajes aun.
3. Reducir de 40 a 30 aplicando la regla 2/3.
4. Para cada uno, escribir una frase de personalizacion concreta en el tracker.
5. Solo despues, usar `02-mensajes-personalizables.md`.

## Criterio de calidad del hueco personalizable

Bueno:

> "Vi tu charla sobre gobierno de IA en banca y el punto sobre trazabilidad de decisiones LLM..."

Malo:

> "Vi tu perfil y me parecio interesante..."

Bueno:

> "Vi que vuestro producto acaba de incorporar automatizacion de workflows para equipos compliance..."

Malo:

> "Vi que trabajais con tecnologia..."

