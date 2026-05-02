# CapÃ­tulo 10: Seguridad y AutenticaciÃ³n

## IntroducciÃ³n

DataBridge se conecta a **fuentes de datos sensibles** (bases de datos financieras, registros de clientes, datos de salud). La seguridad no es opcionalâ€”es la **base de la confianza**.

En este capÃ­tulo, implementaremos:

1. **AutenticaciÃ³n** - Verificar quiÃ©n hace las solicitudes (OAuth 2.0, API keys)
2. **AutorizaciÃ³n** - Controlar quÃ© pueden acceder los usuarios (RBAC, seguridad a nivel de fila)
3. **Cifrado** - Proteger datos en reposo y en trÃ¡nsito (AES-256, TLS 1.3)
4. **GestiÃ³n de Secretos** - Almacenar credenciales de forma segura (HashiCorp Vault)
5. **Logging de AuditorÃ­a** - Rastrear cada acciÃ³n para cumplimiento (SOC 2, GDPR)
6. **LimitaciÃ³n de Tasa** - Prevenir abuso (cuotas por tier)

**Arquitectura de Seguridad:**

```
Client Request
    â†“
TLS 1.3 (Encryption in Transit)
    â†“
API Gateway (Rate Limiting)
    â†“
Authentication Middleware (JWT verification)
    â†“
Authorization Check (RBAC + Row-Level Security)
    â†“
Tool Execution (with audit logging)
    â†“
Credentials Decryption (HashiCorp Vault)
    â†“
Database Query (encrypted at rest)
    â†“
Response (sanitized, no PII leakage)
```

**Requisitos de Cumplimiento:**

| Framework | Requisitos | ImplementaciÃ³n DataBridge |
|-----------|-------------|---------------------------|
| **SOC 2 Type II** | Controles de acceso, audit trails, cifrado | OAuth 2.0, audit logs, AES-256 |
| **GDPR** | MinimizaciÃ³n de datos, derecho al olvido, cifrado | RedacciÃ³n PII, soft delete, cifrado |
| **HIPAA** | Cifrado PHI, logs de acceso, BAA | Vault secrets, audit logs, cifrado |
| **PCI DSS** | Cifrado datos tarjetas, logs acceso | TLS 1.3, AES-256, rate limiting |

**InversiÃ³n de Tiempo:** 6-7 horas para implementar autenticaciÃ³n, cifrado, gestiÃ³n de secretos y logging de auditorÃ­a.

---

## 10.1 AutenticaciÃ³n: OAuth 2.0 + API Keys

DataBridge soporta **dos mÃ©todos de autenticaciÃ³n**:

1. **OAuth 2.0** - Para apps web/mÃ³viles (acceso delegado)
2. **API Keys** - Para servidor-a-servidor (clientes MCP)

### Flujo de AutenticaciÃ³n

**OAuth 2.0 (Authorization Code Flow):**

```
1. User clicks "Connect Google Workspace"
2. Redirect to Google OAuth consent screen
3. User approves scopes (read email, calendar)
4. Google redirects back with authorization code
5. Exchange code for access token + refresh token
6. Store tokens in Vault (encrypted)
7. Use access token for API requests
```

**API Key (Direct Access):**

```
1. User creates API key in DataBridge dashboard
2. API key stored in database (hashed with bcrypt)
3. Client includes API key in MCP request header: X-API-Key: db_xxx
4. Server validates API key, retrieves organization
5. Proceed with request
```

### ImplementaciÃ³n de API Key

Crea `packages/server/src/auth/api-key.ts`:

```typescript
import { getPrismaClient } from '../db/client.js';
import { logger } from '../utils/logger.js';
import * as bcrypt from 'bcrypt';
import { randomBytes } from 'crypto';

const SALT_ROUNDS = 12;

/**
 * Generate a new API key for an organization
 */
export async function generateApiKey(organizationId: string): Promise<string> {
  const prisma = getPrismaClient();

  // Generate random key (32 bytes = 64 hex chars)
  const rawKey = randomBytes(32).toString('hex');
  const apiKey = `db_${rawKey}`; // Prefix for easy identification

  // Hash the key for storage (never store plaintext!)
  const hashedKey = await bcrypt.hash(apiKey, SALT_ROUNDS);

  // Update organization with hashed key
  await prisma.organization.update({
    where: { id: organizationId },
    data: { apiKey: hashedKey },
  });

  logger.info('API key generated', { organizationId });

  // Return plaintext key ONCE (user must save it)
  return apiKey;
}

/**
 * Validate API key and return organization
 */
export async function validateApiKey(
  apiKey: string
): Promise<{ organizationId: string; tier: string } | null> {
  const prisma = getPrismaClient();

  // Find all organizations (we'll check hashes)
  const organizations = await prisma.organization.findMany({
    where: { apiKey: { not: null } },
    select: { id: true, apiKey: true, tier: true },
  });

  // Check each hashed key (constant-time comparison)
  for (const org of organizations) {
    if (org.apiKey && (await bcrypt.compare(apiKey, org.apiKey))) {
      logger.info('API key validated', { organizationId: org.id });
      return { organizationId: org.id, tier: org.tier };
    }
  }

  logger.warn('Invalid API key', { apiKey: apiKey.substring(0, 10) + '...' });
  return null;
}

/**
 * Revoke API key (delete from database)
 */
export async function revokeApiKey(organizationId: string): Promise<void> {
  const prisma = getPrismaClient();

  await prisma.organization.update({
    where: { id: organizationId },
    data: { apiKey: null },
  });

  logger.info('API key revoked', { organizationId });
}
```

### Middleware de AutenticaciÃ³n

Crea `packages/server/src/auth/middleware.ts`:

```typescript
import { validateApiKey } from './api-key.js';
import { validateJWT } from './jwt.js';
import { logger } from '../utils/logger.js';

export interface AuthContext {
  organizationId: string;
  userId?: string;
  tier: string;
  method: 'api-key' | 'oauth';
}

/**
 * Extract authentication from request headers
 */
export async function authenticate(headers: Record<string, string>): Promise<AuthContext | null> {
  // Check for API key
  const apiKey = headers['x-api-key'] || headers['authorization']?.replace('Bearer ', '');
  
  if (apiKey && apiKey.startsWith('db_')) {
    const result = await validateApiKey(apiKey);
    if (result) {
      return {
        organizationId: result.organizationId,
        tier: result.tier,
        method: 'api-key',
      };
    }
  }

  // Check for JWT (OAuth)
  const jwt = headers['authorization']?.replace('Bearer ', '');
  if (jwt && !jwt.startsWith('db_')) {
    const decoded = await validateJWT(jwt);
    if (decoded) {
      return {
        organizationId: decoded.organizationId,
        userId: decoded.userId,
        tier: decoded.tier,
        method: 'oauth',
      };
    }
  }

  logger.warn('Authentication failed', { headers: Object.keys(headers) });
  return null;
}
```

### ImplementaciÃ³n de JWT (OAuth 2.0)

Crea `packages/server/src/auth/jwt.ts`:

```typescript
import jwt from 'jsonwebtoken';
import { logger } from '../utils/logger.js';

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-CHANGE-IN-PRODUCTION';
const JWT_EXPIRY = '24h';

export interface JWTPayload {
  organizationId: string;
  userId: string;
  tier: string;
  email: string;
  role: string;
}

/**
 * Create JWT token for authenticated user
 */
export function createJWT(payload: JWTPayload): string {
  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: JWT_EXPIRY,
    issuer: 'databridge-mcp',
  });
}

/**
 * Validate JWT and return payload
 */
export async function validateJWT(token: string): Promise<JWTPayload | null> {
  try {
    const decoded = jwt.verify(token, JWT_SECRET, {
      issuer: 'databridge-mcp',
    }) as JWTPayload;

    logger.debug('JWT validated', { userId: decoded.userId });
    return decoded;
  } catch (error: any) {
    logger.warn('JWT validation failed', { error: error.message });
    return null;
  }
}

/**
 * Refresh JWT (issue new token with extended expiry)
 */
export function refreshJWT(oldToken: string): string | null {
  try {
    const decoded = jwt.verify(oldToken, JWT_SECRET, {
      ignoreExpiration: true, // Allow expired tokens for refresh
    }) as JWTPayload;

    // Issue new token
    return createJWT(decoded);
  } catch (error: any) {
    logger.error('JWT refresh failed', { error: error.message });
    return null;
  }
}
```

