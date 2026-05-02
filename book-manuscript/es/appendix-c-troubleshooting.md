# Apéndice C: Guía de Troubleshooting

Este apéndice proporciona soluciones a problemas comunes encontrados al construir y deployar servidores MCP.

## Issues Generales

### Servidor No Inicia

**Síntoma:** El servidor sale inmediatamente o no inicia.

**Pasos de Diagnóstico:**

1. **Verificar variables de entorno:**
```powershell
# Verificar que todas las variables requeridas estén configuradas
$env:DATABASE_URL
$env:REDIS_URL
$env:PORT
```

2. **Probar conexión de base de datos:**
```powershell
# PostgreSQL
psql $env:DATABASE_URL

# Probar conectividad
pg_isready -d $env:DATABASE_URL
```

3. **Revisar logs:**
```powershell
# TypeScript (DataBridge)
npm start 2>&1 | Tee-Object -FilePath error.log

# Rust (MarketPulse)
RUST_LOG=debug ./target/release/marketpulse 2>&1 | Tee-Object -FilePath error.log
```

**Soluciones Comunes:**

| Problema | Solución |
|---------|----------|
| Variable de entorno faltante | Agregar a archivo `.env` o entorno del sistema |
| Base de datos inaccesible | Verificar host, puerto, reglas de firewall |
| Puerto ya en uso | Cambiar variable PORT o matar proceso |
| Permiso denegado | Ejecutar con privilegios de usuario apropiados |

### Cliente MCP No Puede Conectar

**Síntoma:** Claude Desktop u otro cliente reporta error de conexión.

**Pasos de Diagnóstico:**

1. **Verificar configuración:**
```json
{
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["C:\\full\\path\\to\\server\\dist\\index.js"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

2. **Probar comunicación stdio:**
```powershell
# Enviar request de initialize manualmente
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' | node dist/index.js
```

3. **Verificar separadores de path:**
```json
// ❌ Incorrecto (en Windows)
"command": "path/to/server"

// ✅ Correcto (en Windows)
"command": "path\\to\\server"
// o
"command": "C:/path/to/server"
```

**Soluciones Comunes:**

| Problema | Solución |
|---------|----------|
| Paths relativos | Usar paths absolutos en config |
| Comando incorrecto | Verificar path de `node`, `python`, o ejecutable |
| Error de sintaxis JSON | Validar JSON con linter |
| Desajuste de protocolo | Actualizar cliente o servidor para match de versión |

### Rendimiento Lento

**Síntoma:** El servidor tarda demasiado en responder.

**Pasos de Diagnóstico:**

1. **Habilitar logging de rendimiento:**
```typescript
// DataBridge
const startTime = Date.now();
const result = await executeQuery(query);
console.log(`Query took ${Date.now() - startTime}ms`);
```

```rust
// MarketPulse
use std::time::Instant;
let start = Instant::now();
let result = get_ohlcv(symbol, interval).await;
println!("Query took {:?}", start.elapsed());
```

2. **Verificar query plans de base de datos:**
```sql
EXPLAIN ANALYZE SELECT * FROM large_table WHERE condition;
```

3. **Monitorear connection pool:**
```typescript
console.log(`Pool: ${pool.totalCount} total, ${pool.idleCount} idle`);
```

**Soluciones Comunes:**

| Problema | Solución |
|---------|----------|
| Índices faltantes | Agregar índices a columnas consultadas frecuentemente |
| Sin connection pooling | Implementar connection pooling (r2d2, pg.Pool) |
| Result sets grandes | Agregar cláusulas LIMIT, implementar paginación |
| Sin caching | Agregar capa de caching Redis |
| Red lenta | Optimizar consultas, reducir transferencia de datos |

## Issues Específicos de DataBridge

### Errores de Conexión de Base de Datos

#### Error: "ECONNREFUSED"

**Causa:** Servidor de base de datos no ejecutándose o inaccesible.

**Soluciones:**
```powershell
# 1. Verificar si PostgreSQL está ejecutándose
Get-Service postgresql*

# 2. Iniciar PostgreSQL
net start postgresql-x64-16

# 3. Probar conexión
psql -h localhost -U postgres -d databridge

# 4. Verificar firewall
Test-NetConnection -ComputerName localhost -Port 5432
```

#### Error: "password authentication failed"

**Causa:** Credenciales incorrectas.

**Soluciones:**
```powershell
# 1. Verificar credenciales en .env
DATABASE_URL=postgresql://correct_user:correct_password@localhost:5432/databridge

