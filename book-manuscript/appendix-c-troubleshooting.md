# Appendix C: Troubleshooting Guide

This appendix provides solutions to common problems encountered when building and deploying MCP servers.

## General Issues

### Server Not Starting

**Symptom:** Server exits immediately or won't start.

**Diagnostic Steps:**

1. **Check environment variables:**
```powershell
# Verify all required variables are set
$env:DATABASE_URL
$env:REDIS_URL
$env:PORT
```

2. **Test database connection:**
```powershell
# PostgreSQL
psql $env:DATABASE_URL

# Test connectivity
pg_isready -d $env:DATABASE_URL
```

3. **Check logs:**
```powershell
# TypeScript (DataBridge)
npm start 2>&1 | Tee-Object -FilePath error.log

# Rust (MarketPulse)
RUST_LOG=debug ./target/release/marketpulse 2>&1 | Tee-Object -FilePath error.log
```

**Common Solutions:**

| Problem | Solution |
|---------|----------|
| Missing env var | Add to `.env` file or system environment |
| Database unreachable | Check host, port, firewall rules |
| Port already in use | Change PORT env var or kill process |
| Permission denied | Run with appropriate user privileges |

### MCP Client Can't Connect

**Symptom:** Claude Desktop or other client reports connection error.

**Diagnostic Steps:**

1. **Verify configuration:**
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

2. **Test stdio communication:**
```powershell
# Send initialize request manually
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' | node dist/index.js
```

3. **Check path separators:**
```json
// ❌ Wrong (on Windows)
"command": "path/to/server"

// ✅ Correct (on Windows)
"command": "path\\to\\server"
// or
"command": "C:/path/to/server"
```

**Common Solutions:**

| Problem | Solution |
|---------|----------|
| Relative paths | Use absolute paths in config |
| Wrong command | Verify `node`, `python`, or executable path |
| JSON syntax error | Validate JSON with linter |
| Protocol mismatch | Update client or server to match version |

### Slow Performance

**Symptom:** Server takes too long to respond.

**Diagnostic Steps:**

1. **Enable performance logging:**
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

2. **Check database query plans:**
```sql
EXPLAIN ANALYZE SELECT * FROM large_table WHERE condition;
```

3. **Monitor connection pool:**
```typescript
console.log(`Pool: ${pool.totalCount} total, ${pool.idleCount} idle`);
```

**Common Solutions:**

| Problem | Solution |
|---------|----------|
| Missing indexes | Add indexes to frequently queried columns |
| No connection pooling | Implement connection pooling (r2d2, pg.Pool) |
| Large result sets | Add LIMIT clauses, implement pagination |
| No caching | Add Redis caching layer |
| Slow network | Optimize queries, reduce data transfer |

## DataBridge-Specific Issues

### Database Connection Errors

#### Error: "ECONNREFUSED"

**Cause:** Database server not running or unreachable.

**Solutions:**
```powershell
# 1. Check if PostgreSQL is running
Get-Service postgresql*

# 2. Start PostgreSQL
net start postgresql-x64-16

# 3. Test connection
psql -h localhost -U postgres -d databridge

# 4. Check firewall
Test-NetConnection -ComputerName localhost -Port 5432
```

#### Error: "password authentication failed"

**Cause:** Incorrect credentials.

**Solutions:**
```powershell
# 1. Verify credentials in .env
DATABASE_URL=postgresql://correct_user:correct_password@localhost:5432/databridge

# 2. Reset password (as postgres user)
psql -U postgres
ALTER USER myuser WITH PASSWORD 'newpassword';

# 3. Check pg_hba.conf authentication method
# Should have: host all all 127.0.0.1/32 md5
```

#### Error: "too many clients"

**Cause:** Connection pool exhausted.

**Solutions:**
```typescript
// 1. Reduce pool size
const pool = new Pool({
  max: 10, // Reduce from 20
  min: 2,
  idleTimeoutMillis: 30000
});

// 2. Increase PostgreSQL max_connections
// In postgresql.conf:
max_connections = 100

// 3. Always release connections
try {
  const client = await pool.connect();
  // ... use client
} finally {
  client.release(); // Critical!
}
```

### Redis Connection Issues

#### Error: "Redis connection refused"

**Solutions:**
```powershell
# 1. Start Redis
redis-server

# Or with custom config
redis-server C:\path\to\redis.conf

# 2. Test connection
redis-cli ping
# Should return: PONG

# 3. Check Redis URL
REDIS_URL=redis://localhost:6379
# Or with password
REDIS_URL=redis://:password@localhost:6379
```

