# Appendix F: Glossary of Terms

This glossary defines key terms, acronyms, and concepts used throughout the book.

## A

**Aggregation**  
The process of combining multiple data points into summary statistics (sum, average, count, etc.). In SQL, performed using GROUP BY with aggregate functions.

**API (Application Programming Interface)**  
A set of rules and protocols that allow different software applications to communicate. In this book, refers to database APIs and the MCP protocol API.

**API Key**  
A unique identifier used to authenticate requests to an API. Should be kept secret and rotated regularly.

**Async/Await**  
A programming pattern for handling asynchronous operations in a synchronous-looking manner. Widely used in JavaScript/TypeScript and Rust.

**ATR (Average True Range)**  
A technical indicator that measures market volatility by calculating the average range between high and low prices over a period.

**Authentication**  
The process of verifying the identity of a user or system. Common methods include passwords, API keys, and OAuth tokens.

**Authorization**  
The process of determining whether an authenticated user has permission to perform a specific action or access a resource.

## B

**Bcrypt**  
A password hashing algorithm designed to be slow and resistant to brute-force attacks. Uses a work factor to control computation time.

**Binance**  
A major cryptocurrency exchange. MarketPulse uses Binance's WebSocket API for real-time market data.

**Bollinger Bands**  
A technical indicator consisting of a moving average with upper and lower bands representing standard deviations, used to identify overbought/oversold conditions.

**Broadcast Channel**  
A communication pattern where messages are sent to multiple subscribers simultaneously. Used in MarketPulse for distributing price updates.

**Buffer**  
A temporary storage area for data, typically used when data is being transferred between processes or across networks.

## C

**Cache**  
A high-speed storage layer that stores frequently accessed data to reduce latency. Redis is commonly used as a distributed cache.

**Candlestick / OHLCV**  
A price chart format showing Open, High, Low, Close prices and Volume for a time period. Used in financial market analysis.

**CI/CD (Continuous Integration / Continuous Deployment)**  
A software development practice involving automated building, testing, and deployment of code changes.

**Claude Desktop**  
Anthropic's desktop application for Claude AI that supports MCP servers, allowing users to extend Claude's capabilities.

**Connection Pool**  
A cache of database connections maintained for reuse, improving performance by avoiding the overhead of creating new connections.

**CORS (Cross-Origin Resource Sharing)**  
A security mechanism that allows or restricts resources on a web server to be requested from another domain.

**Crate**  
The Rust term for a package or library. Distributed via crates.io, the Rust package registry.

**Cryptocurrency**  
A digital or virtual currency secured by cryptography. Examples: Bitcoin (BTC), Ethereum (ETH), Solana (SOL).

**CSV (Comma-Separated Values)**  
A simple file format for tabular data where values are separated by commas. Commonly used for data export.

## D

**DataBridge**  
The TypeScript-based MCP server project developed in Part II of this book, focused on enterprise data integration.

**Database Connector**  
A configuration that defines how to connect to a specific database instance, including host, credentials, and connection parameters.

**Diesel**  
A safe, extensible ORM and query builder for Rust. Used in MarketPulse for database operations.

**Docker**  
A platform for developing, shipping, and running applications in containers, providing consistent environments across development and production.

**Docker Compose**  
A tool for defining and running multi-container Docker applications using a YAML configuration file.

## E

**ECS (Elastic Container Service)**  
AWS service for running Docker containers in production at scale, with support for Fargate (serverless) and EC2 deployments.

**EMA (Exponential Moving Average)**  
A technical indicator that gives more weight to recent prices, making it more responsive to price changes than a simple moving average.

**Environment Variable**  
A dynamic value that affects how processes run on a computer. Used to configure applications without hardcoding values.

**ETL (Extract, Transform, Load)**  
A data integration process for extracting data from sources, transforming it, and loading it into a destination system.

## F

**Fargate**  
AWS serverless compute engine for containers, eliminating the need to provision and manage servers.