# 2. Resetear password (como usuario postgres)
psql -U postgres
ALTER USER myuser WITH PASSWORD 'newpassword';

# 3. Verificar método de autenticación en pg_hba.conf
# Debe tener: host all all 127.0.0.1/32 md5
```

#### Error: "too many clients"

**Causa:** Connection pool agotado.

**Soluciones:**
```typescript
// 1. Reducir tamaño de pool
const pool = new Pool({
  max: 10, // Reducir de 20
  min: 2,
  idleTimeoutMillis: 30000
});

// 2. Incrementar max_connections de PostgreSQL
// En postgresql.conf:
max_connections = 100

// 3. Siempre liberar conexiones
try {
  const client = await pool.connect();
  // ... usar client
} finally {
  client.release(); // ¡Crítico!
}
```

### Issues de Conexión Redis

#### Error: "Redis connection refused"

**Soluciones:**
```powershell
# 1. Iniciar Redis
redis-server

# O con config personalizada
redis-server C:\path\to\redis.conf

# 2. Probar conexión
redis-cli ping
# Debe retornar: PONG

# 3. Verificar URL de Redis
REDIS_URL=redis://localhost:6379
# O con password
REDIS_URL=redis://:password@localhost:6379
```

#### Error: "Redis command timeout"

**Soluciones:**
```typescript
// 1. Incrementar timeout
const redis = new Redis({
  host: 'localhost',
  port: 6379,
  connectTimeout: 10000, // 10 segundos
  commandTimeout: 5000
});

// 2. Verificar memoria de Redis
// En redis-cli:
INFO memory

// 3. Establecer política de eviction
// En redis.conf:
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Issues de OAuth 2.0

#### Error: "Invalid client credentials"

**Soluciones:**
```typescript
// 1. Verificar config OAuth
const oauthConfig = {
  clientId: process.env.OAUTH_CLIENT_ID,
  clientSecret: process.env.OAUTH_CLIENT_SECRET,
  redirectUri: 'http://localhost:3000/callback'
};

console.log('Client ID:', oauthConfig.clientId);
// ¡No loggear secret en producción!

// 2. Verificar que redirect URI coincida exactamente
// Config del proveedor: http://localhost:3000/callback
// Tu config: http://localhost:3000/callback
// ❌ No agregar trailing slash si el proveedor no lo tiene

// 3. Verificar scopes
const scopes = ['read:user', 'read:data'];
```

#### Error: "Token expired"

**Soluciones:**
```typescript
// 1. Implementar refresh de token
async function refreshAccessToken(refreshToken: string) {
  const response = await fetch('https://oauth-provider.com/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: process.env.OAUTH_CLIENT_ID!,
      client_secret: process.env.OAUTH_CLIENT_SECRET!
    })
  });
  return await response.json();
}

// 2. Auto-refresh antes de expirar
const expiresAt = token.expires_at;
const now = Date.now();
if (now >= expiresAt - 60000) { // Refresh 1 min antes de expirar
  token = await refreshAccessToken(token.refresh_token);
}
```

### Issues de Ejecución de Queries

#### Error: "Query timeout"

**Soluciones:**
```typescript
// 1. Establecer statement timeout
await client.query('SET statement_timeout = 30000'); // 30 segundos

// 2. Agregar timeout a config de pool
const pool = new Pool({
  statement_timeout: 30000
});

// 3. Optimizar queries lentas
// Agregar índices
CREATE INDEX idx_users_email ON users(email);

// Usar EXPLAIN para analizar
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

#### Error: "Column does not exist"

**Soluciones:**
```typescript
// 1. Verificar que schema coincida con query
const result = await client.query(`
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'users'
`);
console.log('Available columns:', result.rows);

// 2. Usar identificadores entrecomillados para columnas case-sensitive
SELECT "firstName" FROM users; // No firstname

// 3. Verificar que tabla existe
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

## Issues Específicos de MarketPulse

### Issues de Conexión WebSocket

#### Error: "WebSocket connection failed"

