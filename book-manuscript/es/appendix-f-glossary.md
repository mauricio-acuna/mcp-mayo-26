# Apéndice F: Glosario de Términos

Este glosario define términos clave, acrónimos y conceptos utilizados a lo largo del libro.

## A

**Aggregation**  
El proceso de combinar múltiples puntos de datos en estadísticas resumidas (suma, promedio, conteo, etc.). En SQL, se realiza usando GROUP BY con funciones de agregación.

**API (Application Programming Interface)**  
Un conjunto de reglas y protocolos que permiten a diferentes aplicaciones de software comunicarse. En este libro, se refiere a APIs de bases de datos y la API del protocolo MCP.

**API Key**  
Un identificador único utilizado para autenticar solicitudes a una API. Debe mantenerse en secreto y rotarse regularmente.

**Async/Await**  
Un patrón de programación para manejar operaciones asíncronas de manera que parezca síncrona. Ampliamente utilizado en JavaScript/TypeScript y Rust.

**ATR (Average True Range)**  
Un indicador técnico que mide la volatilidad del mercado calculando el rango promedio entre precios altos y bajos durante un período.

**Authentication**  
El proceso de verificar la identidad de un usuario o sistema. Los métodos comunes incluyen contraseñas, API keys y tokens OAuth.

**Authorization**  
El proceso de determinar si un usuario autenticado tiene permiso para realizar una acción específica o acceder a un recurso.

## B

**Bcrypt**  
Un algoritmo de hashing de contraseñas diseñado para ser lento y resistente a ataques de fuerza bruta. Utiliza un factor de trabajo para controlar el tiempo de cómputo.

**Binance**  
Un importante exchange de criptomonedas. MarketPulse utiliza la API WebSocket de Binance para datos de mercado en tiempo real.

**Bollinger Bands**  
Un indicador técnico que consiste en una media móvil con bandas superior e inferior que representan desviaciones estándar, utilizado para identificar condiciones de sobrecompra/sobreventa.

**Broadcast Channel**  
Un patrón de comunicación donde los mensajes se envían a múltiples suscriptores simultáneamente. Utilizado en MarketPulse para distribuir actualizaciones de precios.

**Buffer**  
Un área de almacenamiento temporal para datos, típicamente utilizada cuando los datos se transfieren entre procesos o a través de redes.

## C

**Cache**  
Una capa de almacenamiento de alta velocidad que almacena datos de acceso frecuente para reducir la latencia. Redis se usa comúnmente como caché distribuida.

**Candlestick / OHLCV**  
Un formato de gráfico de precios que muestra precios de Apertura (Open), Alto (High), Bajo (Low), Cierre (Close) y Volumen (Volume) para un período de tiempo. Utilizado en análisis de mercados financieros.

**CI/CD (Continuous Integration / Continuous Deployment)**  
Una práctica de desarrollo de software que involucra construcción, prueba e implementación automatizadas de cambios de código.

**Claude Desktop**  
La aplicación de escritorio de Anthropic para Claude AI que soporta servidores MCP, permitiendo a los usuarios extender las capacidades de Claude.

**Connection Pool**  
Una caché de conexiones de base de datos mantenidas para reutilización, mejorando el rendimiento al evitar la sobrecarga de crear nuevas conexiones.

**CORS (Cross-Origin Resource Sharing)**  
Un mecanismo de seguridad que permite o restringe que recursos en un servidor web sean solicitados desde otro dominio.

**Crate**  
El término de Rust para un paquete o biblioteca. Distribuido a través de crates.io, el registro de paquetes de Rust.

**Cryptocurrency**  
Una moneda digital o virtual asegurada por criptografía. Ejemplos: Bitcoin (BTC), Ethereum (ETH), Solana (SOL).

**CSV (Comma-Separated Values)**  
Un formato de archivo simple para datos tabulares donde los valores están separados por comas. Comúnmente utilizado para exportación de datos.

## D

**DataBridge**  
El proyecto de servidor MCP basado en TypeScript desarrollado en la Parte II de este libro, enfocado en integración de datos empresariales.

**Database Connector**  
Una configuración que define cómo conectarse a una instancia de base de datos específica, incluyendo host, credenciales y parámetros de conexión.

**Diesel**  
Un ORM seguro y extensible y constructor de consultas para Rust. Utilizado en MarketPulse para operaciones de base de datos.

**Docker**  
Una plataforma para desarrollar, enviar y ejecutar aplicaciones en contenedores, proporcionando entornos consistentes entre desarrollo y producción.

**Docker Compose**  
Una herramienta para definir y ejecutar aplicaciones Docker multi-contenedor usando un archivo de configuración YAML.