**Foreign Key**  
A database constraint that establishes a relationship between two tables, ensuring referential integrity.

## G

**GitHub Actions**  
A CI/CD platform integrated with GitHub that automates workflows like testing, building, and deployment.

**Graceful Shutdown**  
The process of cleanly stopping a server by completing in-progress requests and closing connections before terminating.

## H

**Hypertable**  
A TimescaleDB feature that partitions time-series data into chunks for improved query performance and data management.

**HTTPS (HTTP Secure)**  
An extension of HTTP using TLS/SSL encryption to secure communication over a network.

## I

**Idempotent**  
An operation that produces the same result regardless of how many times it's executed. Important for reliable distributed systems.

**Index (Database)**  
A data structure that improves the speed of data retrieval operations on a database table at the cost of additional storage and write performance.

**Indicator (Technical)**  
A mathematical calculation based on price and/or volume data used to analyze market trends and make trading decisions.

**Input Schema**  
A JSON Schema definition that specifies the structure, types, and validation rules for tool inputs in MCP.

## J

**JSON (JavaScript Object Notation)**  
A lightweight data interchange format that's easy for humans to read and write and easy for machines to parse and generate.

**JSON-RPC**  
A remote procedure call protocol encoded in JSON. MCP uses JSON-RPC 2.0 as its base protocol.

**JWT (JSON Web Token)**  
A compact, URL-safe means of representing claims between two parties, commonly used for authentication and authorization.

## K

**Kubernetes (K8s)**  
An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

## L

**Latency**  
The time delay between a request and its response. Lower latency means faster system response times.

**LLM (Large Language Model)**  
An AI model trained on vast amounts of text data, capable of understanding and generating human-like text. Examples: Claude, GPT-4.

**Load Balancer**  
A device or service that distributes network traffic across multiple servers to ensure no single server is overwhelmed.

## M

**MACD (Moving Average Convergence Divergence)**  
A trend-following momentum indicator showing the relationship between two moving averages of prices.

**MarketPulse**  
The Rust-based MCP server project developed in Part III of this book, focused on real-time cryptocurrency market data.

**MCP (Model Context Protocol)**  
An open protocol enabling communication between LLM applications and external data sources or tools.

**Middleware**  
Software that sits between an operating system or database and applications, providing services like authentication or logging.

**Migration (Database)**  
A version-controlled change to a database schema, allowing teams to evolve the database structure over time.

**MongoDB**  
A NoSQL document database that stores data in flexible, JSON-like documents.

**Multi-Stage Build**  
A Docker feature allowing the use of multiple FROM statements to create smaller, more efficient final images.

**MySQL**  
An open-source relational database management system based on SQL.

## N

**npm (Node Package Manager)**  
The default package manager for Node.js, used to install and manage JavaScript packages.

**NVMe (Non-Volatile Memory Express)**  
A high-performance storage protocol for solid-state drives, offering significantly lower latency than SATA.

## O

**OAuth 2.0**  
An authorization framework enabling applications to obtain limited access to user accounts on HTTP services.

**OHLCV**  
Open, High, Low, Close, Volume - the five data points that make up a candlestick in financial charts.

**ORM (Object-Relational Mapping)**  
A programming technique for converting data between incompatible type systems using object-oriented programming languages.

**Overbought/Oversold**  
Market conditions where an asset's price has risen or fallen excessively, suggesting a potential reversal.

## P

**Pagination**  
The practice of dividing content into discrete pages, improving performance and user experience with large datasets.

**Parameterized Query**  
A database query where parameters are passed separately from the SQL command, preventing SQL injection attacks.

**pgcrypto**  
A PostgreSQL extension providing cryptographic functions for encryption, hashing, and random data generation.

**PostgreSQL**  
A powerful, open-source object-relational database system with a strong reputation for reliability and feature robustness.

**Prompt (MCP)**  
A pre-defined template in MCP that generates structured instructions for LLMs, including context and parameters.