**Soluciones:**
```rust
// 1. Probar URL de WebSocket
use tokio_tungstenite::connect_async;

let url = "wss://stream.binance.com:9443/ws/btcusdt@trade";
match connect_async(url).await {
    Ok((ws, _)) => println!("Connected"),
    Err(e) => eprintln!("Failed: {}", e)
}

// 2. Verificar certificados TLS
// Agregar a Cargo.toml:
[dependencies]
native-tls = "0.2"
tokio-tungstenite = { version = "0.21", features = ["native-tls"] }

// 3. Implementar lógica de reconexión
async fn connect_with_retry(url: &str, max_retries: u32) -> Result<WebSocket> {
    for attempt in 1..=max_retries {
        match connect_async(url).await {
            Ok((ws, _)) => return Ok(ws),
            Err(e) => {
                eprintln!("Attempt {}: {}", attempt, e);
                tokio::time::sleep(Duration::from_secs(2_u64.pow(attempt))).await;
            }
        }
    }
    Err(anyhow!("Max retries exceeded"))
}
```

#### Error: "WebSocket ping timeout"

**Soluciones:**
```rust
// 1. Implementar ping/pong
use tokio::time::{interval, Duration};

let mut ping_interval = interval(Duration::from_secs(30));

loop {
    tokio::select! {
        _ = ping_interval.tick() => {
            ws.send(Message::Ping(vec![])).await?;
        }
        msg = ws.next() => {
            match msg {
                Some(Ok(Message::Pong(_))) => {
                    // Conexión viva
                }
                // ... manejar otros mensajes
            }
        }
    }
}

// 2. Establecer timeout de WebSocket
use tokio::time::timeout;

let result = timeout(
    Duration::from_secs(60),
    ws.next()
).await;

match result {
    Ok(Some(Ok(msg))) => { /* procesar */ },
    Ok(None) => { /* conexión cerrada */ },
    Err(_) => { /* timeout */ }
}
```

### Issues de Base de Datos (TimescaleDB)

#### Error: "Extension timescaledb not found"

**Soluciones:**
```sql
-- 1. Instalar extensión TimescaleDB
-- Windows: Descargar de https://www.timescale.com/
-- Linux: apt-get install timescaledb-postgresql-16

-- 2. Habilitar extensión
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 3. Verificar instalación
SELECT * FROM pg_extension WHERE extname = 'timescaledb';

-- 4. Verificar versión
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

#### Error: "Hypertable already exists"

**Soluciones:**
```sql
-- 1. Verificar si hypertable existe
SELECT * FROM timescaledb_information.hypertables
WHERE hypertable_name = 'ohlcv';

-- 2. Eliminar y recrear
DROP TABLE IF EXISTS ohlcv CASCADE;
CREATE TABLE ohlcv (
    timestamp TIMESTAMPTZ NOT NULL,
    symbol_id INTEGER NOT NULL,
    -- ... otras columnas
);
SELECT create_hypertable('ohlcv', 'timestamp');

-- 3. O saltar si existe
SELECT create_hypertable('ohlcv', 'timestamp', if_not_exists => TRUE);
```

#### Error: "Chunk size too small"

**Soluciones:**
```sql
-- 1. Establecer intervalo de chunk apropiado
SELECT create_hypertable(
    'ohlcv',
    'timestamp',
    chunk_time_interval => INTERVAL '1 week'
);

-- 2. Modificar hypertable existente
SELECT set_chunk_time_interval('ohlcv', INTERVAL '1 week');

-- 3. Verificar chunks actuales
SELECT * FROM timescaledb_information.chunks
WHERE hypertable_name = 'ohlcv'
ORDER BY range_start DESC;
```

### Issues de Diesel ORM

#### Error: "diesel.toml not found"

**Soluciones:**
```powershell
# 1. Inicializar Diesel
diesel setup

# 2. Crear diesel.toml manualmente
echo "[print_schema]" > diesel.toml
echo "file = `"src/schema.rs`"" >> diesel.toml
echo "custom_type_derives = [`"diesel::query_builder::QueryId`"]" >> diesel.toml

# 3. Verificar DATABASE_URL
echo $env:DATABASE_URL
```

#### Error: "Migration failed"

**Soluciones:**
```powershell
# 1. Verificar estado de migración
diesel migration list

# 2. Revertir última migración
diesel migration revert

# 3. Rehacer migración
diesel migration redo

# 4. Arreglar SQL de migración
# Editar migrations/TIMESTAMP_name/up.sql
# Arreglar errores de sintaxis, luego:
diesel migration run

# 5. Resetear base de datos (¡destructivo!)
diesel database reset
```

#### Error: "Table not found in schema.rs"

**Soluciones:**
```rust
// 1. Regenerar schema
// En terminal:
diesel print-schema > src/schema.rs

