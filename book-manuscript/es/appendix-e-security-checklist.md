# Apéndice E: Lista de Verificación de Mejores Prácticas de Seguridad

Este apéndice proporciona una lista de verificación integral de seguridad para implementaciones de servidores MCP en entornos de producción.

## Autenticación y Autorización

### Autenticación de API

- [ ] **Implementar OAuth 2.0** para autenticación de usuarios
  - Usar flujo de Authorization Code con PKCE para aplicaciones web
  - Usar flujo de Client Credentials para comunicación servidor-a-servidor
  - Almacenar tokens de forma segura (cifrados en reposo)
  - Implementar mecanismo de actualización de tokens
  
- [ ] **Gestión de API Keys**
  - Generar API keys criptográficamente seguras (mínimo 32 bytes)
  - Aplicar hash a las API keys antes de almacenarlas en la base de datos
  - Implementar política de rotación de keys (cada 90 días)
  - Permitir a los usuarios revocar keys inmediatamente
  - Registrar todo el uso de API keys
  
- [ ] **Gestión de Sesiones**
  - Usar identificadores de sesión seguros (UUID v4 o mejor)
  - Establecer timeout de sesión apropiado (15-30 minutos de inactividad)
  - Implementar invalidación de sesión al cerrar sesión
  - Usar cookies HTTP-only, Secure, SameSite
  - Regenerar el ID de sesión después de la autenticación

### Autorización

- [ ] **Control de Acceso Basado en Roles (RBAC)**
  - Definir roles claros: admin, user, readonly
  - Implementar principio de mínimo privilegio
  - Documentar matriz de permisos
  - Auditorías regulares de permisos
  
- [ ] **Autorización a Nivel de Recurso**
  - Verificar permisos de usuario para cada acceso a recurso
  - Implementar seguridad a nivel de fila en la base de datos
  - Verificar permisos antes de las consultas a la base de datos
  - Registrar fallos de autorización
  
- [ ] **Permisos de Conectores de Base de Datos**
  ```typescript
  // ✅ Bien: Verificar permisos
  async function executeQuery(user: User, connectorId: string, query: string) {
    const connector = await getConnector(connectorId);
    if (!user.hasAccessTo(connector)) {
      throw new ForbiddenError('Access denied');
    }
    return await connector.execute(query);
  }
  
  // ❌ Mal: Sin verificación de permisos
  async function executeQuery(connectorId: string, query: string) {
    const connector = await getConnector(connectorId);
    return await connector.execute(query);
  }
  ```

## Validación de Entrada

### Prevención de Inyección SQL

- [ ] **Usar Consultas Parametrizadas**
  ```typescript
  // ✅ Bien: Parametrizado
  const result = await client.query(
    'SELECT * FROM users WHERE email = $1',
    [userEmail]
  );
  
  // ❌ Mal: Concatenación de strings
  const result = await client.query(
    `SELECT * FROM users WHERE email = '${userEmail}'`
  );
  ```

- [ ] **Validación de Consultas**
  - Lista blanca de palabras clave SQL permitidas (SELECT, INSERT, etc.)
  - Bloquear operaciones peligrosas (DROP, TRUNCATE, DELETE sin WHERE)
  - Validar nombres de tablas y columnas contra el esquema
  - Limitar complejidad de consultas (máximo de joins, subconsultas)
  
- [ ] **Sanitización de Entrada**
  ```typescript
  // Ejemplo de validación de consultas
  function validateQuery(query: string): void {
    const dangerous = /\b(DROP|TRUNCATE|DELETE\s+FROM\s+\w+\s*(?!WHERE))/i;
    if (dangerous.test(query)) {
      throw new Error('Dangerous operation detected');
    }
  }
  ```

### Validación de Tipos de Datos

- [ ] **Validación de JSON Schema**
  ```typescript
  import Ajv from 'ajv';
  
  const ajv = new Ajv();
  const validate = ajv.compile(inputSchema);
  
  if (!validate(input)) {
    throw new ValidationError(validate.errors);
  }
  ```