#### Error: "Redis command timeout"

**Solutions:**
```typescript
// 1. Increase timeout
const redis = new Redis({
  host: 'localhost',
  port: 6379,
  connectTimeout: 10000, // 10 seconds
  commandTimeout: 5000
});

// 2. Check Redis memory
// In redis-cli:
INFO memory

// 3. Set eviction policy
// In redis.conf:
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### OAuth 2.0 Issues

#### Error: "Invalid client credentials"

**Solutions:**
```typescript
// 1. Verify OAuth config
const oauthConfig = {
  clientId: process.env.OAUTH_CLIENT_ID,
  clientSecret: process.env.OAUTH_CLIENT_SECRET,
  redirectUri: 'http://localhost:3000/callback'
};

console.log('Client ID:', oauthConfig.clientId);
// Don't log secret in production!

// 2. Check redirect URI matches exactly
// Provider config: http://localhost:3000/callback
// Your config: http://localhost:3000/callback
// ❌ Don't add trailing slash if provider doesn't have it

// 3. Verify scopes
const scopes = ['read:user', 'read:data'];
```

#### Error: "Token expired"

**Solutions:**
```typescript
// 1. Implement token refresh
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

// 2. Auto-refresh before expiry
const expiresAt = token.expires_at;
const now = Date.now();
if (now >= expiresAt - 60000) { // Refresh 1 min before expiry
  token = await refreshAccessToken(token.refresh_token);
}
```

### Query Execution Issues

#### Error: "Query timeout"

**Solutions:**
```typescript
// 1. Set statement timeout
await client.query('SET statement_timeout = 30000'); // 30 seconds

// 2. Add timeout to pool config
const pool = new Pool({
  statement_timeout: 30000
});

// 3. Optimize slow queries
// Add indexes
CREATE INDEX idx_users_email ON users(email);

// Use EXPLAIN to analyze
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

#### Error: "Column does not exist"

**Solutions:**
```typescript
// 1. Check schema matches query
const result = await client.query(`
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'users'
`);
console.log('Available columns:', result.rows);

// 2. Use quoted identifiers for case-sensitive columns
SELECT "firstName" FROM users; // Not firstname

// 3. Check table exists
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

## MarketPulse-Specific Issues

### WebSocket Connection Issues

#### Error: "WebSocket connection failed"

**Solutions:**
```rust
// 1. Test WebSocket URL
use tokio_tungstenite::connect_async;

let url = "wss://stream.binance.com:9443/ws/btcusdt@trade";
match connect_async(url).await {
    Ok((ws, _)) => println!("Connected"),
    Err(e) => eprintln!("Failed: {}", e)
}

// 2. Check TLS certificates
// Add to Cargo.toml:
[dependencies]
native-tls = "0.2"
tokio-tungstenite = { version = "0.21", features = ["native-tls"] }

// 3. Implement reconnection logic
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

**Solutions:**
```rust
// 1. Implement ping/pong
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
                    // Connection alive
                }
                // ... handle other messages
            }
        }
    }
}

// 2. Set WebSocket timeout
use tokio::time::timeout;

let result = timeout(
    Duration::from_secs(60),
    ws.next()
).await;

match result {
    Ok(Some(Ok(msg))) => { /* process */ },
    Ok(None) => { /* connection closed */ },
    Err(_) => { /* timeout */ }
}
```

### Database Issues (TimescaleDB)

#### Error: "Extension timescaledb not found"

**Solutions:**
```sql
-- 1. Install TimescaleDB extension
-- Windows: Download from https://www.timescale.com/
-- Linux: apt-get install timescaledb-postgresql-16

-- 2. Enable extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 3. Verify installation
SELECT * FROM pg_extension WHERE extname = 'timescaledb';

-- 4. Check version
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

#### Error: "Hypertable already exists"

**Solutions:**
```sql
-- 1. Check if hypertable exists
SELECT * FROM timescaledb_information.hypertables
WHERE hypertable_name = 'ohlcv';

-- 2. Drop and recreate
DROP TABLE IF EXISTS ohlcv CASCADE;
CREATE TABLE ohlcv (
    timestamp TIMESTAMPTZ NOT NULL,
    symbol_id INTEGER NOT NULL,
    -- ... other columns
);
SELECT create_hypertable('ohlcv', 'timestamp');

-- 3. Or skip if exists
SELECT create_hypertable('ohlcv', 'timestamp', if_not_exists => TRUE);
```

#### Error: "Chunk size too small"

**Solutions:**
```sql
-- 1. Set appropriate chunk interval
SELECT create_hypertable(
    'ohlcv',
    'timestamp',
    chunk_time_interval => INTERVAL '1 week'
);

