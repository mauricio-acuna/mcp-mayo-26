# Apéndice A: Referencia de Especificación del Protocolo MCP

Este apéndice proporciona una referencia comprensiva para la especificación del Model Context Protocol (MCP) versión 2024-11-05.

## Visión General del Protocolo

MCP usa JSON-RPC 2.0 como su protocolo de comunicación base, con convenciones adicionales para funcionalidad específica de LLM.

### Capas de Transporte

MCP soporta múltiples mecanismos de transporte:

| Transporte | Caso de Uso | Pros | Contras |
|-----------|----------|------|------|
| **stdio** | Ejecución local | Simple, sin networking | Solo un usuario |
| **SSE** | Servidores remotos | Basado en HTTP, amigable con firewalls | Push unidireccional del servidor |
| **HTTP** | APIs RESTful | Estándar, bien entendido | Stateless, polling requerido |

## Base JSON-RPC 2.0

### Formato de Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Campos:**
- `jsonrpc` (requerido): Debe ser exactamente "2.0"
- `id` (opcional): Identificador de request. Omitir para notificaciones.
- `method` (requerido): El método a invocar
- `params` (opcional): Parámetros para el método

### Formato de Response

**Response de Éxito:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "data": "response_data"
  }
}
```

**Response de Error:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": {
      "details": "Additional error information"
    }
  }
}
```

### Códigos de Error Estándar

| Código | Mensaje | Significado |
|------|---------|---------|
| -32700 | Parse error | JSON inválido |
| -32600 | Invalid Request | Estructura JSON-RPC inválida |
| -32601 | Method not found | El método no existe |
| -32602 | Invalid params | Parámetros de método inválidos |
| -32603 | Internal error | Error interno del servidor |

## Métodos de Ciclo de Vida MCP

### 1. initialize

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "ExampleClient",
      "version": "1.0.0"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {
        "listChanged": false
      },
      "resources": {
        "subscribe": true,
        "listChanged": false
      },
      "prompts": {
        "listChanged": false
      }
    },
    "serverInfo": {
      "name": "ExampleServer",
      "version": "1.0.0"
    }
  }
}
```

**Capabilities:**

**Capabilities del Cliente:**
- `roots`: El cliente puede proporcionar filesystem roots
  - `listChanged`: El cliente soporta notificaciones cuando los roots cambian
- `sampling`: El cliente soporta sampling requests

**Capabilities del Servidor:**
- `tools`: El servidor proporciona tools
  - `listChanged`: El servidor envía notificaciones cuando la lista de tools cambia
- `resources`: El servidor proporciona resources
  - `subscribe`: El servidor soporta suscripciones a resources
  - `listChanged`: El servidor envía notificaciones cuando la lista de resources cambia
- `prompts`: El servidor proporciona prompts
  - `listChanged`: El servidor envía notificaciones cuando la lista de prompts cambia

### 2. initialized

**Notificación (sin response):**
```json
{
  "jsonrpc": "2.0",
  "method": "initialized"
}
```

Enviada por el cliente después de procesar la response de initialize. Indica que el cliente está listo.

## API de Tools

### tools/list

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name or coordinates"
            },
            "units": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"],
              "default": "celsius"
            }
          },
          "required": ["location"]
        }
      }
    ]
  }
}
```

**Definición de Tool:**
- `name` (requerido): Identificador único del tool
- `description` (requerido): Descripción legible por humanos
- `inputSchema` (requerido): JSON Schema para validación de input

### tools/call

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "location": "San Francisco",
      "units": "fahrenheit"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in San Francisco: 65°F, partly cloudy"
      }
    ],
    "isError": false
  }
}
```

**Tipos de Content:**
- `text`: Response de texto plano
- `image`: Imagen codificada en Base64 (futuro)
- `resource`: Referencia a un resource (futuro)

**Manejo de Errores:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Error: Location not found"
      }
    ],
    "isError": true
  }
}
```

## API de Resources

### resources/list

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "resources": [
      {
        "uri": "file:///docs/readme.md",
        "name": "README",
        "description": "Project README file",
        "mimeType": "text/markdown"
      },
      {
        "uri": "weather://current/san-francisco",
        "name": "San Francisco Weather",
        "description": "Current weather data",
        "mimeType": "application/json"
      }
    ]
  }
}
```

**Definición de Resource:**
- `uri` (requerido): Identificador único de resource (formato URI)
- `name` (requerido): Nombre legible por humanos
- `description` (opcional): Descripción detallada
- `mimeType` (opcional): Tipo MIME del contenido

### resources/read

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/read",
  "params": {
    "uri": "file:///docs/readme.md"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "contents": [
      {
        "uri": "file:///docs/readme.md",
        "mimeType": "text/markdown",
        "text": "# Project Title\n\nProject description..."
      }
    ]
  }
}
```