- [ ] **Prevención de Coerción de Tipos**
  - Verificación de tipos estricta (modo strict de TypeScript)
  - Validar rangos numéricos (min/max)
  - Validar longitudes de strings (maxLength)
  - Validar formatos de fecha (ISO 8601)
  - Validar formatos de email (RFC 5322)

### Prevención de XSS

- [ ] **Codificación de Salida**
  ```typescript
  import { escape } from 'html-escaper';
  
  // ✅ Bien: Codificar salida
  const safe = escape(userInput);
  
  // ❌ Mal: Salida cruda
  const unsafe = userInput;
  ```

- [ ] **Content Security Policy**
  ```typescript
  app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', "default-src 'self'");
    next();
  });
  ```

## Seguridad de Red

### HTTPS/TLS

- [ ] **Forzar HTTPS**
  - Usar TLS 1.3 (o TLS 1.2 mínimo)
  - Certificados SSL/TLS válidos (Let's Encrypt, CA comercial)
  - Redirigir HTTP a HTTPS
  - Habilitar HSTS (HTTP Strict Transport Security)
  
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

### Configuración de CORS

- [ ] **Política CORS Estricta**
  ```typescript
  import cors from 'cors';
  
  // ✅ Bien: Lista blanca de orígenes específicos
  app.use(cors({
    origin: ['https://app.example.com', 'https://admin.example.com'],
    credentials: true,
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Authorization']
  }));
  
  // ❌ Mal: Permitir todos los orígenes
  app.use(cors({ origin: '*' }));
  ```

### Reglas de Firewall

- [ ] **Segmentación de Red**
  - Base de datos en subred privada (sin acceso público)
  - Aplicación en subred pública (con ALB/NLB)
  - Redis en subred privada
  - Bastion host para acceso administrativo
  
- [ ] **Configuración de Security Group**
  ```yaml
  # Ejemplo de AWS Security Group
  ApplicationSG:
    Ingress:
      - Port: 443 (HTTPS)
        Source: 0.0.0.0/0
      - Port: 80 (HTTP, solo redirección)
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

## Seguridad de Datos

### Cifrado en Reposo

- [ ] **Cifrado de Base de Datos**
  - Habilitar cifrado de PostgreSQL (pgcrypto)
  - Cifrar columnas sensibles (contraseñas, tokens, PII)
  - Usar AES-256-GCM para cifrado
  - Gestión segura de claves (AWS KMS, HashiCorp Vault)
  
  ```sql
  -- Cifrar columna sensible
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password_hash BYTEA,  -- Ya hasheada con bcrypt
    api_key BYTEA         -- Cifrada con pgcrypto
  );
  
  -- Insertar datos cifrados
  INSERT INTO users (email, api_key)
  VALUES ('user@example.com', pgp_sym_encrypt('secret-key', 'encryption-password'));
  
  -- Consultar datos cifrados
  SELECT email, pgp_sym_decrypt(api_key, 'encryption-password')
  FROM users WHERE id = 1;
  ```

- [ ] **Cifrado de Backups**
  - Cifrar backups de base de datos
  - Cifrar archivos de persistencia de Redis (RDB, AOF)
  - Almacenamiento seguro de backups (S3 con cifrado)
  - Implementar política de retención de backups

### Cifrado en Tránsito

- [ ] **TLS para Todas las Conexiones**
  ```typescript
  // PostgreSQL con TLS
  const pool = new Pool({
    host: 'db.example.com',
    port: 5432,
    ssl: {
      rejectUnauthorized: true,
      ca: fs.readFileSync('/path/to/ca-cert.pem').toString()
    }
  });
  
  // Redis con TLS
  const redis = new Redis({
    host: 'redis.example.com',
    port: 6380,
    tls: {
      rejectUnauthorized: true,
      ca: fs.readFileSync('/path/to/ca-cert.pem')
    }
  });
  ```

### Gestión de Secretos

- [ ] **Variables de Entorno**
  - Nunca commitear secretos al control de versiones
  - Usar archivos `.env` (añadir a `.gitignore`)
  - Usar servicios de gestión de secretos (AWS Secrets Manager, Vault)
  
  ```bash
  # ❌ Mal: Secretos hardcodeados
  DATABASE_URL=postgresql://user:password123@localhost/db
  
  # ✅ Bien: Referencia desde gestor de secretos
  DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id db-credentials --query SecretString --output text | jq -r .url)
  ```

- [ ] **Rotación de Secretos**
  - Rotar contraseñas de base de datos cada 90 días
  - Rotar API keys cada 90 días
  - Rotar certificados TLS antes de su expiración
  - Automatizar rotación cuando sea posible

## Rate Limiting y Prevención de DoS

### Rate Limiting de Solicitudes

- [ ] **Límites de Rate por Usuario**
  ```typescript
  import rateLimit from 'express-rate-limit';
  
  const limiter = rateLimit({
    windowMs: 60 * 1000, // 1 minuto
    max: 100, // 100 solicitudes por minuto
    message: 'Too many requests, please try again later',
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => req.user.id // Por usuario
  });
  
  app.use('/api/', limiter);
  ```

- [ ] **Rate Limiting Dinámico**
  ```typescript
  // Límites más altos para usuarios premium
  const getDynamicLimit = (user: User) => {
    if (user.tier === 'premium') return 1000;
    if (user.tier === 'basic') return 100;
    return 10; // Tier gratuito
  };
  
  const limiter = rateLimit({
    max: (req) => getDynamicLimit(req.user)
  });
  ```

### Límites de Recursos de Consultas

- [ ] **Timeouts de Consultas**
  ```sql
  -- Establecer timeout de statement (30 segundos)
  SET statement_timeout = 30000;
  ```

- [ ] **Límites de Conjunto de Resultados**
  ```typescript
  const MAX_ROWS = 10000;
  
  function validateLimit(limit?: number): number {
    if (!limit) return 100; // Por defecto
    if (limit > MAX_ROWS) throw new Error(`Limit exceeds maximum (${MAX_ROWS})`);
    return limit;
  }
  ```

- [ ] **Límites de Conexión**
  ```typescript
  const pool = new Pool({
    max: 20,           // Conexiones máximas
    min: 5,            // Conexiones inactivas mínimas
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000
  });
  ```

### Protección contra DDoS

- [ ] **Nivel de Infraestructura**
  - Usar CDN (CloudFlare, Akamai)
  - Habilitar AWS Shield / Azure DDoS Protection
  - Configurar Web Application Firewall (WAF)
  - Implementar blacklisting de IP para abusadores

## Logging y Monitoreo

### Logging de Eventos de Seguridad

- [ ] **Eventos de Autenticación**
  ```typescript
  // Registrar login exitoso
  logger.info('User login successful', {
    userId: user.id,
    email: user.email,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    timestamp: new Date().toISOString()
  });
  
  // Registrar login fallido
  logger.warn('User login failed', {
    email: attemptedEmail,
    ip: req.ip,
    reason: 'Invalid password',
    timestamp: new Date().toISOString()
  });
  ```

- [ ] **Fallos de Autorización**
  ```typescript
  logger.warn('Unauthorized access attempt', {
    userId: user.id,
    resource: req.path,
    method: req.method,
    ip: req.ip,
    timestamp: new Date().toISOString()
  });
  ```

- [ ] **Logs de Acceso a Datos**
  ```typescript
  // Registrar acceso a datos sensibles
  logger.info('Database query executed', {
    userId: user.id,
    connectorId: connector.id,
    query: sanitizeQuery(query), // No registrar valores sensibles
    rowCount: result.rowCount,
    duration: executionTime,
    timestamp: new Date().toISOString()
  });
  ```

### Monitoreo de Seguridad

- [ ] **Detección de Anomalías**
  - Monitorear patrones de consultas inusuales
  - Alertar sobre intentos excesivos de login fallido (>5 en 5 minutos)
  - Rastrear patrones de uso de API keys
  - Monitorear intentos de inyección SQL
  
- [ ] **Configuración de Alertas**
  ```yaml
  # Reglas de alerta de Prometheus
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