---

## 10.2 AutorizaciÃ³n: RBAC + Seguridad a Nivel de Fila

**Control de Acceso Basado en Roles (RBAC):**

| Rol | Permisos |
|------|-------------|
| **ADMIN** | Acceso completo (crear conectores, gestionar usuarios, ver audit logs) |
| **MEMBER** | Leer/escribir datos, crear consultas, programar reportes |
| **READONLY** | Solo lectura de datos (sin escrituras, sin cambios de configuraciÃ³n) |

**Seguridad a Nivel de Fila (RLS):**
- Cada consulta filtra por `organizationId` (multi-tenancy)
- Los usuarios solo pueden acceder a los datos de su organizaciÃ³n
- Aplicado en la capa de base de datos (middleware de Prisma)

### ImplementaciÃ³n de RBAC

Crea `packages/server/src/auth/rbac.ts`:

```typescript
import { Role } from '@prisma/client';
import { logger } from '../utils/logger.js';

export enum Permission {
  // Connector permissions
  CONNECTOR_CREATE = 'connector:create',
  CONNECTOR_READ = 'connector:read',
  CONNECTOR_UPDATE = 'connector:update',
  CONNECTOR_DELETE = 'connector:delete',

  // Query permissions
  QUERY_EXECUTE = 'query:execute',
  QUERY_READ = 'query:read',

  // Write permissions
  DATA_WRITE = 'data:write',
  DATA_DELETE = 'data:delete',

  // Report permissions
  REPORT_CREATE = 'report:create',
  REPORT_READ = 'report:read',

  // User management
  USER_CREATE = 'user:create',
  USER_DELETE = 'user:delete',

  // Audit logs
  AUDIT_READ = 'audit:read',
}

const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  ADMIN: [
    Permission.CONNECTOR_CREATE,
    Permission.CONNECTOR_READ,
    Permission.CONNECTOR_UPDATE,
    Permission.CONNECTOR_DELETE,
    Permission.QUERY_EXECUTE,
    Permission.QUERY_READ,
    Permission.DATA_WRITE,
    Permission.DATA_DELETE,
    Permission.REPORT_CREATE,
    Permission.REPORT_READ,
    Permission.USER_CREATE,
    Permission.USER_DELETE,
    Permission.AUDIT_READ,
  ],
  MEMBER: [
    Permission.CONNECTOR_READ,
    Permission.QUERY_EXECUTE,
    Permission.QUERY_READ,
    Permission.DATA_WRITE,
    Permission.REPORT_CREATE,
    Permission.REPORT_READ,
  ],
  READONLY: [
    Permission.CONNECTOR_READ,
    Permission.QUERY_EXECUTE,
    Permission.QUERY_READ,
    Permission.REPORT_READ,
  ],
};

/**
 * Check if role has permission
 */
export function hasPermission(role: Role, permission: Permission): boolean {
  const permissions = ROLE_PERMISSIONS[role] || [];
  return permissions.includes(permission);
}

/**
 * Authorize user action (throws error if unauthorized)
 */
export function authorize(role: Role, permission: Permission): void {
  if (!hasPermission(role, permission)) {
    logger.warn('Authorization failed', { role, permission });
    throw new Error(`Permission denied: ${permission}`);
  }
}
```

### Seguridad a Nivel de Fila (Middleware de Prisma)

Actualiza `packages/server/src/db/client.ts`:

```typescript
import { PrismaClient } from '@prisma/client';
import { logger } from '../utils/logger.js';

let prisma: PrismaClient;

export function getPrismaClient(): PrismaClient {
  if (!prisma) {
    prisma = new PrismaClient({
      log: [
        { level: 'query', emit: 'event' },
        { level: 'error', emit: 'event' },
      ],
    });

    // Log queries
    prisma.$on('query', (e: any) => {
      logger.debug('Prisma query', { query: e.query, duration: e.duration });
    });

    // Log errors
    prisma.$on('error', (e: any) => {
      logger.error('Prisma error', { error: e.message });
    });

    // ROW-LEVEL SECURITY MIDDLEWARE
    prisma.$use(async (params, next) => {
      // Only apply to models with organizationId
      const modelsWithOrgId = [
        'Connector',
        'Schema',
        'Query',
        'AuditLog',
        'User',
      ];

      if (modelsWithOrgId.includes(params.model || '')) {
        // For findMany, findFirst, update, delete: Add organizationId filter
        if (['findMany', 'findFirst', 'update', 'delete', 'deleteMany'].includes(params.action)) {
          // Get organizationId from context (set by middleware)
          const organizationId = (params as any).organizationId;

          if (organizationId) {
            // Add organizationId to where clause
            params.args.where = {
              ...params.args.where,
              organizationId,
            };

            logger.debug('Row-level security applied', {
              model: params.model,
              action: params.action,
              organizationId,
            });
          } else {
            logger.warn('No organizationId in context', {
              model: params.model,
              action: params.action,
            });
          }
        }
      }

      return next(params);
    });

    logger.info('Prisma client initialized with RLS middleware');
  }

  return prisma;
}

/**
 * Set organization context for row-level security
 */
export function setOrganizationContext(prisma: PrismaClient, organizationId: string) {
  (prisma as any).organizationId = organizationId;
}
```

---

## 10.3 Cifrado: AES-256 + HashiCorp Vault

**Requisitos de Cifrado:**

| Tipo de Dato | MÃ©todo de Cifrado | Almacenamiento de Clave |
|-----------|-------------------|-------------|
| **Credenciales de BD** | AES-256-GCM | HashiCorp Vault |
| **API keys** | bcrypt (hash unidireccional) | PostgreSQL |
| **Tokens OAuth** | AES-256-GCM | HashiCorp Vault |
| **Resultados de consultas** | TLS 1.3 (en trÃ¡nsito) | N/A |
| **Audit logs** | Ninguno (no sensible) | PostgreSQL |

### ImplementaciÃ³n de Cifrado AES-256

Crea `packages/server/src/crypto/encryption.ts`:

```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';
import { logger } from '../utils/logger.js';

const ALGORITHM = 'aes-256-gcm';
const KEY_LENGTH = 32; // 256 bits
const IV_LENGTH = 16; // 128 bits
const AUTH_TAG_LENGTH = 16;

/**
 * Generate encryption key (store in environment variable)
 */
export function generateEncryptionKey(): string {
  return randomBytes(KEY_LENGTH).toString('base64');
}

/**
 * Encrypt plaintext with AES-256-GCM
 */
export function encrypt(plaintext: string, key: string): string {
  try {
    const keyBuffer = Buffer.from(key, 'base64');
    const iv = randomBytes(IV_LENGTH);
    
    const cipher = createCipheriv(ALGORITHM, keyBuffer, iv);
    
    let encrypted = cipher.update(plaintext, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    
    const authTag = cipher.getAuthTag();
    
    // Format: iv:authTag:ciphertext (all base64)
    return `${iv.toString('base64')}:${authTag.toString('base64')}:${encrypted}`;
  } catch (error: any) {
    logger.error('Encryption failed', { error: error.message });
    throw new Error('Encryption failed');
  }
}

/**
 * Decrypt ciphertext with AES-256-GCM
 */
export function decrypt(ciphertext: string, key: string): string {
  try {
    const keyBuffer = Buffer.from(key, 'base64');
    const [ivBase64, authTagBase64, encryptedBase64] = ciphertext.split(':');
    
    const iv = Buffer.from(ivBase64, 'base64');
    const authTag = Buffer.from(authTagBase64, 'base64');
    const encrypted = Buffer.from(encryptedBase64, 'base64');
    
    const decipher = createDecipheriv(ALGORITHM, keyBuffer, iv);
    decipher.setAuthTag(authTag);
    
    let decrypted = decipher.update(encrypted, undefined, 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  } catch (error: any) {
    logger.error('Decryption failed', { error: error.message });
    throw new Error('Decryption failed');
  }
}
```

### IntegraciÃ³n con HashiCorp Vault

Crea `packages/server/src/crypto/vault.ts`:

```typescript
import axios from 'axios';
import { logger } from '../utils/logger.js';

const VAULT_ADDR = process.env.VAULT_ADDR || 'http://localhost:8200';
const VAULT_TOKEN = process.env.VAULT_TOKEN || 'dev-token';
const VAULT_NAMESPACE = 'databridge';

/**
 * Store secret in Vault
 */
export async function storeSecret(path: string, data: Record<string, any>): Promise<void> {
  try {
    await axios.post(
      `${VAULT_ADDR}/v1/${VAULT_NAMESPACE}/data/${path}`,
      { data },
      {
        headers: {
          'X-Vault-Token': VAULT_TOKEN,
        },
      }
    );

    logger.info('Secret stored in Vault', { path });
  } catch (error: any) {
    logger.error('Failed to store secret in Vault', {
      path,
      error: error.message,
    });
    throw new Error('Failed to store secret');
  }
}

/**
 * Retrieve secret from Vault
 */
export async function retrieveSecret(path: string): Promise<Record<string, any> | null> {
  try {
    const response = await axios.get(
      `${VAULT_ADDR}/v1/${VAULT_NAMESPACE}/data/${path}`,
      {
        headers: {
          'X-Vault-Token': VAULT_TOKEN,
        },
      }
    );

    logger.info('Secret retrieved from Vault', { path });
    return response.data.data.data;
  } catch (error: any) {
    if (error.response?.status === 404) {
      logger.warn('Secret not found in Vault', { path });
      return null;
    }

    logger.error('Failed to retrieve secret from Vault', {
      path,
      error: error.message,
    });
    throw new Error('Failed to retrieve secret');
  }
}

/**
 * Delete secret from Vault
 */
export async function deleteSecret(path: string): Promise<void> {
  try {
    await axios.delete(
      `/v1//metadata/`,
      {
        headers: {
          'X-Vault-Token': VAULT_TOKEN,
        },
      }
    );

    logger.info('Secret deleted from Vault', { path });
  } catch (error: any) {
    logger.error('Failed to delete secret from Vault', {
      path,
      error: error.message,
    });
    throw new Error('Failed to delete secret');
  }
}

/**
 * Store connector credentials in Vault
 */
export async function storeConnectorCredentials(
  connectorId: string,
  credentials: Record<string, any>
): Promise<void> {
  const path = `connectors//credentials`;
  await storeSecret(path, credentials);
}

/**
 * Retrieve connector credentials from Vault
 */
export async function retrieveConnectorCredentials(
  connectorId: string
): Promise<Record<string, any> | null> {
  const path = `connectors//credentials`;
  return retrieveSecret(path);
}
```

---

## 10.4 Limitación de Tasa

**Rate Limit por Tier:**

| Tier | Consultas por Día | Consultas por Mes | Límite Burst |
|------|------------------|-------------------|-------------|
| **FREE** | 100 | 3,000 | 10/minuto |
| **PRO** | 10,000 | 300,000 | 100/minuto |
| **ENTERPRISE** | Ilimitado | Ilimitado | 1,000/minuto |

### Implementación del Rate Limiter

Crea `packages/server/src/middleware/rate-limiter.ts`:

```typescript
import { cache } from '../utils/cache.js';
import { logger } from '../utils/logger.js';
import { Tier } from '@prisma/client';

const RATE_LIMITS: Record<Tier, { daily: number; burst: number }> = {
  FREE: { daily: 100, burst: 10 },
  PRO: { daily: 10000, burst: 100 },
  ENTERPRISE: { daily: Infinity, burst: 1000 },
};

/**
 * Check if organization has exceeded rate limit
 */
export async function checkRateLimit(
  organizationId: string,
  tier: Tier
): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
  const limits = RATE_LIMITS[tier];
  
  // Daily limit check
  const dailyKey = `rate-limit:daily:`;
  const dailyCount = (await cache.get(dailyKey)) || 0;
  
  if (dailyCount >= limits.daily) {
    logger.warn('Daily rate limit exceeded', { organizationId, tier, dailyCount });
    
    const resetAt = new Date();
    resetAt.setHours(24, 0, 0, 0); // Next midnight
    
    return { allowed: false, remaining: 0, resetAt };
  }
  
  // Burst limit check (per minute)
  const burstKey = `rate-limit:burst:`;
  const burstCount = (await cache.get(burstKey)) || 0;
  
  if (burstCount >= limits.burst) {
    logger.warn('Burst rate limit exceeded', { organizationId, tier, burstCount });
    
    const resetAt = new Date(Date.now() + 60 * 1000); // 1 minute from now
    
    return { allowed: false, remaining: 0, resetAt };
  }
  
  // Increment counters
  await cache.incr(dailyKey);
  await cache.expire(dailyKey, 86400); // 24 hours
  
  await cache.incr(burstKey);
  await cache.expire(burstKey, 60); // 1 minute
  
  const remaining = limits.daily - (dailyCount + 1);
  const resetAt = new Date();
  resetAt.setHours(24, 0, 0, 0);
  
  return { allowed: true, remaining, resetAt };
}