**Tipos de Contenido:**
- Contenido de texto: campo `text` con string
- Contenido binario: campo `blob` con string base64 (futuro)

### resources/subscribe

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "resources/subscribe",
  "params": {
    "uri": "weather://current/san-francisco"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {}
}
```

**Notificación de Actualización (desde el servidor):**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "weather://current/san-francisco"
  }
}
```

### resources/unsubscribe

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "resources/unsubscribe",
  "params": {
    "uri": "weather://current/san-francisco"
  }
}
```

## API de Prompts

### prompts/list

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "prompts/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "prompts": [
      {
        "name": "code_review",
        "description": "Review code for best practices",
        "arguments": [
          {
            "name": "language",
            "description": "Programming language",
            "required": true
          },
          {
            "name": "code",
            "description": "Code to review",
            "required": true
          }
        ]
      }
    ]
  }
}
```

### prompts/get

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "language": "python",
      "code": "def hello():\n    print('Hello')"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Review this Python code:\n\n```python\ndef hello():\n    print('Hello')\n```\n\nProvide feedback on..."
        }
      }
    ]
  }
}
```

## Notificaciones

Las notificaciones son mensajes unidireccionales (no se espera response).

### notifications/tools/list_changed

**Desde el Servidor:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

Indica que el cliente debe llamar a `tools/list` nuevamente.

### notifications/resources/list_changed

**Desde el Servidor:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/list_changed"
}
```

### notifications/resources/updated

**Desde el Servidor:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "resource://identifier"
  }
}
```

### notifications/prompts/list_changed

**Desde el Servidor:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/prompts/list_changed"
}
```

## Notificaciones de Progreso

Para operaciones de larga duración:

**Token de Progreso en Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "process_large_file",
    "arguments": {
      "file": "large.csv"
    },
    "_meta": {
      "progressToken": "progress-123"
    }
  }
}
```

**Notificaciones de Progreso:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "progress-123",
    "progress": 25.5,
    "total": 100
  }
}
```

## Sampling (Futuro)

Para que los servidores soliciten completions de LLM:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Analyze this data..."
        }
      }
    ],
    "maxTokens": 1000
  }
}
```

## Esquemas URI

MCP define esquemas URI para identificación de resources:

### Esquemas Estándar

- `file://` - Resources del sistema de archivos
- `http://` / `https://` - Resources web
- Esquemas personalizados - Definidos por el servidor (ej., `market://`, `database://`)

### Formato URI

```
scheme://authority/path?query#fragment
```

**Ejemplos:**
```
file:///home/user/document.txt
market://btc/price
database://users/12345
api://github/repos/owner/repo
```

### Mejores Prácticas

1. **Usar esquemas descriptivos**: `market://` en lugar de `m://`
2. **Paths jerárquicos**: `market://crypto/btc/price`
3. **Parámetros de query**: `market://btc/price?currency=usd`
4. **Case insensitive**: Tratar URIs sin distinción de mayúsculas/minúsculas

## Tipos de Contenido

### Contenido de Texto

```json
{
  "type": "text",
  "text": "String content here"
}
```

### Contenido de Imagen (Futuro)

```json
{
  "type": "image",
  "data": "base64_encoded_image_data",
  "mimeType": "image/png"
}
```

### Referencia a Resource (Futuro)

```json
{
  "type": "resource",
  "uri": "resource://identifier"
}
```

## Input Schema (JSON Schema)

Los tools usan JSON Schema (draft-07) para validación de input:

### Tipos Básicos

```json
{
  "type": "object",
  "properties": {
    "string_param": {
      "type": "string",
      "description": "A string parameter"
    },
    "number_param": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "boolean_param": {
      "type": "boolean",
      "default": true
    },
    "array_param": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["string_param"]
}
```

### Enums

```json
{
  "type": "string",
  "enum": ["option1", "option2", "option3"],
  "default": "option1"
}
```

### Objetos Anidados