### Gestión de Logs

- [ ] **Almacenamiento Seguro de Logs**
  - Logging centralizado (stack ELK, Splunk, CloudWatch)
  - Cifrar logs en reposo y en tránsito
  - Implementar política de retención de logs (mínimo 90 días)
  - Backups regulares de logs
  
- [ ] **Sanitización de Logs**
  ```typescript
  // ❌ Mal: Registrar datos sensibles
  logger.info('Query executed', { query: `SELECT * FROM users WHERE password = '${password}'` });
  
  // ✅ Bien: Sanitizar datos sensibles
  function sanitizeQuery(query: string): string {
    return query.replace(/['"]([^'"]{8,})['"]/, "'***'");
  }
  logger.info('Query executed', { query: sanitizeQuery(query) });
  ```

## Seguridad de Dependencias

### Escaneo de Vulnerabilidades

- [ ] **Actualizaciones Regulares de Dependencias**
  ```bash
  # Verificar vulnerabilidades
  npm audit
  
  # Corregir vulnerabilidades
  npm audit fix
  
  # Corrección forzada (puede romper)
  npm audit fix --force
  ```

- [ ] **Escaneo Automatizado**
  ```yaml
  # GitHub Actions: Escaneo de dependencias
  - name: Run npm audit
    run: npm audit --audit-level=moderate
  
  # Fallar build en vulnerabilidades high/critical
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

### Fijación de Dependencias

- [ ] **Lock Files**
  - Commitear `package-lock.json` (npm)
  - Commitear `Cargo.lock` (Rust)
  - Usar versiones exactas en producción
  
  ```json
  // package.json
  {
    "dependencies": {
      "express": "4.18.2",  // ✅ Versión exacta
      // No: "express": "^4.18.2" (permite actualizaciones)
    }
  }
  ```

### Seguridad de Cadena de Suministro

- [ ] **Verificar Integridad de Paquetes**
  ```bash
  # npm: Verificar firmas de paquetes
  npm install --ignore-scripts
  
  # Rust: Verificar cargo-audit
  cargo install cargo-audit
  cargo audit
  ```

- [ ] **Usar Registro Privado**
  - Hospedar paquetes internos de forma privada
  - Proxy de paquetes públicos a través de registro privado
  - Escanear paquetes antes de permitirlos

## Seguridad de Base de Datos

### Endurecimiento de PostgreSQL

- [ ] **Configuración**
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
  log_statement = 'mod'  # Registrar todas las modificaciones
  ```

