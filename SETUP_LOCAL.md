# Setup local del proyecto

Estado preparado el 2026-05-02 para ejecutar la Etapa 1 sin mezclar datos
privados con material publicable.

## Herramientas instaladas / verificadas

| Herramienta | Estado | Nota |
|---|---|---|
| Git | OK | Repo local inicializado. No hay remoto configurado. |
| Python 3.11 | OK | Entorno recreado en `.venv/`. |
| GitHub CLI | OK | Instalado como `C:\Program Files\GitHub CLI\gh.exe`. Reabrir terminal si `gh` no aparece en PATH. |
| Docker | Pendiente | No es necesario para Etapa 1. Instalar solo cuando se retome MediMind tecnico. |

## Comandos utiles

Activar Python:

```powershell
.\.venv\Scripts\Activate.ps1
python --version
```

Si `python` sigue apuntando al stub de Microsoft Store, usar la ruta directa:

```powershell
.\.venv\Scripts\python.exe --version
```

Verificar entorno:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-entorno.ps1
```

Verificar estado de validacion:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-validacion.ps1
```

Generar borradores locales de mensajes desde el tracker:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\generate-mensajes-validacion.ps1
```

La salida queda en `_local/validacion/semana-1/mensajes-generados.local.md`.

Revisar calidad de mensajes antes de enviar:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-mensajes-validacion.ps1
```

Generar plan local de envio por lotes:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\generate-plan-envio-validacion.ps1
```

Marcar filas como enviadas despues de cada lote:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\update-tracker-status.ps1 -Ids 1,2,3,4,5,6,7,8,9,10 -Estado enviado
```

## Flujo inmediato

1. Rellenar `_local/validacion/semana-1/CONFIG.local.md`.
2. Ejecutar `check-validacion.ps1`.
3. Generar mensajes y revisar con `check-mensajes-validacion.ps1`.
4. Generar plan de envio por lotes.
5. Enviar mensajes y marcar estados con `update-tracker-status.ps1`.
6. Guardar notas reales en `_local/validacion/semana-1/notas/`.
7. Al cerrar entrevistas, copiar solo datos agregados y anonimizados a `mayo2026/ejecucion/semana-1/04-sintesis-dia-7.md`.

## Reglas de seguridad

- No subir `_local/` a ningun remoto.
- No publicar `mayo2026/` en un repo publico: contiene estrategia comercial.
- No crear repos publicos (`web-mcp-produccion`, `owasp-mcp-top-10`) hasta tener decision VERDE.
- No instalar dependencias pesadas de MediMind ni levantar Docker hasta que la validacion lo justifique.