/**
 * Get current rate limit status
 */
export async function getRateLimitStatus(
  organizationId: string,
  tier: Tier
): Promise<{ used: number; limit: number; remaining: number; resetAt: Date }> {
  const limits = RATE_LIMITS[tier];
  const dailyKey = `rate-limit:daily:`;
  const used = (await cache.get(dailyKey)) || 0;
  
  const remaining = Math.max(0, limits.daily - used);
  const resetAt = new Date();
  resetAt.setHours(24, 0, 0, 0);
  
  return {
    used,
    limit: limits.daily,
    remaining,
    resetAt,
  };
}
```

---

## 10.5 Logging de Auditoría

Cada acción sensible se registra en la tabla `audit_logs` para cumplimiento.

### Implementación del Audit Logger

Crea `packages/server/src/audit/logger.ts`:

```typescript
import { getPrismaClient } from '../db/client.js';
import { logger } from '../utils/logger.js';

export interface AuditEvent {
  action: string;
  userId?: string;
  organizationId: string;
  resourceType: string;
  resourceId?: string;
  metadata?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
}

/**
 * Log audit event to database
 */
export async function logAudit(event: AuditEvent): Promise<void> {
  const prisma = getPrismaClient();

  try {
    await prisma.auditLog.create({
      data: {
        action: event.action,
        userId: event.userId,
        organizationId: event.organizationId,
        resourceType: event.resourceType,
        resourceId: event.resourceId,
        metadata: event.metadata || {},
        ipAddress: event.ipAddress,
        userAgent: event.userAgent,
      },
    });

    logger.info('Audit event logged', { action: event.action, resourceType: event.resourceType });
  } catch (error: any) {
    logger.error('Failed to log audit event', { error: error.message, event });
  }
}

/**
 * Audit-logged actions
 */
export enum AuditAction {
  // Authentication
  USER_LOGIN = 'USER_LOGIN',
  USER_LOGOUT = 'USER_LOGOUT',
  API_KEY_CREATED = 'API_KEY_CREATED',
  API_KEY_REVOKED = 'API_KEY_REVOKED',

  // Connectors
  CONNECTOR_CREATED = 'CONNECTOR_CREATED',
  CONNECTOR_UPDATED = 'CONNECTOR_UPDATED',
  CONNECTOR_DELETED = 'CONNECTOR_DELETED',
  CONNECTOR_CREDENTIALS_VIEWED = 'CONNECTOR_CREDENTIALS_VIEWED',

  // Queries
  QUERY_EXECUTED = 'QUERY_EXECUTED',
  QUERY_FAILED = 'QUERY_FAILED',

  // Write operations
  DATA_WRITTEN = 'DATA_WRITTEN',
  DATA_DELETED = 'DATA_DELETED',

  // Reports
  REPORT_SCHEDULED = 'REPORT_SCHEDULED',
  REPORT_CANCELED = 'REPORT_CANCELED',