**Protocol**  
A set of rules governing the exchange of data between systems. MCP defines protocols for LLM-tool communication.

## R

**r2d2**  
A Rust library providing a generic connection pool for managing reusable connections to databases or other resources.

**Rate Limiting**  
A technique for controlling the rate of requests a user can make to an API, preventing abuse and ensuring fair resource distribution.

**RBAC (Role-Based Access Control)**  
An access control method where permissions are assigned to roles, and users are assigned to roles.

**Redis**  
An in-memory data structure store used as a database, cache, message broker, and streaming engine.

**Resource (MCP)**  
A piece of data exposed by an MCP server that LLMs can read, identified by a URI (e.g., `market://btc/price`).

**REST (Representational State Transfer)**  
An architectural style for distributed systems, typically implemented over HTTP with standard methods (GET, POST, etc.).

**RSI (Relative Strength Index)**  
A momentum indicator measuring the speed and magnitude of price changes, ranging from 0 to 100.

**Rust**  
A systems programming language focused on safety, speed, and concurrency, used to build MarketPulse.

## S

**Schema (Database)**  
The structure of a database, including tables, columns, data types, and relationships.

**Schema (JSON)**  
A vocabulary that allows you to annotate and validate JSON documents.

**SDK (Software Development Kit)**  
A collection of tools, libraries, and documentation for building applications for a specific platform.

**Serde**  
A Rust framework for serializing and deserializing data structures efficiently and generically.

**SMA (Simple Moving Average)**  
A technical indicator calculated by averaging prices over a specified period, smoothing out price data.

**SQL (Structured Query Language)**  
A domain-specific language for managing and querying relational databases.

**SQL Injection**  
A code injection technique exploiting security vulnerabilities in database queries, allowing attackers to execute malicious SQL.

**stdio (Standard Input/Output)**  
A communication method using standard input and output streams, used by MCP for local server communication.

**Stochastic Oscillator**  
A momentum indicator comparing a closing price to its price range over a period, producing %K and %D values.

## T

**Technical Analysis**  
A trading discipline for evaluating investments by analyzing statistical trends from trading activity.

**TimescaleDB**  
An open-source time-series database built on PostgreSQL, optimized for time-series data workloads.

**TLS (Transport Layer Security)**  
A cryptographic protocol providing communications security over a network, the successor to SSL.

**Tokio**  
An asynchronous runtime for Rust, providing the building blocks for writing network applications.

**Tool (MCP)**  
A function exposed by an MCP server that LLMs can invoke to perform actions or retrieve information.

**TTL (Time To Live)**  
The time period for which data should be cached before being considered stale and refreshed.

**TypeScript**  
A typed superset of JavaScript that compiles to plain JavaScript, providing optional static typing.

## U

**URI (Uniform Resource Identifier)**  
A string identifying a resource, used in MCP to identify resources (e.g., `database://connector/table`).

**UUID (Universally Unique Identifier)**  
A 128-bit number used to uniquely identify information, often formatted as 32 hexadecimal digits.

## V

**Validation**  
The process of checking that data meets specified criteria before processing.

**Volume**  
The number of shares or contracts traded in a security or market during a given period.

**Vulnerability**  
A weakness in a system that can be exploited to compromise security.

## W

**WebSocket**  
A communication protocol providing full-duplex communication channels over a single TCP connection, used for real-time data streaming.

**WMA (Weighted Moving Average)**  
A moving average that assigns greater weight to more recent data points.

## X

**XSS (Cross-Site Scripting)**  
A security vulnerability allowing attackers to inject malicious scripts into web pages viewed by other users.

## Acronyms & Abbreviations

| Acronym | Full Form |
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
| **P50/P95/P99** | 50th/95th/99th Percentile |
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

## Technical Concepts

### Asynchronous Programming
A programming paradigm where operations can run concurrently without blocking the main execution thread. Essential for I/O-bound operations like network requests and database queries.

