# HANDOFF — Continuación del proyecto

> Documento de traspaso. Lectura obligatoria para cualquier persona o asistente IA (Codex, Claude, Cursor, otros) que retome el trabajo después del 30 de abril de 2026.
>
> **Última actualización:** 30 abril 2026.
> **Autor del traspaso:** GitHub Copilot (Claude) en sesión preparatoria.

---

## 0. Cómo usar este documento

1. Lee primero [README.md](README.md), luego [PIVOTE_2026.md](PIVOTE_2026.md), luego [mayo2026/RECOMENDACION.md](mayo2026/RECOMENDACION.md).
2. Vuelve aquí.
3. Confirma con el humano responsable las decisiones pendientes en §1.
4. Ejecuta la fase que corresponda según §2.

**Nada de lo que sigue se ejecuta sin haber completado la Etapa 1 (validación) descrita en [mayo2026/ejecucion/semana-1/](mayo2026/ejecucion/semana-1/).** Si llegas a este repo y no hay archivos rellenos en `semana-1/01-tracker-contactos.md` ni decisión escrita en `semana-1/04-sintesis-dia-7.md`: la Etapa 1 sigue pendiente y todo lo demás está bloqueado.

---

## 1. Decisiones pendientes que el humano debe confirmar

Sin estas, no hay ejecución correcta posible. Pregunta antes de actuar.

| # | Decisión | Por qué bloquea | Default sugerido si no responde |
|---|---|---|---|
| 1 | **Runway disponible** (€ y meses sin ingresos) | Determina si se prioriza C (cash flow rápido) o E (apuesta a 18 m) | <3 meses → solo C |
| 2 | **Visibilidad del repo** | `mayo2026/` contiene estrategia comercial sensible | Privado por defecto, splits a públicos según §4 |
| 3 | **Licencia(s) finales** | Necesario antes de publicar nada | Ver §5 |
| 4 | **Datos LSSI-CE** (nombre, NIF/CIF, email, dirección postal) | Obligatorios en landing y sales page | Pedir al humano, no inventar |
| 5 | **Marca personal vs sub-marca** | Afecta dominio, copy, identidad de `mcp-audit` | Marca personal del autor + sub-marca `mcp-audit` |
| 6 | **Resultado de las 5-7 entrevistas (verde/ámbar/rojo)** | Determina la rama del roadmap | No proceder hasta tenerlo escrito |

---

## 2. Mapa de etapas y qué hacer en cada una

```
ETAPA 1 — Validación  ←  ESTÁS AQUÍ HASTA QUE SE COMPLETE
    │
    ├── VERDE  →  ETAPA 2A (continuar combo C+A→E)
    ├── ÁMBAR  →  ETAPA 2B (ajustar oferta y re-validar)
    └── ROJO   →  ETAPA 2C (replantear opciones B/D/esperar)

ETAPA 2A → ETAPA 3 (escalado mes 6+) → ETAPA 4 (toolkit OSS mes 9+)
```

### ETAPA 1 — Validación (semana actual)

**Estado esperado:** archivos en [mayo2026/ejecucion/semana-1/](mayo2026/ejecucion/semana-1/) rellenos, decisión escrita en `04-sintesis-dia-7.md`.

**Tu rol como asistente IA:**

- ❌ NO ejecutas las llamadas (las hace el humano).
- ❌ NO escribes capítulos del libro todavía.
- ❌ NO publicas nada externamente.
- ✅ SÍ ayudas a personalizar mensajes según contactos concretos cuando el humano te los pase.
- ✅ SÍ ayudas a sintetizar notas de entrevista cuando el humano te las comparta.
- ✅ SÍ ayudas a redactar el post LinkedIn de cierre de la semana.

### ETAPA 2A — Verde: continuar combo C+A→E

**Activación:** la decisión escrita en `semana-1/04-sintesis-dia-7.md` marca casilla VERDE.

**Acciones a ejecutar (en este orden):**

