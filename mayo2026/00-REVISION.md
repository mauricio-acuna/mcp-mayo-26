# Revisión crítica del proyecto — mayo 2026

> Lectura del estado del repo tras el pivote de abril ([PIVOTE_2026.md](../PIVOTE_2026.md)).
> Objetivo: identificar qué está funcionando, qué riesgos persisten y qué decisiones quedan abiertas antes de invertir más tiempo.

---

## 1. Lo que está bien resuelto

- **Tesis del pivote es correcta.** MCP es commodity en abril 2026; competir en "tu primer MCP server" es perder. El foco en seguridad/compliance/operación es donde la IA generativa todavía no entrega bien.
- **Recorte agresivo de alcance.** Pasar de 3 casos (DataBridge, MarketPulse, MediMind) a uno solo (MediMind) reduce riesgo de ejecución y permite profundidad.
- **Idioma primario español** evita competir con un océano de contenido en inglés y aprovecha un nicho mal servido.
- **Ángulo defendible:** HIPAA + FHIR es la única de las tres áreas originales con barrera regulatoria real.
- **Material conservado del libro original** ([appendix-e-security-checklist.md](../book-manuscript/appendix-e-security-checklist.md), [10-chapter-security-authentication.md](../book-manuscript/10-chapter-security-authentication.md)) es directamente reutilizable.

## 2. Riesgos no resueltos por el pivote

### 2.1 Validación de mercado pendiente
El paso 1 del pivote pide *"5 entrevistas a CTOs/arquitectos de health-tech en español"*. **No hay evidencia en el repo de que se hayan hecho.** Sin esa validación se está construyendo a ciegas un libro/producto que asume:

- que el comprador habla español como idioma de trabajo técnico,
- que health-tech hispanohablante adopta MCP en horizonte 6-12 meses,
- que prefiere libro/curso sobre consultoría o herramienta.

Las tres asunciones pueden ser falsas individualmente. La probabilidad de que las tres sean simultáneamente verdaderas es baja sin evidencia.

### 2.2 Conflicto producto vs. contenido
El plan trata MediMind como **caso de estudio del libro** *y* como **producto activo** simultáneamente. Eso choca:

- Un caso pedagógico requiere código simple, didáctico, opinionado.
- Un producto vendible requiere código robusto, multi-tenant, certificable.

Quien intenta ambos termina con un código mediocre para las dos cosas. El [RESUMEN_IMPLEMENTACION.md](../medimind-mcp/RESUMEN_IMPLEMENTACION.md) ya muestra el síntoma: 45% completado, 0% tests, 15-25 días para llegar a "100%" — y ese 100% sigue siendo prototipo, no producto certificable.

### 2.3 Coste oculto de HIPAA real
El libro promete "HIPAA traducido a controles técnicos". Para que eso sea creíble el autor necesita:

- Acceso a un entorno FHIR real (Epic sandbox no basta para producción).
- BAA con al menos un proveedor LLM (Anthropic/OpenAI tienen, pero requieren contrato enterprise).
- Idealmente, un revisor con experiencia HIPAA real (no solo lectura del texto legal).

Sin eso el libro queda en "checklist + ejemplos plausibles", que es exactamente lo que la IA generativa ya hace.

### 2.4 Canal de distribución poco claro
El pivote descarta KDP y menciona "Gumroad / Leanpub / Maven". Esos canales requieren **audiencia preexistente**. No hay en el repo una lista de correo, newsletter activa, ni presencia en comunidad MCP hispanohablante. El libro sin canal es invisible.

### 2.5 Monetización del libro es la peor de las opciones
A precio razonable (€25-40) y con un mercado nicho (health-tech ES + interés en MCP + interés en compliance), el techo realista del libro solo son **bajos miles de euros/año**. El esfuerzo de escribir 200 páginas técnicas correctas no se amortiza con eso. Hay caminos con mejor ratio esfuerzo/ingreso (§ opciones B–E).

## 3. Activos reales del proyecto (independientes del formato final)

Estos sobreviven a cualquier pivote ulterior:

1. **Conocimiento estructurado** sobre superficie de ataque MCP, redacción de PHI, auditoría LLM→MCP→datos.
2. **Repositorio MediMind** con esqueleto FastAPI + FHIR + audit + encryption (45% pero arquitectura correcta).
3. **Checklist de seguridad** y capítulo de auth ya redactados.
4. **TOC reescrito** que ya filtra lo que es commodity de lo que no.
5. **Idioma español** como diferenciador de canal.

Cualquier camino futuro debe partir de explotar estos activos, no de tirarlos.

## 4. Preguntas abiertas que el repo no responde

1. ¿El autor tiene experiencia clínica/healthcare real, o el ángulo HIPAA es aspiracional?
2. ¿Hay tiempo y capital para 6-9 meses sin ingresos hasta lanzar el libro?
3. ¿Hay red profesional en hospitales/health-tech hispanohablantes para distribución directa?
4. ¿Se acepta vender consultoría/servicios o el objetivo es producto pasivo?
5. ¿Cuál es el horizonte? (12 meses cash → consultoría; 36 meses construir audiencia → producto)

Las cinco opciones del directorio responden a combinaciones distintas de estas respuestas.

## 5. Mapa de opciones alternativas

| Opción | Inversión | Time to revenue | Techo | Riesgo |
|---|---|---|---|---|
| **A** Libro lean + lead magnet | Bajo | 3-4 meses | €5-15k/año | Bajo |
| **B** MediMind como SaaS | Muy alto | 12-18 meses | €1M+ ARR | Muy alto |
| **C** Consultoría / auditoría MCP-security | Medio | 1-3 meses | €100-250k/año | Medio |
| **D** Curso por cohortes en español | Medio | 4-6 meses | €30-80k/año | Medio |
| **E** Toolkit OSS + tier enterprise | Alto | 9-12 meses | €100-500k/año | Alto |

Detalle de cada una en los documentos `OPCION-*.md`. Mi síntesis en [RECOMENDACION.md](RECOMENDACION.md).
