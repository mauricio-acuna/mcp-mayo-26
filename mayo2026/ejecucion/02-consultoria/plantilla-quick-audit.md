# Plantilla — Informe MCP Quick-Audit

> Entregable estándar del paquete €4.500. Reutilizable engagement tras engagement. Markdown que luego se exporta a PDF maquetado.

---

# MCP Quick-Audit — {Cliente}

**Servidor auditado:** {nombre / repo}
**Fecha:** {YYYY-MM-DD}
**Auditor:** {nombre}
**Versión del informe:** 1.0
**Confidencialidad:** Restringido — uso interno {Cliente}

---

## 1. Resumen ejecutivo

### Veredicto

> Una frase. Ej.: *"El servidor presenta 3 hallazgos críticos que impiden recomendar su exposición a usuarios externos hasta su mitigación."*

### Métricas clave

| | Conteo |
|---|---|
| Hallazgos críticos | {n} |
| Hallazgos altos | {n} |
| Hallazgos medios | {n} |
| Hallazgos bajos / informativos | {n} |
| **Total** | **{n}** |

### Top 3 hallazgos críticos

1. **{Título}** — {1 línea de impacto}.
2. **{Título}** — {1 línea de impacto}.
3. **{Título}** — {1 línea de impacto}.

### Recomendación general

{2-3 párrafos. Sin tecnicismos. Lo que un CTO necesita saber para decidir.}

---

## 2. Alcance

### Qué se auditó

- Repositorio(s): {lista con commit SHA}.
- Componentes: tools, resources, prompts, capa de transporte, capa de auth.
- Entornos: {dev / staging / prod observado vía X}.
- Periodo de revisión: {fechas}.

### Qué NO se auditó

- Infraestructura subyacente (red, IAM cloud, etc.) — fuera del paquete Quick-Audit.
- Código del cliente LLM consumidor.
- Dependencias de terceros (limitado a CVEs conocidos).
- Pentest activo (no se ejecutaron exploits en vivo).

### Metodología

- Lectura estática de código.
- Modelo de amenazas STRIDE-MCP (ver Anexo A).
- Comprobación contra **OWASP MCP Top 10 v{x.y}**.
- Revisión de configuración de despliegue (Dockerfile, manifests, env vars).
- 1 entrevista de 60 min con el equipo técnico.

---

## 3. Modelo de amenazas

### Diagrama de superficie

```
{Diagrama ASCII o referencia a draw.io adjunto}
   Cliente LLM ──► MCP server ──► {backends del cliente}
```

### Activos protegidos

| Activo | Sensibilidad | Por qué importa |
|---|---|---|
| {p.ej. PII de clientes} | Alta | RGPD, reputación |
| {p.ej. Tokens OAuth de terceros} | Alta | Pivot a otros sistemas |
| {p.ej. Prompts internos del sistema} | Media | Disclosure ≠ brecha pero da ventaja al atacante |

### Actores

| Actor | Capacidad | Motivación |
|---|---|---|
| Usuario final del LLM (legítimo pero curioso) | Inyectar prompts | Acceder a datos de otros usuarios |
| Usuario final malicioso | Prompt injection avanzada | Exfiltración / RCE |
| Desarrollador con acceso al repo | Cambios de código | Backdoor |
| SRE con acceso a logs | Lectura | PHI/PII en logs |

### Matriz STRIDE-MCP resumida

| Amenaza | Vector MCP típico | Presente en este servidor |
|---|---|---|
| Spoofing | Cliente MCP suplantado | {sí/no/parcial} |
| Tampering | Tool input no validado | {sí/no/parcial} |
| Repudiation | Sin audit log | {sí/no/parcial} |
| Information disclosure | Resource sin auth | {sí/no/parcial} |
| DoS | Tool sin rate limit | {sí/no/parcial} |
| Elevation of privilege | Scopes OAuth amplios | {sí/no/parcial} |

---

## 4. Hallazgos detallados

> Numerados QA-001, QA-002, … Por severidad descendente.

### QA-001 · {Título corto del hallazgo}

| | |
|---|---|
| Severidad | 🔴 Crítica / 🟠 Alta / 🟡 Media / 🔵 Baja / ⚪ Info |
| Categoría | {OWASP-MCP-Top-10 ID, p.ej. M01: Tool Over-Privilege} |
| Componente | {archivo:línea o `tool:nombre`} |
| Esfuerzo de fix | {S / M / L} |

**Descripción**

{Qué se encontró. Concreto, sin moralina.}

**Evidencia**

```python
# extracto de {archivo}:{línea}
{código real anonimizado}
```

**Impacto**

{Qué puede pasar en el peor caso realista. Sin inflar.}

**Cómo reproducirlo**

1. {Pasos numerados, reproducibles por el equipo del cliente.}
2. ...

**Recomendación**

{Fix concreto. Si es de código, mostrar el código corregido.}

```python
# fix sugerido
{código}
```

**Referencias**

- {Link a sección del libro, OWASP MCP Top 10, RFC, etc.}

---

### QA-002 · {…}

{Repetir formato.}

---

## 5. Hallazgos no priorizados

Lista de antipatrones menores no incluidos en el detalle por bajo impacto pero recomendable atender en próximo refactor.

| ID | Hallazgo | Severidad | Componente |
|---|---|---|---|
| QA-N01 | … | Info | … |

---

## 6. Plan de remediación sugerido

### Sprint 1 (semana 1-2) — Críticos

- [ ] QA-001
- [ ] QA-002
- [ ] QA-003

### Sprint 2 (semana 3-4) — Altos

- [ ] QA-004
- [ ] QA-005

### Backlog (próximo trimestre) — Medios e inferiores

- [ ] QA-006…

### Estimación de esfuerzo total

{X días-persona aproximados. Distinguir entre código, infraestructura y documentación.}

### Opcional — Hardening Sprint

Si {Cliente} no tiene capacidad interna para ejecutar Sprints 1-2, puede contratarse el paquete *MCP Hardening Sprint* (€25.000, 4 semanas) que entrega los fixes como PRs mergeables. **Sin obligación.**

---

## 7. Próximos pasos sugeridos para {Cliente}

1. Revisión interna del informe (1 semana).
2. Sesión de 90 min con el auditor para Q&A — incluida en el paquete.
3. Decisión go/no-go sobre exposición a producción / ampliación de scope.
4. Re-audit en 6 meses para verificar remediación (paquete reducido €2.500).

---

## Anexos

### Anexo A · STRIDE-MCP completo

{Tabla extensa para los puristas.}

### Anexo B · Checklist OWASP MCP Top 10 punto por punto

{Tabla con cada control + cumple/no cumple/no aplica.}

### Anexo C · Evidencias adicionales

{Capturas, logs, configs relevantes.}

### Anexo D · Glosario

{PHI, MCP, STRIDE, SARIF, etc.}

---

**Limitaciones del informe**

Este Quick-Audit es una revisión estática y de configuración limitada a 5 días. No sustituye a un pentest, a una revisión de arquitectura cloud, ni a una auditoría regulatoria formal. Los hallazgos reflejan el estado del servidor en la fecha indicada; cambios posteriores no están cubiertos.

**Confidencialidad**

Documento sujeto al NDA firmado el {fecha}. No reproducir ni distribuir sin consentimiento escrito de {Cliente} y {Auditor}.