## E

**ECS (Elastic Container Service)**  
Servicio de AWS para ejecutar contenedores Docker en producción a escala, con soporte para Fargate (serverless) e implementaciones EC2.

**EMA (Exponential Moving Average)**  
Un indicador técnico que da más peso a los precios recientes, haciéndolo más sensible a cambios de precios que una media móvil simple.

**Environment Variable**  
Un valor dinámico que afecta cómo se ejecutan los procesos en una computadora. Utilizado para configurar aplicaciones sin hardcodear valores.

**ETL (Extract, Transform, Load)**  
Un proceso de integración de datos para extraer datos de fuentes, transformarlos y cargarlos en un sistema de destino.

## F

**Fargate**  
Motor de cómputo serverless de AWS para contenedores, eliminando la necesidad de provisionar y gestionar servidores.

**Foreign Key**  
Una restricción de base de datos que establece una relación entre dos tablas, asegurando integridad referencial.

## G

**GitHub Actions**  
Una plataforma CI/CD integrada con GitHub que automatiza flujos de trabajo como pruebas, construcción e implementación.

**Graceful Shutdown**  
El proceso de detener limpiamente un servidor completando solicitudes en progreso y cerrando conexiones antes de terminar.

## H

**Hypertable**  
Una característica de TimescaleDB que particiona datos de series temporales en fragmentos para mejorar el rendimiento de consultas y la gestión de datos.

**HTTPS (HTTP Secure)**  
Una extensión de HTTP que usa cifrado TLS/SSL para asegurar la comunicación a través de una red.

## I

**Idempotent**  
Una operación que produce el mismo resultado independientemente de cuántas veces se ejecute. Importante para sistemas distribuidos confiables.

**Index (Database)**  
Una estructura de datos que mejora la velocidad de operaciones de recuperación de datos en una tabla de base de datos a costa de almacenamiento adicional y rendimiento de escritura.

**Indicator (Technical)**  
Un cálculo matemático basado en datos de precio y/o volumen usado para analizar tendencias de mercado y tomar decisiones de trading.

**Input Schema**  
Una definición de JSON Schema que especifica la estructura, tipos y reglas de validación para entradas de herramientas en MCP.

## J

**JSON (JavaScript Object Notation)**  
Un formato de intercambio de datos ligero que es fácil de leer y escribir para humanos y fácil de analizar y generar para máquinas.

**JSON-RPC**  
Un protocolo de llamada a procedimiento remoto codificado en JSON. MCP utiliza JSON-RPC 2.0 como su protocolo base.

**JWT (JSON Web Token)**  
Un medio compacto y seguro para URL de representar reclamaciones entre dos partes, comúnmente usado para autenticación y autorización.

## K

**Kubernetes (K8s)**  
Una plataforma de orquestación de contenedores de código abierto para automatizar la implementación, escalado y gestión de aplicaciones en contenedores.

## L

**Latency**  
El retraso de tiempo entre una solicitud y su respuesta. Menor latencia significa tiempos de respuesta del sistema más rápidos.

**LLM (Large Language Model)**  
Un modelo de IA entrenado en grandes cantidades de datos de texto, capaz de entender y generar texto similar al humano. Ejemplos: Claude, GPT-4.

**Load Balancer**  
Un dispositivo o servicio que distribuye tráfico de red a través de múltiples servidores para asegurar que ningún servidor único sea sobrecargado.

## M

**MACD (Moving Average Convergence Divergence)**  
Un indicador de momentum que sigue tendencias mostrando la relación entre dos medias móviles de precios.

**MarketPulse**  
El proyecto de servidor MCP basado en Rust desarrollado en la Parte III de este libro, enfocado en datos de mercado de criptomonedas en tiempo real.

**MCP (Model Context Protocol)**  
Un protocolo abierto que permite comunicación entre aplicaciones LLM y fuentes de datos externas o herramientas.

**Middleware**  
Software que se sitúa entre un sistema operativo o base de datos y aplicaciones, proporcionando servicios como autenticación o logging.

**Migration (Database)**  
Un cambio versionado a un esquema de base de datos, permitiendo a los equipos evolucionar la estructura de la base de datos con el tiempo.

**MongoDB**  
Una base de datos de documentos NoSQL que almacena datos en documentos flexibles similares a JSON.

**Multi-Stage Build**  
Una característica de Docker que permite el uso de múltiples declaraciones FROM para crear imágenes finales más pequeñas y eficientes.

**MySQL**  
Un sistema de gestión de bases de datos relacionales de código abierto basado en SQL.

## N

