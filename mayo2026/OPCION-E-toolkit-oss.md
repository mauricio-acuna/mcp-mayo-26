# Opción E — Toolkit open source + tier enterprise

> Convertir el conocimiento en software libre, capturar valor con servicios premium.

## Tesis

El mercado MCP necesita una herramienta de **auditoría de seguridad para servidores MCP** que hoy no existe (equivalente a `bandit` o `semgrep` para MCP). Open-sourcearla genera adopción rápida y posiciona al autor como referente. La monetización viene del tier hosted/enterprise.

## Producto

### Capa OSS (gratis, MIT)

**`mcp-audit`** — CLI + librería Python que:

- Escanea un servidor MCP (definición de tools/resources, código fuente).
- Detecta antipatrones de seguridad: tools sobre-permisivos, resources que filtran PHI, prompts con inyección, ausencia de auth, logs con datos sensibles.
- Genera informe HTML + SARIF (para integrar en CI/CD).
- 50-80 reglas iniciales cubriendo OWASP MCP top-10 (que el autor publica como spec del proyecto).

```bash
pip install mcp-audit
mcp-audit scan ./my-mcp-server --output report.html
```

### Capa Cloud (€)

- **mcp-audit Cloud** — versión SaaS con dashboard, histórico, integración GitHub/GitLab, alertas.
- Pricing: free hasta 1 repo, **€49/mes** team, **€399/mes** enterprise (SSO, on-prem, soporte).

### Capa Enterprise (€€€)

- Auditoría manual + consultoría sobre hallazgos (Opción C empaquetada).
- Reglas custom para compliance específico (HIPAA, GDPR, SOC 2).
- Soporte 24/7.

## Por qué este nicho

- No hay competencia directa a abril 2026.
- Las empresas grandes ya despliegan MCP y necesitarán pasar auditorías.
- OSS resuelve el problema de distribución (GitHub stars + Hacker News + comunidad MCP oficial).
- El catálogo de reglas **es el activo defendible**: cuanto más se mantiene, más valioso.

## Reutilización del repo actual

- El conocimiento del libro/MediMind se convierte directamente en **reglas del scanner**.
- MediMind sirve como **suite de tests** (servidor real con vulns y fixes documentados).
- El libro pasa a ser *"the official mcp-audit handbook"* — gratuito, marketing del proyecto.

## Plan ejecutable (9 meses)

| Mes | Hito |
|---|---|
| 1 | Spec pública "OWASP MCP Top 10" como repo separado, pedir contribuciones |
| 2-3 | MVP `mcp-audit` con 20 reglas, lanzamiento en Show HN + r/LocalLLaMA + comunidad MCP |
| 4 | 500 stars, primeras integraciones de usuarios |
| 5-6 | Llegar a 50 reglas, publicar comparativas con MCP servers públicos famosos |
| 7 | Lanzar Cloud (free + team) |
| 8-9 | Cerrar 2-3 enterprise (€10-30k/año cada uno) |

## Economía objetivo año 1-2

- 200 cuentas Team × €49/mes = €117k ARR
- 5 cuentas Enterprise × €5k/año = €25k ARR
- Servicios premium = €60k/año
- **Total año 2:** €200k+ ARR realista, con techo €500k+ si crece la comunidad.

## Pros

- Distribución resuelta vía OSS.
- Defensibilidad por catálogo de reglas + comunidad.
- Multiplica la utilidad del trabajo ya hecho.
- Posiciona al autor en la cumbre del nicho (autor del estándar de facto).

## Contras

- Mantenimiento de OSS es trabajo a perpetuidad.
- Requiere skills de devrel/comunidad además de técnicas.
- Conversión OSS → pago suele ser <1%; necesita volumen para que el SaaS funcione.
- 6-9 meses sin ingresos serios.

## Cuándo elegir esta opción

- El autor disfruta hacer OSS y construir comunidad técnica.
- Tiene runway de 9-12 meses.
- Quiere construir un activo a 5-10 años, no ingresos rápidos.
- Acepta que el libro y MediMind son herramientas, no productos finales.