// 2. Verificar declaración de tabla
// src/schema.rs debe tener:
table! {
    ohlcv (timestamp, symbol_id) {
        timestamp -> Timestamptz,
        symbol_id -> Int4,
        open -> Float8,
        // ...
    }
}

// 3. Importar schema en tu código
mod schema;
use schema::ohlcv;
```

### Issues de Cálculo de Indicadores Técnicos

#### Error: "Insufficient data for indicator"

**Soluciones:**
```rust
// 1. Verificar longitud de datos antes de calcular
pub fn calculate_rsi(prices: &[f64], period: usize) -> Result<f64> {
    if prices.len() < period + 1 {
        return Err(anyhow!(
            "Need {} prices, got {}",
            period + 1,
            prices.len()
        ));
    }
    // ... cálculo
}

// 2. Obtener suficientes datos históricos
let limit = period + 50; // Buffer extra
let ohlcv = get_ohlcv(symbol, interval, limit).await?;

// 3. Manejar gracefully
match calculate_rsi(&prices, 14) {
    Ok(rsi) => println!("RSI: {}", rsi),
    Err(e) => println!("Cannot calculate: {}", e)
}
```

#### Error: "NaN result in calculation"

**Soluciones:**
```rust
// 1. Verificar división por cero
let average = if count > 0 {
    sum / count as f64
} else {
    0.0
};

// 2. Manejar infinito
if result.is_infinite() || result.is_nan() {
    return Err(anyhow!("Invalid calculation result"));
}

// 3. Validar datos de input
for price in prices {
    if *price <= 0.0 || price.is_nan() || price.is_infinite() {
        return Err(anyhow!("Invalid price data: {}", price));
    }
}

// 4. Usar f64::max para comparaciones
let max_price = prices.iter()
    .copied()
    .fold(f64::NEG_INFINITY, f64::max);
```

## Issues de Deployment

### Issues de Docker

#### Error: "Cannot connect to Docker daemon"

**Soluciones:**
```powershell
# 1. Iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# 2. Verificar estado de Docker
docker info

# 3. Reiniciar servicio Docker
Restart-Service docker

# 4. Verificar si ejecuta en modo admin
# Ejecutar PowerShell como Administrador
```

#### Error: "Build failed: COPY failed"

**Soluciones:**
```dockerfile
# 1. Verificar que archivo existe y path es correcto
COPY package.json ./
# No: COPY src/package.json ./ (si package.json está en root)

# 2. Verificar .dockerignore
# Asegurar que archivos requeridos no están ignorados
# .dockerignore:
node_modules
dist
# No ignorar: package.json, src/, etc.

# 3. Usar contexto correcto
docker build -t myapp -f Dockerfile .
#                                   ^ contexto

# 4. Verificar separadores de path de Windows
COPY package.json ./
# No: COPY package.json .\ (backslash)
```

#### Error: "Image size too large"

**Soluciones:**
```dockerfile
# 1. Usar multi-stage builds
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
CMD ["node", "dist/index.js"]

# 2. Usar imágenes base alpine
FROM node:18-alpine  # Mucho más pequeña que node:18

# 3. Limpiar en la misma capa
RUN apt-get update && \
    apt-get install -y build-essential && \
    npm install && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 4. Verificar tamaño de imagen
docker images | grep myapp
```

### Issues de AWS ECS

#### Error: "Task failed to start"

**Soluciones:**
```powershell
# 1. Verificar logs de CloudWatch
aws logs tail /ecs/myapp --follow

# 2. Verificar definición de task
aws ecs describe-task-definition --task-definition myapp:1

# 3. Verificar variables de entorno
# En definición de task:
{
  "environment": [
    {"name": "DATABASE_URL", "value": "..."},
    {"name": "REDIS_URL", "value": "..."}
  ]
}

# 4. Verificar permisos IAM
# Task execution role necesita:
# - ecr:GetAuthorizationToken
# - ecr:BatchCheckLayerAvailability
# - logs:CreateLogStream
# - logs:PutLogEvents
```

#### Error: "Service unable to place task"

**Soluciones:**
```powershell
# 1. Verificar capacidad
aws ecs describe-clusters --clusters my-cluster

# 2. Verificar subnet y security groups
# Asegurar:
# - Subnets tienen IPs disponibles
# - Security groups permiten puertos requeridos
# - NAT Gateway configurado para subnets privadas