**npm (Node Package Manager)**  
El gestor de paquetes predeterminado para Node.js, usado para instalar y gestionar paquetes JavaScript.

**NVMe (Non-Volatile Memory Express)**  
Un protocolo de almacenamiento de alto rendimiento para unidades de estado sólido, ofreciendo latencia significativamente menor que SATA.

## O

**OAuth 2.0**  
Un framework de autorización que permite a aplicaciones obtener acceso limitado a cuentas de usuario en servicios HTTP.

**OHLCV**  
Open, High, Low, Close, Volume - los cinco puntos de datos que componen una vela en gráficos financieros.

**ORM (Object-Relational Mapping)**  
Una técnica de programación para convertir datos entre sistemas de tipos incompatibles usando lenguajes de programación orientados a objetos.

**Overbought/Oversold**  
Condiciones de mercado donde el precio de un activo ha subido o caído excesivamente, sugiriendo una posible reversión.

## P

**Pagination**  
La práctica de dividir contenido en páginas discretas, mejorando el rendimiento y la experiencia del usuario con grandes conjuntos de datos.

**Parameterized Query**  
Una consulta de base de datos donde los parámetros se pasan separadamente del comando SQL, previniendo ataques de inyección SQL.

**pgcrypto**  
Una extensión de PostgreSQL que proporciona funciones criptográficas para cifrado, hashing y generación de datos aleatorios.

**PostgreSQL**  
Un potente sistema de base de datos objeto-relacional de código abierto con una sólida reputación de confiabilidad y robustez de características.

**Prompt (MCP)**  
Una plantilla predefinida en MCP que genera instrucciones estructuradas para LLMs, incluyendo contexto y parámetros.

**Protocol**  
Un conjunto de reglas que gobiernan el intercambio de datos entre sistemas. MCP define protocolos para comunicación LLM-herramienta.

## R

**r2d2**  
Una biblioteca de Rust que proporciona un pool de conexiones genérico para gestionar conexiones reutilizables a bases de datos u otros recursos.

**Rate Limiting**  
Una técnica para controlar la tasa de solicitudes que un usuario puede hacer a una API, previniendo abuso y asegurando distribución justa de recursos.

**RBAC (Role-Based Access Control)**  
Un método de control de acceso donde los permisos se asignan a roles, y los usuarios se asignan a roles.

**Redis**  
Un almacén de estructura de datos en memoria usado como base de datos, caché, broker de mensajes y motor de streaming.

**Resource (MCP)**  
Una pieza de datos expuesta por un servidor MCP que los LLMs pueden leer, identificada por un URI (ej., `market://btc/price`).

**REST (Representational State Transfer)**  
Un estilo arquitectónico para sistemas distribuidos, típicamente implementado sobre HTTP con métodos estándar (GET, POST, etc.).

**RSI (Relative Strength Index)**  
Un indicador de momentum que mide la velocidad y magnitud de cambios de precio, con rango de 0 a 100.

**Rust**  
Un lenguaje de programación de sistemas enfocado en seguridad, velocidad y concurrencia, usado para construir MarketPulse.

## S

**Schema (Database)**  
La estructura de una base de datos, incluyendo tablas, columnas, tipos de datos y relaciones.

**Schema (JSON)**  
Un vocabulario que permite anotar y validar documentos JSON.

**SDK (Software Development Kit)**  
Una colección de herramientas, bibliotecas y documentación para construir aplicaciones para una plataforma específica.

**Serde**  
Un framework de Rust para serializar y deserializar estructuras de datos de manera eficiente y genérica.

**SMA (Simple Moving Average)**  
Un indicador técnico calculado promediando precios durante un período específico, suavizando datos de precios.

**SQL (Structured Query Language)**  
Un lenguaje específico de dominio para gestionar y consultar bases de datos relacionales.

**SQL Injection**  
Una técnica de inyección de código que explota vulnerabilidades de seguridad en consultas de base de datos, permitiendo a atacantes ejecutar SQL malicioso.

**stdio (Standard Input/Output)**  
Un método de comunicación usando flujos de entrada y salida estándar, usado por MCP para comunicación de servidores locales.

**Stochastic Oscillator**  
Un indicador de momentum que compara un precio de cierre con su rango de precios durante un período, produciendo valores %K y %D.

## T

**Technical Analysis**  
Una disciplina de trading para evaluar inversiones analizando tendencias estadísticas de actividad de trading.

**TimescaleDB**  
Una base de datos de series temporales de código abierto construida sobre PostgreSQL, optimizada para cargas de trabajo de datos de series temporales.

