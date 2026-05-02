# OWASP MCP Top 10 — Borrador 0.1

> Spec abierto, no normativo, comunitario. Es la semilla de la opción E (toolkit OSS) y el activo de marca para C (consultoría) y A (libro).
>
> Publicar como repo separado en GitHub bajo CC-BY-4.0. Aceptar PRs desde día 1.

---

# OWASP MCP Top 10 — v0.1 (DRAFT, mayo 2026)

> **Estado:** borrador para discusión pública. **No** es un proyecto oficial OWASP todavía. La intención es proponerlo como tal una vez la comunidad valide v1.0.
>
> **Idioma de referencia:** inglés. Traducción oficial al español mantenida en paralelo.
>
> **Cómo contribuir:** abrir issue / PR. Ver `CONTRIBUTING.md`.

## Por qué

Los servidores MCP están en producción en miles de organizaciones a mediados de 2026. La superficie de ataque difiere lo suficiente de una API REST tradicional como para que las taxonomías existentes (OWASP API Top 10, OWASP LLM Top 10) cubran el tema sólo parcialmente.

Esta spec compila los 10 antipatrones de seguridad más frecuentes y de mayor impacto observados en auditorías reales de servidores MCP entre noviembre 2024 y abril 2026.

## Alcance

- Aplicable a servidores MCP (cualquier transporte: stdio, SSE, HTTP).
- No cubre seguridad del cliente LLM ni del modelo subyacente.
- No cubre seguridad de infraestructura (red, IAM cloud) salvo donde interactúa específicamente con MCP.

## Resumen de la lista

| ID | Nombre | Severidad típica |
|---|---|---|
| **M01** | Tool Over-Privilege | Crítica |
| **M02** | Resource Disclosure Without Authorization | Crítica |
| **M03** | Prompt Injection via Resources or Tool Outputs | Alta |
| **M04** | Missing or Forgeable Authentication | Crítica |
| **M05** | Insufficient Audit Logging | Alta |
| **M06** | Sensitive Data in Logs and Traces | Alta |
| **M07** | Unbounded Tool Operations (DoS) | Media |
| **M08** | Tenant Isolation Failure | Crítica |
| **M09** | Insecure Defaults and Configuration Drift | Media |
| **M10** | Vulnerable or Outdated MCP SDK / Dependencies | Media |

---

## M01 — Tool Over-Privilege

**Descripción**

Un tool expone más capacidad o más datos de los necesarios para su función declarada, otorgando al LLM (y por tanto a cualquier entidad capaz de inyectar prompts) más poder del que debe tener.

**Cómo se manifiesta**

- Tools que aceptan SQL/queries arbitrarias en lugar de operaciones específicas.
- Tools de escritura sin confirmación cuando uno de lectura serviría.
- Un único mega-tool con un parámetro `action` en lugar de N tools acotados.
- Scopes OAuth solicitados con `*` o equivalentes.

**Impacto típico**

Cualquier prompt injection convierte una capacidad legítima en arbitraria. Datos de otros usuarios, escrituras destructivas, ejecución de código.

**Cómo detectarlo**

- Revisión: ¿la descripción del tool y su firma coinciden con su capacidad real?
- Automatizado: tools que aceptan parámetros de tipo `string` libre sin enum/regex; tools cuyo nombre contiene `query`, `execute`, `run`, `eval`.

**Cómo mitigarlo**

- Un tool por operación de negocio.
- Inputs validados con schema (enums, regex, rangos).
- Si un tool necesita operar sobre múltiples entidades, exigir lista explícita en input, nunca query libre.
- Principio de menor privilegio aplicado por defecto.

**Referencias**

- {Sección del libro: cap. 3.}
- {OWASP API: API1:2023 BOLA — vector relacionado.}

---

## M02 — Resource Disclosure Without Authorization

**Descripción**

Resources MCP devuelven datos sin verificar que el contexto de llamada (usuario, sesión, scope) está autorizado a leerlos.

**Cómo se manifiesta**

- Resources con URIs predecibles (`patient://{id}`) sin chequeo de pertenencia.
- Filtros aplicados en el system prompt en lugar de en el código del resource.
- Caché compartida entre tenants sin segmentación por clave.

**Impacto típico**

IDOR clásica adaptada a MCP. Un usuario puede pedir resources de otro vía prompt.

**Mitigación**

- Autorización en el código del resource, no en el prompt.
- Row-level security a nivel de base de datos cuando aplica.
- Caché segmentada por tenant + usuario.

---

## M03 — Prompt Injection via Resources or Tool Outputs

**Descripción**

Contenido controlado parcial o totalmente por terceros (documentos, emails, comentarios, registros de log) llega al LLM a través de resources o respuestas de tools, alterando su comportamiento.

**Cómo se manifiesta**

- Resources que devuelven contenido user-generated sin marcado.
- Tools que leen contenido externo (web, email, tickets) y lo retornan crudo.
- Salidas de tools que mezclan datos y metadatos sin separación.

**Impacto típico**

Exfiltración de datos a través de tools subsecuentes. Manipulación de respuestas. Bypass de guardrails.

**Mitigación**