- [ ] **Control de Acceso**
  ```conf
  # pg_hba.conf
  # TYPE  DATABASE  USER      ADDRESS         METHOD
  local   all       postgres                  peer
  host    all       all       127.0.0.1/32    scram-sha-256
  hostssl all       app_user  10.0.0.0/8      scram-sha-256
  host    all       all       0.0.0.0/0       reject
  ```

- [ ] **Permisos de Usuario**
  ```sql
  -- Crear usuario limitado
  CREATE USER app_user WITH PASSWORD 'strong-password';
  
  -- Otorgar permisos mínimos
  GRANT CONNECT ON DATABASE mydb TO app_user;
  GRANT SELECT, INSERT, UPDATE ON TABLE users TO app_user;
  
  -- Revocar permisos peligrosos
  REVOKE CREATE ON SCHEMA public FROM PUBLIC;
  REVOKE ALL ON TABLE pg_user FROM PUBLIC;
  ```

### Seguridad de Redis

- [ ] **Configuración**
  ```conf
  # redis.conf
  requirepass your-strong-password
  
  # Deshabilitar comandos peligrosos
  rename-command FLUSHDB ""
  rename-command FLUSHALL ""
  rename-command CONFIG "CONFIG-xyz-secret"
  
  # Enlace de red
  bind 127.0.0.1 10.0.1.5  # No 0.0.0.0
  protected-mode yes
  
  # TLS
  tls-port 6380
  tls-cert-file /path/to/redis.crt
  tls-key-file /path/to/redis.key
  tls-ca-cert-file /path/to/ca.crt
  ```

## Seguridad de Aplicación

### Manejo de Errores