1. **Web mínima publicada** (Astro estático en Cloudflare Pages o GitHub Pages):
   - Sales page de consultoría → contenido de [mayo2026/ejecucion/02-consultoria/sales-page.md](mayo2026/ejecucion/02-consultoria/sales-page.md).
   - Landing del libro → contenido de [mayo2026/ejecucion/03-libro/landing-page.md](mayo2026/ejecucion/03-libro/landing-page.md).
   - Aviso legal LSSI-CE con datos del humano (decisión #4).
   - Crear repo separado público `web-mcp-produccion` (no mezclar con este repo privado).

2. **Capítulo 1 redactado completo** (lead magnet real, ~12-18 págs):
   - Brief en [mayo2026/ejecucion/03-libro/esqueleto-libro-lean.md](mayo2026/ejecucion/03-libro/esqueleto-libro-lean.md) §"Cap. 1".
   - Reutilizar [PIVOTE_2026.md](PIVOTE_2026.md) §1-§3 + secciones del prefacio actual.
   - Salida: `book-manuscript/01-mcp-ya-es-commodity.md` (markdown maquetable).

3. **Spec OWASP MCP Top 10 publicado**:
   - Crear repo separado público `owasp-mcp-top-10` (no en este repo).
   - Mover el contenido de [mayo2026/ejecucion/04-toolkit-oss/owasp-mcp-top-10.md](mayo2026/ejecucion/04-toolkit-oss/owasp-mcp-top-10.md) como `README.md` de ese repo.
   - Añadir `CONTRIBUTING.md`, `LICENSE` (CC-BY-4.0), `CODE_OF_CONDUCT.md`.
   - Anuncio: post LinkedIn + Show HN + comunidad MCP oficial (Discord).

4. **Email kit**:
   - Conectar ConvertKit / MailerLite (decisión del humano).
   - Configurar doble opt-in y secuencia de bienvenida según [mayo2026/ejecucion/03-libro/lead-magnet.md](mayo2026/ejecucion/03-libro/lead-magnet.md).

5. **Outbound continuado**:
   - 50 contactos / semana usando plantillas de [mayo2026/ejecucion/02-consultoria/outbound-secuencia.md](mayo2026/ejecucion/02-consultoria/outbound-secuencia.md).
   - Tracker semanal según [mayo2026/ejecucion/05-roadmap-y-metricas.md](mayo2026/ejecucion/05-roadmap-y-metricas.md) §dashboard.

6. **Capítulos 2-5 cada 2 semanas** según [esqueleto-libro-lean.md](mayo2026/ejecucion/03-libro/esqueleto-libro-lean.md).

7. **Apéndice E reescrito en formato condensado** (1 pág por área del SDLC) para versión printable del lead magnet.

8. **Apéndice F (glosario) actualizado** con: STRIDE-MCP, SARIF, BAA, DPA, M01-M10, mTLS, envelope encryption, FHIR R4, SMART on FHIR, OAuth 2.1, PKCE.

9. **Plantillas legales** (sólo cuando haya primer cliente real):
   - NDA mutuo (ES).
   - Contratos: Quick-Audit / Hardening / Compliance.
   - Pedirlas a abogado real, no generar tú. Usar plantillas de Notion/Lawpath/Stelar como punto de partida.

### ETAPA 2B — Ámbar: ajustar oferta y re-validar

**Activación:** decisión marca ÁMBAR en `semana-1/04-sintesis-dia-7.md`.

**Acciones:**

1. Lee el bloque ÁMBAR de la síntesis para extraer el ajuste necesario (vocabulario, comprador, sector).
2. Reescribe **únicamente** estos archivos antes de seguir:
   - [mayo2026/ejecucion/02-consultoria/sales-page.md](mayo2026/ejecucion/02-consultoria/sales-page.md)
   - [mayo2026/ejecucion/03-libro/landing-page.md](mayo2026/ejecucion/03-libro/landing-page.md)
   - [mayo2026/ejecucion/02-consultoria/outbound-secuencia.md](mayo2026/ejecucion/02-consultoria/outbound-secuencia.md) (mensajes)
3. Repite Etapa 1 con 5 nuevas entrevistas usando la oferta ajustada.
4. Si el segundo verde no llega: tratar como ROJO.

### ETAPA 2C — Rojo: replantear

**Activación:** decisión marca ROJO en `semana-1/04-sintesis-dia-7.md`.

**Acciones:**

1. NO continuar con C+A→E.
2. Revisar [mayo2026/00-REVISION.md](mayo2026/00-REVISION.md) §4 (preguntas abiertas) y [mayo2026/RECOMENDACION.md](mayo2026/RECOMENDACION.md) con la nueva información.
3. Reabrir las opciones marcadas en el bloque ROJO de la síntesis (B, D, esperar, libro EN, pivot).
4. Generar un nuevo documento `mayo2026/REPLANTEO-{YYYYMM}.md` con el nuevo plan, **sin sobrescribir** los archivos existentes.

### ETAPA 3 — Escalado (mes 6+)

Solo entrar tras checkpoint mes 6 según [mayo2026/ejecucion/05-roadmap-y-metricas.md](mayo2026/ejecucion/05-roadmap-y-metricas.md).

Decisión a tomar con el humano: ramificación (escalar C / lanzar D / retomar B).

### ETAPA 4 — Toolkit OSS (mes 9+)

Construir el scanner real `mcp-audit`. Stack sugerido: Python + Tree-sitter para análisis estático + ruff/semgrep como referencia de arquitectura. Repo separado público.

---

## 3. Arquitectura actual
- **Módulos**:
  - Descripción de los módulos principales.
- **Pipeline**:
  - Flujo de datos y componentes clave.

## 4. Configuración
- **Propiedades clave**:
  - Tabla con propiedades y valores por defecto.

## 5. Cosas que NO funcionan en este equipo
- **Limitaciones actuales**:
  - Docker no configurado completamente.
  - Falta de documentación en ciertas áreas.

## 6. Decisiones que NO se revierten sin discutir
- **Reglas inviolables**:
  - Lista de decisiones clave.

## 7. Pendientes priorizados
- **Tareas clave**:
  - Contexto, pasos sugeridos y criterios de aceptación.

## 8. Convenciones inviolables
- **Reglas operativas**:
  - Lista de convenciones.

## 9. Cómo retomar con Codex paso a paso
- **Prompt sugerido**:
  ```
  Lee los archivos HANDOFF.md, README.md y PROJECT.md en ese orden. Proporciona un plan antes de modificar el código.
  ```

## 10. Mapa rápido de archivos
- **Archivos clave**:
  - HANDOFF.md: Documento maestro.
  - README.md: Información general.

## 11. Glosario
- **Términos clave**:
  - Definiciones de términos importantes.

---

## 5. Decisión de licencia (pendiente)

El archivo [LICENSE](LICENSE) actual es un placeholder. Antes del primer push externo:

- **Código privado del repo principal** (medimind-mcp pre-MVP): all-rights-reserved.
- **Cuando MediMind se publique**: Apache-2.0 o BSL-1.1 (si se monetiza versión hosted).
- **Spec OWASP MCP Top 10**: CC-BY-4.0.
- **Capítulos del libro publicados sueltos**: CC-BY-NC-ND-4.0.
- **Libro completo vendido**: copyright reservado, EULA estándar de Gumroad/Leanpub.

Confirmar con el humano y reemplazar [LICENSE](LICENSE).

---

## 6. Comandos útiles para Codex / asistente que retome

```powershell
# Verificar estado del repo antes de cualquier commit
cd c:\VM\mcp
git status
git status --ignored | Select-String "_local"   # debe aparecer _local/ ignorado

# Búsqueda de secretos antes de push
Get-ChildItem -Recurse -Force -Filter ".env" | Where-Object { $_.FullName -notmatch "_local" }
Select-String -Path "*.md","**/*.md" -Pattern "(sk-|AKIA|api[_-]?key|password|secret)" -CaseSensitive:$false | Where-Object { $_.Path -notmatch "_local|node_modules" }

# Crear repo público separado para spec OSS (cuando proceda)
# (no ejecutar sin confirmación humana)
gh repo create owasp-mcp-top-10 --public --description "Top 10 security antipatterns in Model Context Protocol servers"

# Inicializar repo principal en GitHub privado
gh repo create mcp-en-produccion --private --source . --remote origin
```

---

## 7. Glosario express para el asistente

- **Etapa 1:** validación de mercado, semana 1 (5-7 entrevistas).
- **Combo C+A→E:** consultoría (cash) + libro lean (marca) → toolkit OSS (apuesta).
- **C, A, B, D, E:** ver [mayo2026/README.md](mayo2026/README.md) tabla comparativa.
- **PHI:** Protected Health Information (datos sanitarios protegidos).
- **MCP:** Model Context Protocol (Anthropic, 2024).
- **STRIDE-MCP:** adaptación del modelo de amenazas STRIDE al contexto MCP, definida en cap. 2 del libro.
- **OWASP MCP Top 10:** spec en redacción en este repo, será proyecto OWASP en v1.0.

---

## 8. Cosas que NO están hechas (para evitar que Codex las re-haga sin necesidad)

Estas tareas están deliberadamente sin hacer porque dependen de la validación o de decisiones del humano. **No las anticipes.**

- ❌ Capítulos 2-5 redactados (esperan validación).
- ❌ Sales page publicada en web (esperan validación + datos LSSI-CE).
- ❌ Repo OSS público creado (espera decisión de visibilidad).
- ❌ Email kit configurado en proveedor (espera decisión de proveedor).
- ❌ MediMind con tools clínicos completos (no es necesario hasta cap. 4).
- ❌ Tests automáticos en MediMind (no priorizar antes de validar libro).
- ❌ Casos de éxito reales en sales page (no hay clientes todavía).
- ❌ Pricing definitivo (esperar reacciones reales).
- ❌ Plantillas legales de contratos (esperar abogado humano).

Si alguna de estas aparece como "completa" cuando retomes el proyecto: verifica con el humano que efectivamente se hizo y no es un alucinado por un asistente anterior.

---

## 12. Estado de las pruebas automáticas
- **Estado actual**: No se han implementado pruebas automáticas en MediMind.
- **Próximos pasos**:
  - Diseñar e implementar pruebas para las áreas críticas del proyecto.
  - Priorizar pruebas de seguridad y funcionalidad básica.
  - Utilizar `pytest` como framework de pruebas.

---