  // Users
  USER_CREATED = 'USER_CREATED',
  USER_DELETED = 'USER_DELETED',
  USER_ROLE_CHANGED = 'USER_ROLE_CHANGED',
}
```

---

## 10.6 Integración con el Servidor MCP

Ahora actualiza el servidor MCP para usar autenticación y autorización.

Actualiza `packages/server/src/index.ts`:

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { logger } from './utils/logger.js';
import { registerTools } from './mcp/tools/index.js';
import { registerResources } from './mcp/resources/index.js';
import { registerPrompts } from './mcp/prompts/index.js';
import { authenticate } from './auth/middleware.js';
import { checkRateLimit } from './middleware/rate-limiter.js';

const server = new Server(
  {
    name: 'databridge-mcp',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// ============================================================
// AUTHENTICATION MIDDLEWARE
// ============================================================

server.setRequestHandler('*', async (request, extra) => {
  // Extract headers from request (MCP protocol doesn't have standard headers)
  // For now, we'll use a custom metadata field
  const headers = (request as any).params?.metadata?.headers || {};

  // Authenticate
  const authContext = await authenticate(headers);
  if (!authContext) {
    throw new Error('Authentication required');
  }

  // Rate limiting
  const rateLimit = await checkRateLimit(authContext.organizationId, authContext.tier as any);
  if (!rateLimit.allowed) {
    throw new Error(
      `Rate limit exceeded. Reset at `
    );
  }

  // Attach auth context to request
  (request as any).authContext = authContext;

  logger.debug('Request authenticated', {
    organizationId: authContext.organizationId,
    method: authContext.method,
    remaining: rateLimit.remaining,
  });

  // Continue to handler
  return extra.next(request);
});

// Register handlers
registerTools(server);
registerResources(server);
registerPrompts(server);

// Error handling
server.onerror = (error) => {
  logger.error('MCP Server error', { error: error.message, stack: error.stack });
};

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  logger.info('DataBridge MCP Server running on stdio with authentication');
}

main().catch((error) => {
  logger.error('Failed to start server', { error });
  process.exit(1);
});
```

---

## 10.7 Pruebas de Seguridad

### Prueba 1: Autenticación con API Key

```powershell
# Generate API key
npm run cli -- generate-api-key --organization clq1...

# Output: db_a1b2c3d4e5f6...
```

Prueba con MCP Inspector:

```json
{
  "metadata": {
    "headers": {
      "x-api-key": "db_a1b2c3d4e5f6..."
    }
  },
  "query": "show me all customers",
  "connectorId": "clq2..."
}
```

### Prueba 2: Limitación de Tasa

```powershell
# Make 101 requests (exceeds FREE tier daily limit of 100)
for ($i = 0; $i -lt 101; $i++) {
  # Call query_unified_data tool
}

# Expected error on 101st request:
# "Rate limit exceeded. Reset at 2025-01-16T00:00:00Z"
```

### Prueba 3: Seguridad a Nivel de Fila

```sql
-- User from Org A tries to access Org B's data
-- Should return empty result (not error)

SELECT * FROM connectors WHERE id = 'org-b-connector-id';
-- Result: []
```

### Prueba 4: Cifrado

```typescript
import { encrypt, decrypt } from './src/crypto/encryption.js';

const key = generateEncryptionKey();
const plaintext = 'postgresql://user:password@localhost:5432/db';

const encrypted = encrypt(plaintext, key);
console.log('Encrypted:', encrypted);
// Output: iv:authTag:ciphertext

const decrypted = decrypt(encrypted, key);
console.log('Decrypted:', decrypted);
// Output: postgresql://user:password@localhost:5432/db
```

---

## 10.8 Checklist de Seguridad

Antes de desplegar a producción, verifica:

**Autenticación:**
-  API keys con hash bcrypt (no texto plano)
-  JWT secret es fuerte (128+ bits de entropía)
-  Tokens expiran después de 24 horas
-  Refresh tokens rotados en uso

**Autorización:**
-  RBAC aplicado en todas las herramientas
-  Seguridad a nivel de fila aplicada a todas las consultas
-  Usuarios no pueden acceder datos de otras organizaciones

**Cifrado:**
-  Credenciales de BD almacenadas en Vault
-  Tokens OAuth cifrados con AES-256
-  TLS 1.3 para toda comunicación de red
-  Claves de cifrado rotadas trimestralmente

**Limitación de Tasa:**
-  Límites por tier aplicados
-  Protección burst (por minuto)
-  Headers de rate limit retornados en respuestas

**Logging de Auditoría:**
-  Todas las acciones sensibles registradas
-  Logs incluyen usuario, timestamp, IP, acción
-  Logs retenidos por 90 días (cumplimiento)
-  Logs inmutables (append-only)