-- 2. Modify existing hypertable
SELECT set_chunk_time_interval('ohlcv', INTERVAL '1 week');

-- 3. Check current chunks
SELECT * FROM timescaledb_information.chunks
WHERE hypertable_name = 'ohlcv'
ORDER BY range_start DESC;
```

### Diesel ORM Issues

#### Error: "diesel.toml not found"

**Solutions:**
```powershell
# 1. Initialize Diesel
diesel setup

# 2. Create diesel.toml manually
echo "[print_schema]" > diesel.toml
echo "file = `"src/schema.rs`"" >> diesel.toml
echo "custom_type_derives = [`"diesel::query_builder::QueryId`"]" >> diesel.toml

# 3. Verify DATABASE_URL
echo $env:DATABASE_URL
```

#### Error: "Migration failed"

**Solutions:**
```powershell
# 1. Check migration status
diesel migration list

# 2. Revert last migration
diesel migration revert

# 3. Redo migration
diesel migration redo

# 4. Fix migration SQL
# Edit migrations/TIMESTAMP_name/up.sql
# Fix syntax errors, then:
diesel migration run

# 5. Reset database (destructive!)
diesel database reset
```

#### Error: "Table not found in schema.rs"

**Solutions:**
```rust
// 1. Regenerate schema
// In terminal:
diesel print-schema > src/schema.rs

// 2. Verify table declaration
// src/schema.rs should have:
table! {
    ohlcv (timestamp, symbol_id) {
        timestamp -> Timestamptz,
        symbol_id -> Int4,
        open -> Float8,
        // ...
    }
}

// 3. Import schema in your code
mod schema;
use schema::ohlcv;
```

### Technical Indicator Calculation Issues

#### Error: "Insufficient data for indicator"

**Solutions:**
```rust
// 1. Check data length before calculation
pub fn calculate_rsi(prices: &[f64], period: usize) -> Result<f64> {
    if prices.len() < period + 1 {
        return Err(anyhow!(
            "Need {} prices, got {}",
            period + 1,
            prices.len()
        ));
    }
    // ... calculation
}

// 2. Fetch enough historical data
let limit = period + 50; // Extra buffer
let ohlcv = get_ohlcv(symbol, interval, limit).await?;

// 3. Handle gracefully
match calculate_rsi(&prices, 14) {
    Ok(rsi) => println!("RSI: {}", rsi),
    Err(e) => println!("Cannot calculate: {}", e)
}
```

#### Error: "NaN result in calculation"

**Solutions:**
```rust
// 1. Check for zero division
let average = if count > 0 {
    sum / count as f64
} else {
    0.0
};

// 2. Handle infinity
if result.is_infinite() || result.is_nan() {
    return Err(anyhow!("Invalid calculation result"));
}

// 3. Validate input data
for price in prices {
    if *price <= 0.0 || price.is_nan() || price.is_infinite() {
        return Err(anyhow!("Invalid price data: {}", price));
    }
}

// 4. Use f64::max for comparisons
let max_price = prices.iter()
    .copied()
    .fold(f64::NEG_INFINITY, f64::max);
```

## Deployment Issues

### Docker Issues

#### Error: "Cannot connect to Docker daemon"

**Solutions:**
```powershell
# 1. Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# 2. Check Docker status
docker info

# 3. Restart Docker service
Restart-Service docker

# 4. Check if running in admin mode
# Run PowerShell as Administrator
```

#### Error: "Build failed: COPY failed"

**Solutions:**
```dockerfile
# 1. Check file exists and path is correct
COPY package.json ./
# Not: COPY src/package.json ./ (if package.json is in root)

# 2. Check .dockerignore
# Ensure required files aren't ignored
# .dockerignore:
node_modules
dist
# Don't ignore: package.json, src/, etc.

# 3. Use correct context
docker build -t myapp -f Dockerfile .
#                                   ^ context

# 4. Check Windows path separators
COPY package.json ./
# Not: COPY package.json .\ (backslash)
```

#### Error: "Image size too large"

**Solutions:**
```dockerfile
# 1. Use multi-stage builds
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

# 2. Use alpine base images
FROM node:18-alpine  # Much smaller than node:18

# 3. Clean up in same layer
RUN apt-get update && \
    apt-get install -y build-essential && \
    npm install && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 4. Check image size
docker images | grep myapp
```

### AWS ECS Issues

#### Error: "Task failed to start"

**Solutions:**
```powershell
# 1. Check CloudWatch logs
aws logs tail /ecs/myapp --follow