### Blockchain
A distributed ledger technology underlying cryptocurrencies, consisting of blocks containing transaction data linked cryptographically.

### Blue-Green Deployment
A deployment strategy using two identical production environments (blue and green), allowing zero-downtime deployments by switching traffic between them.

### Cache Invalidation
The process of removing stale or outdated data from a cache to ensure fresh data is fetched.

### Circuit Breaker
A design pattern that prevents cascading failures by stopping requests to a failing service temporarily.

### Cold Start
The increased latency when a function or container starts for the first time after being idle.

### Containerization
The practice of packaging software with its dependencies into standardized units (containers) for consistent deployment.

### Database Replication
The process of copying data from a primary database to one or more replica databases for redundancy and read scaling.

### Exponential Backoff
A retry strategy where wait time between retries increases exponentially, preventing system overload.

### Graceful Degradation
A design approach where a system continues operating with reduced functionality when components fail.

### Hot Reload
A development feature that updates running code without restarting the application, preserving state.

### Immutability
A property where data cannot be modified after creation, requiring new instances for changes. Common in functional programming.

### Lazy Loading
A design pattern that defers object initialization until needed, improving performance and memory usage.

### Microservices
An architectural style structuring applications as collections of loosely coupled services.

### Mutex (Mutual Exclusion)
A synchronization primitive preventing multiple threads from accessing shared data simultaneously.

### Observability
The ability to understand a system's internal state from its external outputs (logs, metrics, traces).

### Polling
Repeatedly checking a resource or service for updates at regular intervals.

### Reactive Programming
A programming paradigm focused on data streams and the propagation of change.

### Saga Pattern
A design pattern for managing distributed transactions across microservices using compensating transactions.

### Sharding
A database partitioning technique distributing data across multiple machines horizontally.

### State Management
The process of managing application state (data that changes over time) in a predictable way.

### Throttling
Limiting the rate of operations to prevent overwhelming a system or staying within quotas.

### Versioning (API)**
The practice of managing changes to APIs while maintaining backward compatibility.

## MCP-Specific Terms

### Capability
A feature advertised by an MCP client or server during initialization (e.g., tools, resources, prompts).

### Initialized Notification
A notification sent by the MCP client after successfully processing the server's initialize response.

### JSON-RPC 2.0
The remote procedure call protocol used as the foundation for MCP communication.

### Method
A specific operation in the MCP protocol (e.g., `tools/list`, `tools/call`, `resources/read`).

### MCP Server
A program implementing the MCP protocol to expose tools, resources, and prompts to LLM clients.

### MCP Client
An application (like Claude Desktop) that connects to MCP servers to access their capabilities.

### Progress Token
An identifier used to track progress of long-running MCP operations.

### Protocol Version
The version of the MCP specification (e.g., "2024-11-05") negotiated during initialization.

### Subscription
A mechanism allowing clients to receive notifications when a resource changes.

## Market Data Terms

### Ask Price
The lowest price a seller is willing to accept for an asset.

### Bid Price
The highest price a buyer is willing to pay for an asset.

### Bid-Ask Spread
The difference between the bid and ask prices, representing market liquidity.

### Bull/Bear Market
A bull market has rising prices; a bear market has falling prices.

### Liquidity
The ease with which an asset can be bought or sold without affecting its price.

### Market Cap (Market Capitalization)
The total value of a cryptocurrency calculated by multiplying price by circulating supply.

### Order Book
A list of buy and sell orders for an asset, organized by price level.

### Tick
The smallest possible price movement in a trading instrument.

### Trading Pair
Two assets that can be exchanged for each other (e.g., BTC/USD, ETH/BTC).

### Volatility
The degree of variation in trading prices over time, measuring market instability.

---

*This glossary covers terms used throughout Building MCP Servers (2024 Edition). For the most current MCP specification, visit [modelcontextprotocol.io](https://modelcontextprotocol.io).*