```json
{
  "type": "object",
  "properties": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "zip": { "type": "string" }
      },
      "required": ["city"]
    }
  }
}
```

### Schemas Condicionales

```json
{
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "enum": ["email", "sms"]
    }
  },
  "required": ["type"],
  "allOf": [
    {
      "if": {
        "properties": { "type": { "const": "email" } }
      },
      "then": {
        "properties": {
          "email": { "type": "string", "format": "email" }
        },
        "required": ["email"]
      }
    },
    {
      "if": {
        "properties": { "type": { "const": "sms" } }
      },
      "then": {
        "properties": {
          "phone": { "type": "string" }
        },
        "required": ["phone"]
      }
    }
  ]
}
```

## Versionado

Formato de versión del protocolo: `YYYY-MM-DD`

**Versión actual:** `2024-11-05`

### Negociación de Versión

1. El cliente envía la versión preferida en `initialize`
2. El servidor responde con la versión soportada
3. Si las versiones son incompatibles, el servidor retorna error
4. El cliente puede reintentar con diferente versión

### Compatibilidad Hacia Atrás

- Cambios aditivos no requieren bump de versión
- Cambios breaking requieren nueva versión
- Los servidores deben soportar múltiples versiones cuando sea posible

## Consideraciones de Seguridad

### Autenticación

No especificada por el protocolo. Las implementaciones deben:
- Usar OAuth 2.0 para autenticación de usuario
- Usar API keys para acceso programático
- Implementar rate limiting

### Autorización

- Validar permisos de usuario antes de operaciones
- Implementar control de acceso a nivel resource
- Registrar todos los intentos de acceso

### Validación de Input

- Validar todos los inputs contra el schema
- Sanitizar inputs para prevenir inyección
- Limitar tamaños de input para prevenir DoS

### Mensajes de Error

- No exponer detalles internos en errores
- Usar mensajes de error genéricos para issues de seguridad
- Registrar errores detallados del lado del servidor

## Mejores Prácticas

### Diseño de Tools

1. **Naming claro**: Usar formato verbo_sustantivo (ej., `get_weather`)
2. **Descripciones detalladas**: Incluir ejemplos en las descripciones
3. **Defaults sensibles**: Hacer que parámetros opcionales sean verdaderamente opcionales
4. **Manejo de errores**: Retornar mensajes de error útiles
5. **Idempotencia**: Llamadas repetidas deben tener el mismo efecto

### Diseño de Resources

1. **URIs estables**: No cambiar URIs innecesariamente
2. **Jerárquico**: Usar jerarquía de path para organización
3. **Discoverable**: Proporcionar listados de resources
4. **Eficiente**: Cachear agresivamente, invalidar correctamente

### Rendimiento

1. **Paginación**: Limitar tamaños de resultado, proporcionar paginación
2. **Caching**: Cachear operaciones costosas
3. **Async**: Usar operaciones async para tareas largas
4. **Timeouts**: Establecer timeouts razonables

### Confiabilidad

1. **Reintentos**: Implementar exponential backoff
2. **Circuit breakers**: Fallar rápido cuando downstream esté roto
3. **Degradación elegante**: Proporcionar resultados parciales si es posible
4. **Health checks**: Exponer endpoints de health/readiness

## Ejemplos

### Flujo Completo de Tool Call

```
Client → Server: initialize
Server → Client: InitializeResult
Client → Server: initialized (notification)
Client → Server: tools/list
Server → Client: ToolsList
Client → Server: tools/call(name="search", args={query: "MCP"})
Server → Client: CallToolResult
```

### Flujo Completo de Resource

```
Client → Server: resources/list
Server → Client: ResourcesList
Client → Server: resources/subscribe(uri="market://btc")
Server → Client: {} (success)
Server → Client: notifications/resources/updated (when changed)
Client → Server: resources/read(uri="market://btc")
Server → Client: ReadResourceResult
Client → Server: resources/unsubscribe(uri="market://btc")
```

## Implementaciones de Referencia

- **TypeScript**: `@modelcontextprotocol/sdk`
- **Python**: paquete `mcp`
- **Rust**: Implementaciones de la comunidad

## Lectura Adicional

- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [JSON Schema Documentation](https://json-schema.org/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Documentation](https://modelcontextprotocol.io/)

---

*Este apéndice refleja la versión 2024-11-05 de la especificación MCP. Consulte la documentación oficial para actualizaciones.*