**Gestión de Secretos:**
-  Sin secretos en código o variables de entorno
-  Vault desbloqueado y accesible
-  Token de Vault rotado mensualmente
-  Secretos respaldados de forma segura

---

## 10.9 Resumen

En este capítulo, implementaste **seguridad de nivel empresarial** para DataBridge:

**Autenticación (2 métodos):**
-  API Keys (hash bcrypt, revocables)
-  OAuth 2.0 (tokens JWT, expiran en 24h)

**Autorización:**
-  RBAC (roles ADMIN/MEMBER/READONLY)
-  Seguridad a Nivel de Fila (middleware Prisma)
-  Verificación de permisos en todas las herramientas

**Cifrado:**
-  AES-256-GCM para credenciales
-  HashiCorp Vault para secretos
-  TLS 1.3 para tráfico de red

**Limitación de Tasa:**
-  Cuotas por tier (FREE: 100/día, PRO: 10K/día)
-  Protección burst (10-1000/min)
-  Contadores respaldados por Redis

**Logging de Auditoría:**
-  Cada acción registrada en base de datos
-  Usuario, timestamp, IP, recurso rastreados
-  Listo para cumplimiento (SOC 2, GDPR, HIPAA)

**Cumplimiento:**
-  Listo para SOC 2 Type II
-  Cumple con GDPR (cifrado + audit logs)
-  Cumple con HIPAA (cifrado PHI)
-  Cumple con PCI DSS (cifrado datos tarjetas)

---

## Ejercicios

### Ejercicio 1: Implementar OAuth 2.0 con Google
**Tarea:** Agregar integración OAuth de Google (flujo authorization code).

**Requisitos:**
- Registrar app en Google Cloud Console
- Implementar flujo de redirección OAuth
- Almacenar access + refresh tokens en Vault
- Intercambiar refresh token cuando access token expire

**Entregable:** `packages/server/src/auth/oauth-google.ts`

### Ejercicio 2: Agregar 2FA (Autenticación de Dos Factores)
**Tarea:** Requerir TOTP (Time-based One-Time Password) para usuarios ADMIN.

**Requisitos:**
- Usar paquete npm `speakeasy`
- Generar código QR para setup
- Validar TOTP en login
- Almacenar secret en Vault

**Entregable:** `packages/server/src/auth/totp.ts`

### Ejercicio 3: Implementar IP Allowlisting
**Tarea:** Permitir a organizaciones restringir acceso a rangos IP específicos.

**Requisitos:**
- Agregar campo `allowedIps` al modelo Organization (array de rangos CIDR)
- Validar IP en middleware de autenticación
- Retornar 403 si IP no está en allowlist

**Entregable:** Modificar `packages/server/src/auth/middleware.ts`

### Ejercicio 4: Agregar Seguridad de Webhooks (Firmas HMAC)
**Tarea:** Firmar payloads de webhooks con HMAC-SHA256.

**Requisitos:**
- Generar webhook secret para cada organización
- Firmar payload: `HMAC-SHA256(secret, payload)`
- Incluir firma en header `X-DataBridge-Signature`
- Receptor valida firma

**Entregable:** `packages/server/src/webhooks/signer.ts`

### Ejercicio 5: Implementar Gestión de Sesiones
**Tarea:** Rastrear sesiones activas y permitir a usuarios revocarlas.

**Requisitos:**
- Almacenar sesiones en Redis (sessionId  userId, expiresAt)
- Agregar recurso `sessions`: `databridge://sessions`
- Agregar herramienta `revoke_session`
- Expirar sesiones después de 24h de inactividad

**Entregable:** `packages/server/src/auth/session.ts`

---

## Qué Sigue

En **Capítulo 11**, implementaremos **Deployment & Monitoring**:

**Temas:**
- Docker multi-stage builds (imágenes optimizadas)
- Despliegue en AWS ECS (Fargate + ALB)
- Integración Datadog (métricas, logs, traces)
- Alertas (PagerDuty, Slack)
- Health checks (probes readiness, liveness)
- Despliegues blue-green (zero-downtime)
- Migraciones de base de datos en producción
- Backup & disaster recovery (RTO: 4h, RPO: 1h)

Vamos a desplegar DataBridge a producción! 