# 3. Verificar límites de servicio
aws service-quotas get-service-quota \
  --service-code ecs \
  --quota-code L-3032A538

# 4. Revisar eventos
aws ecs describe-services \
  --cluster my-cluster \
  --services myapp \
  --query 'services[0].events[0:5]'
```

### Issues de GitHub Actions

#### Error: "Workflow not triggered"

**Soluciones:**
```yaml
# 1. Verificar condiciones de trigger
on:
  push:
    branches: [main]  # Asegurar push a branch correcto
  pull_request:
    branches: [main]

# 2. Verificar ubicación .github/workflows
# Debe ser: .github/workflows/ci.yml
# No: github/workflows/ci.yml

# 3. Verificar sintaxis YAML
# Usar validador YAML online

# 4. Verificar permisos de workflow
# Settings > Actions > General > Workflow permissions
```

#### Error: "Step failed: Docker build"

**Soluciones:**
```yaml
# 1. Agregar debugging
- name: Debug
  run: |
    pwd
    ls -la
    cat Dockerfile

# 2. Verificar secrets
- name: Build
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    echo "DATABASE_URL length: ${#DATABASE_URL}"
    # ¡No hacer echo del secret real!

# 3. Usar paths explícitos
- name: Build Docker image
  run: docker build -t myapp:${{ github.sha }} -f ./Dockerfile .
  working-directory: ./

# 4. Verificar límites de rate de Docker Hub
# Usar pulls autenticados
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

## Issues de Testing

### Fallos de Tests de Integración

#### Error: "Database not ready for tests"

**Soluciones:**
```typescript
// 1. Esperar por base de datos
async function waitForDatabase(maxRetries = 10) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await pool.query('SELECT 1');
      return;
    } catch (e) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  throw new Error('Database not ready');
}

beforeAll(async () => {
  await waitForDatabase();
  await runMigrations();
});

// 2. Usar test containers
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container: PostgreSqlContainer;

beforeAll(async () => {
  container = await new PostgreSqlContainer().start();
  process.env.DATABASE_URL = container.getConnectionUri();
});

afterAll(async () => {
  await container.stop();
});
```

#### Error: "Test data conflicts"

**Soluciones:**
```typescript
// 1. Limpiar datos antes de cada test
beforeEach(async () => {
  await client.query('TRUNCATE TABLE users CASCADE');
  await client.query('TRUNCATE TABLE orders CASCADE');
});

// 2. Usar transacciones (más rápido)
let client: PoolClient;

beforeEach(async () => {
  client = await pool.connect();
  await client.query('BEGIN');
});

afterEach(async () => {
  await client.query('ROLLBACK');
  client.release();
});

// 3. Usar datos de test únicos
const testUser = {
  email: `test-${Date.now()}@example.com`,
  name: 'Test User'
};
```

## Tips de Debugging

### Habilitar Logging Verbose

**TypeScript:**
```typescript
// Establecer variable de entorno
process.env.LOG_LEVEL = 'debug';

// O usar paquete debug
import debug from 'debug';
const log = debug('myapp:server');
log('Server starting...');
```

**Rust:**
```rust
// Establecer variable de entorno RUST_LOG
// RUST_LOG=debug cargo run

use env_logger;
env_logger::init();

log::debug!("Server starting...");
log::info!("Connected to database");
log::error!("Failed to connect: {}", err);
```

### Usar Inspección de Red

```powershell
# Monitorear conexiones WebSocket
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.Options.SetRequestHeader("User-Agent", "Test")
# ... conectar e inspeccionar

# Probar conexiones TCP
Test-NetConnection -ComputerName stream.binance.com -Port 9443

# Verificar resolución DNS
Resolve-DnsName stream.binance.com
```

### Perfilar Rendimiento

**TypeScript:**
```typescript
// Usar profiler de Node.js
node --prof dist/index.js
node --prof-process isolate-*.log > profile.txt

// O usar clinic.js
npm install -g clinic
clinic doctor -- node dist/index.js
```

**Rust:**
```rust
// Usar flamegraph
cargo install flamegraph
cargo flamegraph

// O perf (Linux)
perf record -F 99 -g ./target/release/marketpulse
perf script > out.perf
```

---

Para soporte adicional:
- DataBridge GitHub Issues: https://github.com/yourorg/databridge/issues
- MarketPulse GitHub Issues: https://github.com/yourorg/marketpulse/issues
- MCP Documentation: https://modelcontextprotocol.io/

*Última actualización: Noviembre 2024*
