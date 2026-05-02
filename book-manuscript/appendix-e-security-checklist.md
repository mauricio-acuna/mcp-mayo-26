# Appendix E: Security Best Practices Checklist

This appendix provides a comprehensive security checklist for MCP server deployments in production environments.

## Authentication & Authorization

### API Authentication

- [ ] **Implement OAuth 2.0** for user authentication
  - Use Authorization Code flow with PKCE for web apps
  - Use Client Credentials flow for server-to-server
  - Store tokens securely (encrypted at rest)
  - Implement token refresh mechanism
  
- [ ] **API Key Management**
  - Generate cryptographically secure API keys (min 32 bytes)
  - Hash API keys before storing in database
  - Implement key rotation policy (every 90 days)
  - Allow users to revoke keys immediately
  - Log all API key usage
  
- [ ] **Session Management**
  - Use secure session identifiers (UUID v4 or better)
  - Set appropriate session timeout (15-30 minutes idle)
  - Implement session invalidation on logout
  - Use HTTP-only, Secure, SameSite cookies
  - Regenerate session ID after authentication

### Authorization

- [ ] **Role-Based Access Control (RBAC)**
  - Define clear roles: admin, user, readonly
  - Implement least privilege principle
  - Document permission matrix
  - Regular permission audits
  
- [ ] **Resource-Level Authorization**
  - Verify user permissions for each resource access
  - Implement row-level security in database
  - Check permissions before database queries
  - Log authorization failures
  
- [ ] **Database Connector Permissions**
  ```typescript
  // ✅ Good: Check permissions
  async function executeQuery(user: User, connectorId: string, query: string) {
    const connector = await getConnector(connectorId);
    if (!user.hasAccessTo(connector)) {
      throw new ForbiddenError('Access denied');
    }
    return await connector.execute(query);
  }
  
  // ❌ Bad: No permission check
  async function executeQuery(connectorId: string, query: string) {
    const connector = await getConnector(connectorId);
    return await connector.execute(query);
  }
  ```

## Input Validation

### SQL Injection Prevention

- [ ] **Use Parameterized Queries**
  ```typescript
  // ✅ Good: Parameterized
  const result = await client.query(
    'SELECT * FROM users WHERE email = $1',
    [userEmail]
  );
  
  // ❌ Bad: String concatenation
  const result = await client.query(
    `SELECT * FROM users WHERE email = '${userEmail}'`
  );
  ```

- [ ] **Query Validation**
  - Whitelist allowed SQL keywords (SELECT, INSERT, etc.)
  - Block dangerous operations (DROP, TRUNCATE, DELETE without WHERE)
  - Validate table and column names against schema
  - Limit query complexity (max joins, subqueries)
  
- [ ] **Input Sanitization**
  ```typescript
  // Query validation example
  function validateQuery(query: string): void {
    const dangerous = /\b(DROP|TRUNCATE|DELETE\s+FROM\s+\w+\s*(?!WHERE))/i;
    if (dangerous.test(query)) {
      throw new Error('Dangerous operation detected');
    }
  }
  ```

### Data Type Validation

- [ ] **JSON Schema Validation**
  ```typescript
  import Ajv from 'ajv';
  
  const ajv = new Ajv();
  const validate = ajv.compile(inputSchema);
  
  if (!validate(input)) {
    throw new ValidationError(validate.errors);
  }
  ```

- [ ] **Type Coercion Prevention**
  - Strict type checking (TypeScript strict mode)
  - Validate number ranges (min/max)
  - Validate string lengths (maxLength)
  - Validate date formats (ISO 8601)
  - Validate email formats (RFC 5322)

### XSS Prevention

- [ ] **Output Encoding**
  ```typescript
  import { escape } from 'html-escaper';
  
  // ✅ Good: Encode output
  const safe = escape(userInput);
  
  // ❌ Bad: Raw output
  const unsafe = userInput;
  ```

- [ ] **Content Security Policy**
  ```typescript
  app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', "default-src 'self'");
    next();
  });
  ```

## Network Security

