# Workflow de investigacion de personas

> Usar despues de `06-organizaciones-objetivo.md`. El objetivo es pasar de
> organizaciones a 30 contactos reales sin caer en mensajes genericos.

## Campos minimos antes de enviar

Un contacto no esta listo hasta tener:

| Campo | Requisito |
|---|---|
| Nombre | Persona concreta, no empresa ni equipo generico. |
| Empresa | Empresa actual verificada. |
| Rol | Rol actual o razonable para decidir/prescribir seguridad, IA, plataforma o compliance. |
| Perfil | Uno de los 8 perfiles objetivo de la validacion. |
| Hueco personalizacion | Senal publica concreta y reciente, o al menos muy verificable. |

## Secuencia de verificacion

1. Confirmar que la organizacion encaja con uno de los segmentos objetivo.
2. Buscar persona con rol tecnico, seguridad, IA, plataforma, producto o compliance.
3. Confirmar que la persona sigue vinculada a la organizacion.
4. Encontrar una senal concreta:
   - post o charla reciente,
   - repo o producto publico,
   - noticia de financiacion/lanzamiento,
   - oferta de empleo que muestre IA, seguridad, FHIR, compliance o plataforma,
   - certificacion o pagina de seguridad de la empresa.
5. Escribir el hueco de personalizacion en una frase.
6. Ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-validacion.ps1
powershell -ExecutionPolicy Bypass -File .\tools\generate-mensajes-validacion.ps1
```

7. Revisar a mano `mensajes-generados.local.md` antes de enviar.

## Rechazar candidatos

Descartar si:

- Solo hay nombre y cargo, sin senal personalizable.
- La persona parece demasiado junior para opinar sobre compra, riesgo o arquitectura.
- La empresa no tiene IA, compliance, datos sensibles, MCP, plataforma o seguridad como tension real.
- La personalizacion empieza a sonar como "vi tu perfil".

## Orden recomendado para completar los 30

1. 8 contactos con MCP real o developer tooling.
2. 6 contactos healthtech/FHIR/datos sensibles.
3. 6 contactos fintech/insurtech/regulacion.
4. 5 contactos seguridad/GRC/auditoria.
5. 5 contactos consultoria IA/plataforma.

Este reparto da variedad suficiente para decidir verde/ambar/rojo sin sesgar
todo hacia un unico sector.

