# Esqueleto del libro lean (recortado)

> Versión escribible del TOC actual. Cada capítulo con brief de 1 página y referencia al material reutilizable del repo.
>
> **Extensión total objetivo:** 90-110 págs (~28-35k palabras).
> **Cadencia:** 1 capítulo cada 2 semanas durante 12 semanas.

## TOC final

```
Front matter (4 págs)
├── Portada + créditos
├── Prefacio (2 págs)
└── Cómo leer este libro (1 pág)

Parte I — Por qué (15 págs)
├── Cap. 1 · MCP ya es commodity (8 págs) ✅ existe
└── Cap. 2 · Modelo de amenazas de un MCP server (12 págs)

Parte II — Diseño seguro (30 págs)
├── Cap. 3 · Diseño de superficie: tools, resources, prompts (12 págs)
└── Cap. 4 · Cifrado, redacción de PHI/PII y claves (15 págs)

Parte III — Compliance accionable (20 págs)
└── Cap. 5 · HIPAA / RGPD traducidos a controles técnicos (18 págs)

Apéndices (15 págs)
├── Ap. E · Checklist de seguridad MCP (8 págs) ✅ existe
└── Ap. F · Glosario (4 págs) ✅ existe

Total: ~95 págs
```

**Recortado del TOC original (post-pivote):** capítulos 5 (OAuth detallado), 8 (auditoría), 9 (GDPR/SOC 2), 10 (observabilidad), 11 (multi-tenant) y 12 (incidentes). Pasan a artículos en el blog/lista, alimentando el funnel sin bloquear el lanzamiento.

---

## Briefs por capítulo

### Cap. 1 · MCP ya es commodity

Estado: borrador existente reutilizable de [PIVOTE_2026.md](../../../PIVOTE_2026.md) §1-§3 + sección "Por qué este libro" del nuevo prefacio.

Trabajo pendiente: maquetar como capítulo independiente del libro y como lead magnet.

---

### Cap. 2 · Modelo de amenazas de un MCP server

**Tesis del capítulo:** un MCP server tiene una superficie de ataque distinta a una API REST. Si lo modelas con los mismos hábitos vas a fallar.

**Outline:**

1. Qué es STRIDE y por qué adaptarlo.
2. Diagrama de actores: cliente LLM (¿confiable?), usuario final (no), backends.
3. STRIDE-MCP punto por punto:
   - Spoofing: cliente MCP suplantado, prompts del sistema falsificados.
   - Tampering: tool input no validado, resources mutables.
   - Repudiation: ausencia de audit log inmutable.
   - Information disclosure: el caso central, con 3 sub-vectores.
   - DoS: tools costosos sin rate limit, resources que devuelven millones de filas.
   - Elevation: tools que aceptan argumentos de scope.
4. Tabla de amenazas → controles → capítulo del libro donde se implementa.
5. Ejercicio: modelar un MCP propio en 30 minutos con plantilla incluida.

**Material reutilizable:** ninguno todavía. Capítulo nuevo.

**Asset adicional:** plantilla `threat-model-mcp.md` en el repo de acompañamiento.

---

### Cap. 3 · Diseño de superficie segura

**Tesis:** la mayor parte de los hallazgos de seguridad MCP no son bugs, son decisiones de diseño tomadas sin pensar en el atacante.

**Outline:**

1. Principio de menor privilegio aplicado a tools (con anti-ejemplo `query_database(sql)`).
2. Granularidad de tools: ¿uno por acción o uno mega-tool? Trade-offs.
3. Resources con datos sensibles: cuándo exponer, cuándo proxy-ear.
4. Prompts del servidor: cuándo SÍ y cuándo NO. Inyectabilidad desde resources.
5. Validación de inputs: schemas, enums, límites. Por qué `string` libre es casi siempre un error.
6. Versionado y deprecación segura.
7. Mini-caso: refactorizar un tool inseguro real.

**Material reutilizable:** parte de [book-manuscript/10-chapter-security-authentication.md](../../../book-manuscript/10-chapter-security-authentication.md), secciones de tools.

---

### Cap. 4 · Cifrado, redacción de PHI/PII y manejo de claves

**Tesis:** cifrar es lo fácil. Redactar bien y rotar claves es lo que la mayoría suspende.

**Outline:**

1. Cifrado en tránsito: mTLS entre cliente MCP y servidor, no solo TLS.
2. Cifrado en reposo: envelope encryption, KMS/HSM, qué evitar.
3. Tokenización vs cifrado: cuándo cada uno.
4. Redacción de PHI/PII en logs: librería + tests automatizados.
5. Redacción en respuestas de tools: el caso "el LLM verá esto".
6. Manejo de secretos: nunca en env vars en producción multi-tenant.
7. Rotación de claves: la operación que nadie hace bien.

**Material reutilizable:** mucho de `medimind-mcp/mcp-server/src/security/encryption.py` y módulos relacionados. El capítulo puede usar el código real como base.

---

### Cap. 5 · HIPAA / RGPD traducidos a controles técnicos

**Tesis:** los textos legales son inútiles para un ingeniero. Este capítulo los traduce a tickets de Jira.

**Outline:**

1. HIPAA Security Rule: salvaguardas técnicas → controles MCP. Tabla 1-a-1.
2. HIPAA Privacy Rule: minimum necessary y MCP tools.
3. RGPD: bases de licitud cuando un LLM procesa datos personales.
4. RGPD: derecho al olvido en sistemas con LLM y caché.
5. ENS (España, sector público) y DORA (financiero EU): lo mínimo a saber.
6. BAAs y DPAs con proveedores LLM: qué exigir.
7. Plantilla de matriz de cumplimiento (descargable).

**Material reutilizable:** [medimind-mcp/compliance/HIPAA_CHECKLIST.md](../../../medimind-mcp/compliance/HIPAA_CHECKLIST.md) y plantilla BAA.

---

### Apéndice E · Checklist de seguridad MCP

Ya existe en [book-manuscript/appendix-e-security-checklist.md](../../../book-manuscript/appendix-e-security-checklist.md). Necesita:

- Reorganización por fase del SDLC (diseño / build / deploy / operate).
- Versión condensada (1 pág por área) para el lead magnet.
- Marcar qué ítems están cubiertos por reglas automatizadas en `mcp-audit` (cuando exista).

### Apéndice F · Glosario

Ya existe. Revisar y añadir 10-15 términos nuevos (STRIDE-MCP, SARIF, BAA, DPA, etc.).

---

## Calendario de redacción (12 semanas)

| Semana | Trabajo |
|---|---|
| 1 | Cap. 1 maquetado como lead magnet |
| 2 | Brief detallado + outline final cap. 2 |
| 3-4 | Redacción cap. 2 (publicar borrador a la lista) |
| 5-6 | Redacción cap. 3 |
| 7-8 | Redacción cap. 4 |
| 9-10 | Redacción cap. 5 |
| 11 | Apéndices E y F revisados + maquetación |
| 12 | Revisión técnica externa + lanzamiento pre-venta |

## Reglas de proceso

1. **Borrador publicable, no obra maestra.** Cada capítulo se publica a la lista en cuanto pasa una revisión propia. Erratas se corrigen en versionado.
2. **Una sesión de escritura = mínimo 90 min.** Por debajo no compensa el coste de cambio de contexto.
3. **Si un capítulo se atasca >2 semanas, recortarlo.** No bloquear el conjunto.
4. **Revisión técnica externa pagada.** Buscar un revisor con experiencia real en MCP-security (no familiar). Presupuesto: €600-1.000.
5. **Prohibido añadir capítulos.** Cualquier idea nueva va al blog, no al libro.