### HTTPS/TLS

- [ ] **Enforce HTTPS**
  - Use TLS 1.3 (or TLS 1.2 minimum)
  - Valid SSL/TLS certificates (Let's Encrypt, commercial CA)
  - Redirect HTTP to HTTPS
  - Enable HSTS (HTTP Strict Transport Security)
  
  ```typescript
  app.use((req, res, next) => {
    if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
      return res.redirect('https://' + req.get('host') + req.url);
    }
    next();
  });
  
  app.use((req, res, next) => {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    next();
  });
  ```

### CORS Configuration

- [ ] **Strict CORS Policy**
  ```typescript
  import cors from 'cors';
  
  // ✅ Good: Whitelist specific origins
  app.use(cors({
    origin: ['https://app.example.com', 'https://admin.example.com'],
    credentials: true,
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Authorization']
  }));
  
  // ❌ Bad: Allow all origins
  app.use(cors({ origin: '*' }));
  ```

### Firewall Rules

- [ ] **Network Segmentation**
  - Database in private subnet (no public access)
  - Application in public subnet (with ALB/NLB)
  - Redis in private subnet
  - Bastion host for admin access
  
- [ ] **Security Group Configuration**
  ```yaml
  # Example AWS Security Group
  ApplicationSG:
    Ingress:
      - Port: 443 (HTTPS)
        Source: 0.0.0.0/0
      - Port: 80 (HTTP, redirect only)
        Source: 0.0.0.0/0
    Egress:
      - Port: 5432 (PostgreSQL)
        Destination: DatabaseSG
      - Port: 6379 (Redis)
        Destination: RedisSG
  
  DatabaseSG:
    Ingress:
      - Port: 5432
        Source: ApplicationSG
    Egress: None
  ```

## Data Security

### Encryption at Rest

- [ ] **Database Encryption**
  - Enable PostgreSQL encryption (pgcrypto)
  - Encrypt sensitive columns (passwords, tokens, PII)
  - Use AES-256-GCM for encryption
  - Secure key management (AWS KMS, HashiCorp Vault)
  
  ```sql
  -- Encrypt sensitive column
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password_hash BYTEA,  -- Already hashed with bcrypt
    api_key BYTEA         -- Encrypted with pgcrypto
  );
  
  -- Insert encrypted data
  INSERT INTO users (email, api_key)
  VALUES ('user@example.com', pgp_sym_encrypt('secret-key', 'encryption-password'));
  
  -- Query encrypted data
  SELECT email, pgp_sym_decrypt(api_key, 'encryption-password')
  FROM users WHERE id = 1;
  ```

- [ ] **Backup Encryption**
  - Encrypt database backups
  - Encrypt Redis persistence files (RDB, AOF)
  - Secure backup storage (S3 with encryption)
  - Implement backup retention policy

### Encryption in Transit

- [ ] **TLS for All Connections**
  ```typescript
  // PostgreSQL with TLS
  const pool = new Pool({
    host: 'db.example.com',
    port: 5432,
    ssl: {
      rejectUnauthorized: true,
      ca: fs.readFileSync('/path/to/ca-cert.pem').toString()
    }
  });
  
  // Redis with TLS
  const redis = new Redis({
    host: 'redis.example.com',
    port: 6380,
    tls: {
      rejectUnauthorized: true,
      ca: fs.readFileSync('/path/to/ca-cert.pem')
    }
  });
  ```

### Secrets Management

- [ ] **Environment Variables**
  - Never commit secrets to version control
  - Use `.env` files (add to `.gitignore`)
  - Use secret management services (AWS Secrets Manager, Vault)
  
  ```bash
  # ❌ Bad: Hardcoded secrets
  DATABASE_URL=postgresql://user:password123@localhost/db
  
  # ✅ Good: Reference from secret manager
  DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id db-credentials --query SecretString --output text | jq -r .url)
  ```

- [ ] **Secret Rotation**
  - Rotate database passwords every 90 days
  - Rotate API keys every 90 days
  - Rotate TLS certificates before expiry
  - Automate rotation where possible

## Rate Limiting & DoS Prevention

### Request Rate Limiting

- [ ] **Per-User Rate Limits**
  ```typescript
  import rateLimit from 'express-rate-limit';
  
  const limiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 100, // 100 requests per minute
    message: 'Too many requests, please try again later',
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => req.user.id // Per user
  });
  
  app.use('/api/', limiter);
  ```

- [ ] **Dynamic Rate Limiting**
  ```typescript
  // Higher limits for premium users
  const getDynamicLimit = (user: User) => {
    if (user.tier === 'premium') return 1000;
    if (user.tier === 'basic') return 100;
    return 10; // Free tier
  };
  
  const limiter = rateLimit({
    max: (req) => getDynamicLimit(req.user)
  });
  ```

### Query Resource Limits

- [ ] **Query Timeouts**
  ```sql
  -- Set statement timeout (30 seconds)
  SET statement_timeout = 30000;
  ```

- [ ] **Result Set Limits**
  ```typescript
  const MAX_ROWS = 10000;
  
  function validateLimit(limit?: number): number {
    if (!limit) return 100; // Default
    if (limit > MAX_ROWS) throw new Error(`Limit exceeds maximum (${MAX_ROWS})`);
    return limit;
  }
  ```

- [ ] **Connection Limits**
  ```typescript
  const pool = new Pool({
    max: 20,           // Max connections
    min: 5,            // Min idle connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000
  });
  ```

### DDoS Protection

- [ ] **Infrastructure Level**
  - Use CDN (CloudFlare, Akamai)
  - Enable AWS Shield / Azure DDoS Protection
  - Configure Web Application Firewall (WAF)
  - Implement IP blacklisting for abusers

## Logging & Monitoring

### Security Event Logging

- [ ] **Authentication Events**
  ```typescript
  // Log successful login
  logger.info('User login successful', {
    userId: user.id,
    email: user.email,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    timestamp: new Date().toISOString()
  });
  
  // Log failed login
  logger.warn('User login failed', {
    email: attemptedEmail,
    ip: req.ip,
    reason: 'Invalid password',
    timestamp: new Date().toISOString()
  });
  ```

- [ ] **Authorization Failures**
  ```typescript
  logger.warn('Unauthorized access attempt', {
    userId: user.id,
    resource: req.path,
    method: req.method,
    ip: req.ip,
    timestamp: new Date().toISOString()
  });
  ```

- [ ] **Data Access Logs**
  ```typescript
  // Log sensitive data access
  logger.info('Database query executed', {
    userId: user.id,
    connectorId: connector.id,
    query: sanitizeQuery(query), // Don't log sensitive values
    rowCount: result.rowCount,
    duration: executionTime,
    timestamp: new Date().toISOString()
  });
  ```

### Security Monitoring

- [ ] **Anomaly Detection**
  - Monitor for unusual query patterns
  - Alert on excessive failed login attempts (>5 in 5 minutes)
  - Track API key usage patterns
  - Monitor for SQL injection attempts
  
- [ ] **Alert Configuration**
  ```yaml
  # Prometheus alerting rules
  groups:
    - name: security
      rules:
        - alert: HighFailedLoginRate
          expr: rate(failed_logins_total[5m]) > 10
          annotations:
            summary: "High failed login rate detected"
        
        - alert: SuspiciousQueryPattern
          expr: rate(dangerous_queries_total[1m]) > 0
          annotations:
            summary: "Dangerous SQL queries detected"
        
        - alert: UnauthorizedAccess
          expr: rate(unauthorized_requests_total[5m]) > 5
          annotations:
            summary: "Multiple unauthorized access attempts"
  ```

### Log Management

- [ ] **Secure Log Storage**
  - Centralized logging (ELK stack, Splunk, CloudWatch)
  - Encrypt logs at rest and in transit
  - Implement log retention policy (90 days minimum)
  - Regular log backups
  
- [ ] **Log Sanitization**
  ```typescript
  // ❌ Bad: Log sensitive data
  logger.info('Query executed', { query: `SELECT * FROM users WHERE password = '${password}'` });
  
  // ✅ Good: Sanitize sensitive data
  function sanitizeQuery(query: string): string {
    return query.replace(/['"]([^'"]{8,})['"]/, "'***'");
  }
  logger.info('Query executed', { query: sanitizeQuery(query) });
  ```

## Dependency Security

### Vulnerability Scanning

- [ ] **Regular Dependency Updates**
  ```bash
  # Check for vulnerabilities
  npm audit
  
  # Fix vulnerabilities
  npm audit fix
  
  # Force fix (may break)
  npm audit fix --force
  ```

- [ ] **Automated Scanning**
  ```yaml
  # GitHub Actions: Dependency scanning
  - name: Run npm audit
    run: npm audit --audit-level=moderate
  
  # Fail build on high/critical vulnerabilities
  - name: Check for high vulnerabilities
    run: |
      AUDIT_RESULT=$(npm audit --json)
      HIGH=$(echo $AUDIT_RESULT | jq '.metadata.vulnerabilities.high')
      CRITICAL=$(echo $AUDIT_RESULT | jq '.metadata.vulnerabilities.critical')
      if [ $HIGH -gt 0 ] || [ $CRITICAL -gt 0 ]; then
        echo "High or critical vulnerabilities found"
        exit 1
      fi
  ```

### Dependency Pinning

- [ ] **Lock Files**
  - Commit `package-lock.json` (npm)
  - Commit `Cargo.lock` (Rust)
  - Use exact versions in production
  
  ```json
  // package.json
  {
    "dependencies": {
      "express": "4.18.2",  // ✅ Exact version
      // Not: "express": "^4.18.2" (allows updates)
    }
  }
  ```

### Supply Chain Security

- [ ] **Verify Package Integrity**
  ```bash
  # npm: Check package signatures
  npm install --ignore-scripts
  
  # Rust: Check cargo-audit
  cargo install cargo-audit
  cargo audit
  ```

- [ ] **Use Private Registry**
  - Host internal packages privately
  - Proxy public packages through private registry
  - Scan packages before allowing

## Database Security

### PostgreSQL Hardening

- [ ] **Configuration**
  ```conf
  # postgresql.conf
  ssl = on
  ssl_cert_file = '/path/to/server.crt'
  ssl_key_file = '/path/to/server.key'
  ssl_ca_file = '/path/to/ca.crt'
  
  password_encryption = scram-sha-256
  
  # Logging
  log_connections = on
  log_disconnections = on
  log_duration = on
  log_statement = 'mod'  # Log all modifications
  ```

- [ ] **Access Control**
  ```conf
  # pg_hba.conf
  # TYPE  DATABASE  USER      ADDRESS         METHOD
  local   all       postgres                  peer
  host    all       all       127.0.0.1/32    scram-sha-256
  hostssl all       app_user  10.0.0.0/8      scram-sha-256
  host    all       all       0.0.0.0/0       reject
  ```

- [ ] **User Permissions**
  ```sql
  -- Create limited user
  CREATE USER app_user WITH PASSWORD 'strong-password';
  
  -- Grant minimal permissions
  GRANT CONNECT ON DATABASE mydb TO app_user;
  GRANT SELECT, INSERT, UPDATE ON TABLE users TO app_user;
  
  -- Revoke dangerous permissions
  REVOKE CREATE ON SCHEMA public FROM PUBLIC;
  REVOKE ALL ON TABLE pg_user FROM PUBLIC;
  ```

### Redis Security

- [ ] **Configuration**
  ```conf
  # redis.conf
  requirepass your-strong-password
  
  # Disable dangerous commands
  rename-command FLUSHDB ""
  rename-command FLUSHALL ""
  rename-command CONFIG "CONFIG-xyz-secret"
  
  # Network binding
  bind 127.0.0.1 10.0.1.5  # Not 0.0.0.0
  protected-mode yes
  
  # TLS
  tls-port 6380
  tls-cert-file /path/to/redis.crt
  tls-key-file /path/to/redis.key
  tls-ca-cert-file /path/to/ca.crt
  ```

## Application Security

### Error Handling

- [ ] **Safe Error Messages**
  ```typescript
  // ❌ Bad: Expose internal details
  catch (error) {
    return res.status(500).json({
      error: error.message,  // "ECONNREFUSED 10.0.1.5:5432"
      stack: error.stack
    });
  }
  
  // ✅ Good: Generic error message
  catch (error) {
    logger.error('Database error', { error, userId: req.user.id });
    return res.status(500).json({
      error: 'An error occurred processing your request'
    });
  }
  ```

### Security Headers

- [ ] **HTTP Security Headers**
  ```typescript
  import helmet from 'helmet';
  
  app.use(helmet());
  
  // Or manually:
  app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('Permissions-Policy', 'geolocation=(), microphone=()');
    next();
  });
  ```

### Process Isolation

- [ ] **Run as Non-Root User**
  ```dockerfile
  # Dockerfile
  FROM node:18-alpine
  
  # Create non-root user
  RUN addgroup -g 1001 -S nodejs && \
      adduser -S nodejs -u 1001
  
  USER nodejs
  
  COPY --chown=nodejs:nodejs . .
  
  CMD ["node", "dist/index.js"]
  ```

## Compliance & Auditing

### GDPR Compliance

- [ ] **Data Minimization**
  - Only collect necessary data
  - Implement data retention policies
  - Provide data export functionality
  - Implement right to deletion

- [ ] **Consent Management**
  - Explicit consent for data processing
  - Granular consent options
  - Easy consent withdrawal

### Audit Trail

- [ ] **Change Tracking**
  ```sql
  -- Audit table
  CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(50),
    table_name VARCHAR(50),
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
  );
  
  -- Trigger for automatic auditing
  CREATE OR REPLACE FUNCTION audit_trigger()
  RETURNS TRIGGER AS $$
  BEGIN
    INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values)
    VALUES (
      current_setting('app.user_id')::INTEGER,
      TG_OP,
      TG_TABLE_NAME,
      NEW.id,
      row_to_json(OLD),
      row_to_json(NEW)
    );
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;
  ```

### Regular Security Reviews

- [ ] **Quarterly Security Audits**
  - Review access controls
  - Check for unused accounts
  - Verify encryption settings
  - Test backup restoration
  - Review security logs

- [ ] **Penetration Testing**
  - Annual penetration tests
  - Address findings promptly
  - Retest after fixes

## Deployment Security

### Container Security

- [ ] **Docker Best Practices**
  ```dockerfile
  # Use specific version tags
  FROM node:18.19.0-alpine  # Not 'latest'
  
  # Run as non-root
  USER node
  
  # Scan for vulnerabilities
  # docker scan myimage:latest
  
  # Use multi-stage builds (smaller attack surface)
  FROM node:18-alpine AS builder
  # ... build
  FROM node:18-alpine
  COPY --from=builder /app/dist ./dist
  ```

### Kubernetes Security

- [ ] **Pod Security**
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: myapp
  spec:
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
      fsGroup: 1000
    containers:
      - name: app
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: [ALL]
  ```

---

## Security Checklist Summary

**Critical (Must Have):**
- ✅ HTTPS/TLS encryption
- ✅ Input validation & parameterized queries
- ✅ Authentication & authorization
- ✅ Secure secrets management
- ✅ Rate limiting
- ✅ Security logging

**High Priority:**
- ✅ Dependency vulnerability scanning
- ✅ Database encryption
- ✅ CORS configuration
- ✅ Error handling
- ✅ Network segmentation

**Medium Priority:**
- ✅ Security headers
- ✅ Audit logging
- ✅ Container security
- ✅ Backup encryption
- ✅ Regular security reviews

**Nice to Have:**
- ✅ Anomaly detection
- ✅ Penetration testing
- ✅ GDPR compliance features
- ✅ Advanced monitoring

---

*Last updated: November 2024*
*Compliance: OWASP Top 10, CIS Benchmarks, GDPR, SOC 2*
