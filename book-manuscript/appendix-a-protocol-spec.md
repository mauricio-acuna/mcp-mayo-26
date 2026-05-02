# Appendix A: MCP Protocol Specification Reference

This appendix provides a comprehensive reference for the Model Context Protocol (MCP) specification as of version 2024-11-05.

## Protocol Overview

MCP uses JSON-RPC 2.0 as its base communication protocol, with additional conventions for LLM-specific functionality.

### Transport Layers

MCP supports multiple transport mechanisms:

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Local execution | Simple, no networking | Single user only |
| **SSE** | Remote servers | HTTP-based, firewall-friendly | One-direction server push |
| **HTTP** | RESTful APIs | Standard, well-understood | Stateless, polling required |

## JSON-RPC 2.0 Base

### Request Format

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

**Fields:**
- `jsonrpc` (required): Must be exactly "2.0"
- `id` (optional): Request identifier. Omit for notifications.
- `method` (required): The method to invoke
- `params` (optional): Parameters for the method

### Response Format

**Success Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "data": "response_data"
  }
}
```

**Error Response:**
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

### Standard Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | JSON-RPC structure invalid |
| -32601 | Method not found | Method doesn't exist |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Server internal error |

## MCP Lifecycle Methods

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

**Client Capabilities:**
- `roots`: Client can provide filesystem roots
  - `listChanged`: Client supports notifications when roots change
- `sampling`: Client supports sampling requests

**Server Capabilities:**
- `tools`: Server provides tools
  - `listChanged`: Server sends notifications when tool list changes
- `resources`: Server provides resources
  - `subscribe`: Server supports resource subscriptions
  - `listChanged`: Server sends notifications when resource list changes
- `prompts`: Server provides prompts
  - `listChanged`: Server sends notifications when prompt list changes

### 2. initialized

**Notification (no response):**
```json
{
  "jsonrpc": "2.0",
  "method": "initialized"
}
```

Sent by client after processing initialize response. Indicates client is ready.

## Tools API

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

**Tool Definition:**
- `name` (required): Unique tool identifier
- `description` (required): Human-readable description
- `inputSchema` (required): JSON Schema for input validation

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

**Content Types:**
- `text`: Plain text response
- `image`: Base64-encoded image (future)
- `resource`: Reference to a resource (future)

**Error Handling:**
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

## Resources API

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

**Resource Definition:**
- `uri` (required): Unique resource identifier (URI format)
- `name` (required): Human-readable name
- `description` (optional): Detailed description
- `mimeType` (optional): Content MIME type

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

**Content Types:**
- Text content: `text` field with string
- Binary content: `blob` field with base64 string (future)

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

**Update Notification (from server):**
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

## Prompts API

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

## Notifications

Notifications are one-way messages (no response expected).

### notifications/tools/list_changed

**From Server:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

Indicates client should call `tools/list` again.

### notifications/resources/list_changed

**From Server:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/list_changed"
}
```

### notifications/resources/updated

**From Server:**
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

**From Server:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/prompts/list_changed"
}
```

## Progress Notifications

For long-running operations:

**Progress Token in Request:**
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

**Progress Notifications:**
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

## Sampling (Future)

For servers to request LLM completions:

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

## URI Schemes

MCP defines URI schemes for resource identification:

### Standard Schemes

- `file://` - File system resources
- `http://` / `https://` - Web resources
- Custom schemes - Server-defined (e.g., `market://`, `database://`)

### URI Format

```
scheme://authority/path?query#fragment
```

**Examples:**
```
file:///home/user/document.txt
market://btc/price
database://users/12345
api://github/repos/owner/repo
```

### Best Practices

1. **Use descriptive schemes**: `market://` instead of `m://`
2. **Hierarchical paths**: `market://crypto/btc/price`
3. **Query parameters**: `market://btc/price?currency=usd`
4. **Case insensitive**: Treat URIs case-insensitively

## Content Types

### Text Content

```json
{
  "type": "text",
  "text": "String content here"
}
```

### Image Content (Future)

```json
{
  "type": "image",
  "data": "base64_encoded_image_data",
  "mimeType": "image/png"
}
```

### Resource Reference (Future)

```json
{
  "type": "resource",
  "uri": "resource://identifier"
}
```

## Input Schema (JSON Schema)

Tools use JSON Schema (draft-07) for input validation:

### Basic Types

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

### Nested Objects

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

### Conditional Schemas

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

## Versioning

Protocol version format: `YYYY-MM-DD`

**Current version:** `2024-11-05`

### Version Negotiation

1. Client sends preferred version in `initialize`
2. Server responds with supported version
3. If versions incompatible, server returns error
4. Client may retry with different version

### Backward Compatibility

- Additive changes don't require version bump
- Breaking changes require new version
- Servers should support multiple versions when possible

## Security Considerations

### Authentication

Not specified by protocol. Implementations should:
- Use OAuth 2.0 for user authentication
- Use API keys for programmatic access
- Implement rate limiting

### Authorization

- Validate user permissions before operations
- Implement resource-level access control
- Log all access attempts

### Input Validation

- Validate all inputs against schema
- Sanitize inputs to prevent injection
- Limit input sizes to prevent DoS

### Error Messages

- Don't expose internal details in errors
- Use generic error messages for security issues
- Log detailed errors server-side

## Best Practices

### Tool Design

1. **Clear naming**: Use verb_noun format (e.g., `get_weather`)
2. **Detailed descriptions**: Include examples in descriptions
3. **Sensible defaults**: Make optional parameters truly optional
4. **Error handling**: Return helpful error messages
5. **Idempotency**: Repeated calls should have same effect

### Resource Design

1. **Stable URIs**: Don't change URIs unnecessarily
2. **Hierarchical**: Use path hierarchy for organization
3. **Discoverable**: Provide resource listings
4. **Efficient**: Cache aggressively, invalidate correctly

### Performance

1. **Pagination**: Limit result sizes, provide pagination
2. **Caching**: Cache expensive operations
3. **Async**: Use async operations for long tasks
4. **Timeouts**: Set reasonable timeouts

### Reliability

1. **Retries**: Implement exponential backoff
2. **Circuit breakers**: Fail fast when downstream broken
3. **Graceful degradation**: Provide partial results if possible
4. **Health checks**: Expose health/readiness endpoints

## Examples

### Complete Tool Call Flow

```
Client → Server: initialize
Server → Client: InitializeResult
Client → Server: initialized (notification)
Client → Server: tools/list
Server → Client: ToolsList
Client → Server: tools/call(name="search", args={query: "MCP"})
Server → Client: CallToolResult
```

### Complete Resource Flow

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

## Reference Implementations

- **TypeScript**: `@modelcontextprotocol/sdk`
- **Python**: `mcp` package
- **Rust**: Community implementations

## Further Reading

- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [JSON Schema Documentation](https://json-schema.org/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Documentation](https://modelcontextprotocol.io/)

---

*This appendix reflects MCP specification version 2024-11-05. Check official documentation for updates.*