- [ ] **Mensajes de Error Seguros**
  ```typescript
  // ❌ Mal: Exponer detalles internos
  catch (error) {
    return res.status(500).json({
      error: error.message,  // "ECONNREFUSED 10.0.1.5:5432"
      stack: error.stack
    });
  }
  
  // ✅ Bien: Mensaje de error genérico
  catch (error) {
    logger.error('Database error', { error, userId: req.user.id });
    return res.status(500).json({
      error: 'An error occurred processing your request'
    });
  }
  ```

### Headers de Seguridad

- [ ] **HTTP Security Headers**
  ```typescript
  import helmet from 'helmet';
  
  app.use(helmet());
  
  // O manualmente:
  app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('Permissions-Policy', 'geolocation=(), microphone=()');
    next();
  });
  ```

### Aislamiento de Procesos

- [ ] **Ejecutar como Usuario No-Root**
  ```dockerfile
  # Dockerfile
  FROM node:18-alpine
  
  # Crear usuario no-root
  RUN addgroup -g 1001 -S nodejs && \
      adduser -S nodejs -u 1001
  
  USER nodejs
  
  COPY --chown=nodejs:nodejs . .
  
  CMD ["node", "dist/index.js"]
  ```

## Cumplimiento y Auditoría

### Cumplimiento GDPR

- [ ] **Minimización de Datos**
  - Solo recopilar datos necesarios
  - Implementar políticas de retención de datos
  - Proporcionar funcionalidad de exportación de datos
  - Implementar derecho a eliminación

- [ ] **Gestión de Consentimiento**
  - Consentimiento explícito para procesamiento de datos
  - Opciones de consentimiento granulares
  - Retirada de consentimiento fácil

### Pista de Auditoría

- [ ] **Seguimiento de Cambios**
  ```sql
  -- Tabla de auditoría
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
  
  -- Trigger para auditoría automática
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

### Revisiones Regulares de Seguridad

- [ ] **Auditorías de Seguridad Trimestrales**
  - Revisar controles de acceso
  - Verificar cuentas no utilizadas
  - Verificar configuración de cifrado
  - Probar restauración de backups
  - Revisar logs de seguridad

- [ ] **Pruebas de Penetración**
  - Pruebas de penetración anuales
  - Abordar hallazgos rápidamente
  - Re-probar después de correcciones

## Seguridad de Implementación

### Seguridad de Contenedores

- [ ] **Mejores Prácticas de Docker**
  ```dockerfile
  # Usar tags de versión específicos
  FROM node:18.19.0-alpine  # No 'latest'
  
  # Ejecutar como no-root
  USER node
  
  # Escanear vulnerabilidades
  # docker scan myimage:latest
  
  # Usar builds multi-etapa (superficie de ataque menor)
  FROM node:18-alpine AS builder
  # ... build
  FROM node:18-alpine
  COPY --from=builder /app/dist ./dist
  ```

### Seguridad de Kubernetes

- [ ] **Seguridad de Pod**
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

## Resumen de Lista de Verificación de Seguridad

**Crítico (Debe Tener):**
- ✅ Cifrado HTTPS/TLS
- ✅ Validación de entrada y consultas parametrizadas
- ✅ Autenticación y autorización
- ✅ Gestión segura de secretos
- ✅ Rate limiting
- ✅ Logging de seguridad

**Alta Prioridad:**
- ✅ Escaneo de vulnerabilidades de dependencias
- ✅ Cifrado de base de datos
- ✅ Configuración de CORS
- ✅ Manejo de errores
- ✅ Segmentación de red

**Prioridad Media:**
- ✅ Headers de seguridad
- ✅ Logging de auditoría
- ✅ Seguridad de contenedores
- ✅ Cifrado de backups
- ✅ Revisiones regulares de seguridad

**Nice to Have:**
- ✅ Detección de anomalías
- ✅ Pruebas de penetración
- ✅ Características de cumplimiento GDPR
- ✅ Monitoreo avanzado

---

*Última actualización: Noviembre 2024*
*Cumplimiento: OWASP Top 10, CIS Benchmarks, GDPR, SOC 2*