- Marcado explícito de contenido no confiable (ej. tags `<untrusted>...</untrusted>`).
- Política documentada para el cliente LLM sobre cómo tratar contenido marcado.
- Reducción de superficie: no exponer contenido user-generated salvo necesidad.
- Detección heurística de patrones de inyección antes de devolver.

---

## M04 — Missing or Forgeable Authentication

**Descripción**

El servidor MCP confía en el cliente sin verificar identidad criptográficamente, o usa esquemas de auth débiles.

**Manifestaciones**

- API keys compartidas entre todos los usuarios.
- Tokens en headers sin verificar firma.
- OAuth implícito en flujos donde aplica `auth code + PKCE`.
- Ausencia total de auth en MCPs "internos" expuestos a la red corporativa.

**Mitigación**

- OAuth 2.1 con PKCE para flujos interactivos.
- mTLS para flujos servidor-a-servidor.
- Tokens cortos + refresh.
- Identidad propagada hasta backends, no sustituida por una identidad de servicio.

---

## M05 — Insufficient Audit Logging

**Descripción**

No hay registro suficiente para reconstruir qué prompt → qué tool call → qué query → qué dato salió.

**Manifestaciones**

- Logs solo de errores.
- Logs sin correlación entre capas (LLM, MCP, backend).
- Logs mutables / sin firma.

**Mitigación**

- Audit log inmutable con append-only storage.
- Correlation ID propagado en toda la cadena.
- Retención según marco regulatorio aplicable.
- Esquema documentado y testeado.

---

## M06 — Sensitive Data in Logs and Traces

**Descripción**

PHI/PII/secretos aparecen en logs, traces, métricas o mensajes de error.

**Manifestaciones**

- `print(user)` o `logger.info(input)` sin filtro.
- Trazas distribuidas con tags conteniendo emails/IDs sensibles.
- Excepciones que incluyen el SQL que falló (con datos reales).

**Mitigación**

- Librería de redacción aplicada en el sink de logs.
- Tests automatizados que verifican que campos marcados como sensibles no aparecen en stdout.
- Política de retención agresiva.
- Acceso a logs auditado.

---

## M07 — Unbounded Tool Operations (DoS)

**Descripción**

Tools que pueden consumir recursos arbitrarios cuando se invocan con parámetros no acotados.

**Manifestaciones**

- Tools que devuelven "todos los registros" sin paginación.
- Tools que ejecutan queries sin timeout.
- Tools que generan tokens LLM downstream sin límite.

**Mitigación**

- Paginación obligatoria.
- Timeouts y límites de tamaño en cada tool.
- Rate limiting por tenant y por tool.
- Cuotas de coste por sesión.

---

## M08 — Tenant Isolation Failure

**Descripción**

En servidores MCP multi-tenant, datos o capacidades de un tenant son accesibles desde otro.

**Manifestaciones**

- Conexión única al backend con identidad de servicio compartida.
- Caché global sin clave por tenant.
- Configuración compartida modificable por tenant.

**Mitigación**

- Aislamiento a nivel de pool de conexiones, caché, almacenamiento y logs.
- Tests automatizados de aislamiento (tenant A intenta acceder a recursos de B).
- Auditoría periódica.

---

## M09 — Insecure Defaults and Configuration Drift

**Descripción**

El servidor se despliega con defaults inseguros, o la configuración deriva entre entornos sin control.

**Manifestaciones**

- Modo debug activo en producción.
- CORS abierto.
- TLS opcional.
- Diferencias no documentadas entre staging y prod.

**Mitigación**

- Configuración como código, versionada.
- Validación de configuración al arranque (fail-fast en defaults inseguros).
- Comparación automática de config entre entornos.

---

## M10 — Vulnerable or Outdated MCP SDK / Dependencies

**Descripción**

Versiones del SDK MCP o dependencias con CVEs conocidos.

**Manifestaciones**

- SDK MCP > 6 meses sin actualizar.
- Dependencias del transport layer desactualizadas.
- Sin SBOM ni proceso de monitorización de vulnerabilidades.

**Mitigación**

- SBOM generado en cada build.
- Dependabot / Renovate activos.
- Política de SLA para parchear CVEs (críticas <72h).

---

## Roadmap del spec

- **v0.1 (mayo 2026):** este borrador. Abrir feedback público.
- **v0.2 (julio 2026):** revisión tras 2 meses de comentarios. Sumar 5-10 contribuidores externos.
- **v1.0 (octubre 2026):** publicación estable + traducción ES + correspondencia con MITRE ATT&CK donde aplique.
- **v1.1+ (continuo):** revisiones trimestrales.

## Cómo se relaciona con otros estándares

| Estándar | Solapamiento | Diferencia |
|---|---|---|
| OWASP API Top 10 | M01, M02, M07, M09 | API generalista, no contempla LLM en el lazo |
| OWASP LLM Top 10 | M03, M06 | Foco en el modelo, no en el servidor de tools |
| MITRE ATLAS | M03 | Más amplio (ML lifecycle), menos prescriptivo |
| NIST AI RMF | Marco de gobernanza | No prescribe controles técnicos |

## Licencia

CC-BY-4.0. Atribución requerida. Uso comercial permitido.

## Contribuidores

{Tu nombre} (mantenedor inicial). Lista abierta.