# 2. Check task definition
aws ecs describe-task-definition --task-definition myapp:1

# 3. Verify environment variables
# In task definition:
{
  "environment": [
    {"name": "DATABASE_URL", "value": "..."},
    {"name": "REDIS_URL", "value": "..."}
  ]
}

# 4. Check IAM permissions
# Task execution role needs:
# - ecr:GetAuthorizationToken
# - ecr:BatchCheckLayerAvailability
# - logs:CreateLogStream
# - logs:PutLogEvents
```

#### Error: "Service unable to place task"

**Solutions:**
```powershell
# 1. Check capacity
aws ecs describe-clusters --clusters my-cluster

# 2. Check subnet and security groups
# Ensure:
# - Subnets have available IPs
# - Security groups allow required ports
# - NAT Gateway configured for private subnets

# 3. Check service limits
aws service-quotas get-service-quota \
  --service-code ecs \
  --quota-code L-3032A538

# 4. Review events
aws ecs describe-services \
  --cluster my-cluster \
  --services myapp \
  --query 'services[0].events[0:5]'
```

### GitHub Actions Issues

#### Error: "Workflow not triggered"

**Solutions:**
```yaml
# 1. Check trigger conditions
on:
  push:
    branches: [main]  # Ensure pushing to correct branch
  pull_request:
    branches: [main]

# 2. Verify .github/workflows location
# Must be: .github/workflows/ci.yml
# Not: github/workflows/ci.yml

# 3. Check YAML syntax
# Use online YAML validator

# 4. Check workflow permissions
# Settings > Actions > General > Workflow permissions
```

#### Error: "Step failed: Docker build"

**Solutions:**
```yaml
# 1. Add debugging
- name: Debug
  run: |
    pwd
    ls -la
    cat Dockerfile

# 2. Check secrets
- name: Build
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    echo "DATABASE_URL length: ${#DATABASE_URL}"
    # Don't echo actual secret!

# 3. Use explicit paths
- name: Build Docker image
  run: docker build -t myapp:${{ github.sha }} -f ./Dockerfile .
  working-directory: ./

# 4. Check Docker Hub rate limits
# Use authenticated pulls
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

## Testing Issues

### Integration Test Failures

#### Error: "Database not ready for tests"

**Solutions:**
```typescript
// 1. Wait for database
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

// 2. Use test containers
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

**Solutions:**
```typescript
// 1. Clear data before each test
beforeEach(async () => {
  await client.query('TRUNCATE TABLE users CASCADE');
  await client.query('TRUNCATE TABLE orders CASCADE');
});

// 2. Use transactions (faster)
let client: PoolClient;

beforeEach(async () => {
  client = await pool.connect();
  await client.query('BEGIN');
});

afterEach(async () => {
  await client.query('ROLLBACK');
  client.release();
});

// 3. Use unique test data
const testUser = {
  email: `test-${Date.now()}@example.com`,
  name: 'Test User'
};
```

## Debugging Tips

### Enable Verbose Logging

**TypeScript:**
```typescript
// Set environment variable
process.env.LOG_LEVEL = 'debug';

// Or use debug package
import debug from 'debug';
const log = debug('myapp:server');
log('Server starting...');
```

**Rust:**
```rust
// Set RUST_LOG environment variable
// RUST_LOG=debug cargo run

use env_logger;
env_logger::init();

log::debug!("Server starting...");
log::info!("Connected to database");
log::error!("Failed to connect: {}", err);
```

### Use Network Inspection

```powershell
# Monitor WebSocket connections
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.Options.SetRequestHeader("User-Agent", "Test")
# ... connect and inspect

# Test TCP connections
Test-NetConnection -ComputerName stream.binance.com -Port 9443

# Check DNS resolution
Resolve-DnsName stream.binance.com
```

### Profile Performance

**TypeScript:**
```typescript
// Use Node.js profiler
node --prof dist/index.js
node --prof-process isolate-*.log > profile.txt

// Or use clinic.js
npm install -g clinic
clinic doctor -- node dist/index.js
```

**Rust:**
```rust
// Use flamegraph
cargo install flamegraph
cargo flamegraph

// Or perf (Linux)
perf record -F 99 -g ./target/release/marketpulse
perf script > out.perf
```

---

For additional support:
- DataBridge GitHub Issues: https://github.com/yourorg/databridge/issues
- MarketPulse GitHub Issues: https://github.com/yourorg/marketpulse/issues
- MCP Documentation: https://modelcontextprotocol.io/

*Last updated: November 2024*