**TLS (Transport Layer Security)**  
Un protocolo criptográfico que proporciona seguridad de comunicaciones sobre una red, el sucesor de SSL.

**Tokio**  
Un runtime asíncrono para Rust, proporcionando los bloques de construcción para escribir aplicaciones de red.

**Tool (MCP)**  
Una función expuesta por un servidor MCP que los LLMs pueden invocar para realizar acciones o recuperar información.

**TTL (Time To Live)**  
El período de tiempo durante el cual los datos deben estar en caché antes de considerarse obsoletos y actualizarse.

**TypeScript**  
Un superconjunto tipado de JavaScript que compila a JavaScript plano, proporcionando tipado estático opcional.

## U

**URI (Uniform Resource Identifier)**  
Una cadena que identifica un recurso, usado en MCP para identificar recursos (ej., `database://connector/table`).

**UUID (Universally Unique Identifier)**  
Un número de 128 bits usado para identificar información de manera única, a menudo formateado como 32 dígitos hexadecimales.

## V

**Validation**  
El proceso de verificar que los datos cumplan criterios especificados antes de procesarlos.

**Volume**  
El número de acciones o contratos negociados en un valor o mercado durante un período dado.

**Vulnerability**  
Una debilidad en un sistema que puede ser explotada para comprometer la seguridad.

## W

**WebSocket**  
Un protocolo de comunicación que proporciona canales de comunicación full-duplex sobre una única conexión TCP, usado para streaming de datos en tiempo real.

**WMA (Weighted Moving Average)**  
Una media móvil que asigna mayor peso a puntos de datos más recientes.

## X

**XSS (Cross-Site Scripting)**  
Una vulnerabilidad de seguridad que permite a atacantes inyectar scripts maliciosos en páginas web vistas por otros usuarios.

## Acrónimos y Abreviaciones

| Acrónimo | Forma Completa |
|---------|-----------|
| **API** | Application Programming Interface |
| **ATR** | Average True Range |
| **AWS** | Amazon Web Services |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **CORS** | Cross-Origin Resource Sharing |
| **CPU** | Central Processing Unit |
| **CRUD** | Create, Read, Update, Delete |
| **CSV** | Comma-Separated Values |
| **DoS** | Denial of Service |
| **ECS** | Elastic Container Service (AWS) |
| **EMA** | Exponential Moving Average |
| **ETL** | Extract, Transform, Load |
| **GDPR** | General Data Protection Regulation |
| **HTTP** | Hypertext Transfer Protocol |
| **HTTPS** | HTTP Secure |
| **JWT** | JSON Web Token |
| **LLM** | Large Language Model |
| **MACD** | Moving Average Convergence Divergence |
| **MCP** | Model Context Protocol |
| **NoSQL** | Not Only SQL |
| **npm** | Node Package Manager |
| **OHLCV** | Open, High, Low, Close, Volume |
| **ORM** | Object-Relational Mapping |
| **P50/P95/P99** | Percentil 50/95/99 |
| **RAM** | Random Access Memory |
| **RBAC** | Role-Based Access Control |
| **REST** | Representational State Transfer |
| **RSI** | Relative Strength Index |
| **SDK** | Software Development Kit |
| **SMA** | Simple Moving Average |
| **SQL** | Structured Query Language |
| **SSD** | Solid-State Drive |
| **SSL** | Secure Sockets Layer |
| **TLS** | Transport Layer Security |
| **TTL** | Time To Live |
| **URI** | Uniform Resource Identifier |
| **URL** | Uniform Resource Locator |
| **UUID** | Universally Unique Identifier |
| **WAF** | Web Application Firewall |
| **WMA** | Weighted Moving Average |
| **XSS** | Cross-Site Scripting |

## Conceptos Técnicos

### Asynchronous Programming
Un paradigma de programación donde las operaciones pueden ejecutarse concurrentemente sin bloquear el hilo de ejecución principal. Esencial para operaciones de I/O como solicitudes de red y consultas de base de datos.

### Blockchain
Una tecnología de libro mayor distribuido subyacente a las criptomonedas, que consiste en bloques que contienen datos de transacciones vinculados criptográficamente.

### Blue-Green Deployment
Una estrategia de implementación que usa dos entornos de producción idénticos (azul y verde), permitiendo implementaciones sin tiempo de inactividad al cambiar el tráfico entre ellos.

### Cache Invalidation
El proceso de eliminar datos obsoletos o desactualizados de una caché para asegurar que se obtengan datos frescos.

### Circuit Breaker
Un patrón de diseño que previene fallos en cascada deteniendo temporalmente las solicitudes a un servicio que está fallando.

### Cold Start
La latencia aumentada cuando una función o contenedor inicia por primera vez después de estar inactivo.

### Containerization
La práctica de empaquetar software con sus dependencias en unidades estandarizadas (contenedores) para implementación consistente.

### Database Replication
El proceso de copiar datos de una base de datos primaria a una o más bases de datos réplica para redundancia y escalado de lectura.

### Exponential Backoff
Una estrategia de reintento donde el tiempo de espera entre reintentos aumenta exponencialmente, previniendo sobrecarga del sistema.

### Graceful Degradation
Un enfoque de diseño donde un sistema continúa operando con funcionalidad reducida cuando los componentes fallan.

### Hot Reload
Una característica de desarrollo que actualiza el código en ejecución sin reiniciar la aplicación, preservando el estado.

### Immutability
Una propiedad donde los datos no pueden ser modificados después de su creación, requiriendo nuevas instancias para cambios. Común en programación funcional.

### Lazy Loading
Un patrón de diseño que difiere la inicialización de objetos hasta que se necesita, mejorando el rendimiento y el uso de memoria.

### Microservices
Un estilo arquitectónico que estructura aplicaciones como colecciones de servicios débilmente acoplados.

### Mutex (Mutual Exclusion)
Una primitiva de sincronización que previene que múltiples hilos accedan a datos compartidos simultáneamente.

### Observability
La capacidad de entender el estado interno de un sistema desde sus salidas externas (logs, métricas, trazas).

### Polling
Verificar repetidamente un recurso o servicio para actualizaciones a intervalos regulares.

### Reactive Programming
Un paradigma de programación enfocado en flujos de datos y la propagación del cambio.

### Saga Pattern
Un patrón de diseño para gestionar transacciones distribuidas a través de microservicios usando transacciones compensatorias.

### Sharding
Una técnica de particionamiento de base de datos que distribuye datos horizontalmente a través de múltiples máquinas.

### State Management
El proceso de gestionar el estado de la aplicación (datos que cambian con el tiempo) de manera predecible.

### Throttling
Limitar la tasa de operaciones para prevenir sobrecarga de un sistema o mantenerse dentro de cuotas.

### Versioning (API)
La práctica de gestionar cambios en APIs mientras se mantiene compatibilidad hacia atrás.

## Términos Específicos de MCP

### Capability
Una característica anunciada por un cliente o servidor MCP durante la inicialización (ej., tools, resources, prompts).

### Initialized Notification
Una notificación enviada por el cliente MCP después de procesar exitosamente la respuesta de inicialización del servidor.

### JSON-RPC 2.0
El protocolo de llamada a procedimiento remoto usado como fundamento para la comunicación MCP.

### Method
Una operación específica en el protocolo MCP (ej., `tools/list`, `tools/call`, `resources/read`).

### MCP Server
Un programa que implementa el protocolo MCP para exponer herramientas, recursos y prompts a clientes LLM.

### MCP Client
Una aplicación (como Claude Desktop) que se conecta a servidores MCP para acceder a sus capacidades.

### Progress Token
Un identificador usado para rastrear el progreso de operaciones MCP de larga duración.

### Protocol Version
La versión de la especificación MCP (ej., "2024-11-05") negociada durante la inicialización.

### Subscription
Un mecanismo que permite a los clientes recibir notificaciones cuando un recurso cambia.

## Términos de Datos de Mercado

### Ask Price
El precio más bajo que un vendedor está dispuesto a aceptar por un activo.

### Bid Price
El precio más alto que un comprador está dispuesto a pagar por un activo.

### Bid-Ask Spread
La diferencia entre los precios bid y ask, representando la liquidez del mercado.

### Bull/Bear Market
Un mercado alcista (bull) tiene precios en aumento; un mercado bajista (bear) tiene precios en caída.

### Liquidity
La facilidad con la que un activo puede ser comprado o vendido sin afectar su precio.

### Market Cap (Market Capitalization)
El valor total de una criptomoneda calculado multiplicando el precio por el suministro circulante.

### Order Book
Una lista de órdenes de compra y venta para un activo, organizada por nivel de precio.

### Tick
El movimiento de precio más pequeño posible en un instrumento de trading.

### Trading Pair
Dos activos que pueden intercambiarse entre sí (ej., BTC/USD, ETH/BTC).

### Volatility
El grado de variación en los precios de trading a lo largo del tiempo, midiendo la inestabilidad del mercado.

---

*Este glosario cubre términos utilizados a lo largo de Building MCP Servers (Edición 2024). Para la especificación MCP más actual, visite [modelcontextprotocol.io](https://modelcontextprotocol.io).*
