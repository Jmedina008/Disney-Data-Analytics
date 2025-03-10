# Disney Portfolio MCP Server 🔐

Microservice Control Panel (MCP) server for managing API keys and external service integrations for the Disney-themed data science portfolio.

## Features

### API Key Management 🗝️
- Secure storage of API keys
- Automatic key rotation
- Usage monitoring
- Rate limit tracking

### Supported Services
1. TMDB API (Disney+ Content)
   - Movie and TV show data
   - Streaming availability
   - Content metadata

2. Weather API (Theme Parks)
   - Historical weather data
   - Forecasts
   - Location-specific conditions

3. Disney Parks API
   - Wait times
   - Attraction status
   - Park hours

### Security Features
- Environment-based configuration
- Encrypted storage
- Access logging
- Rate limiting
- IP whitelisting

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Docker
- JWT Authentication
- Python-Jose (for encryption)

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

6. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

### Authentication
```
POST /auth/token
GET /auth/verify
```

### API Keys
```
GET /api/keys/{service_name}
POST /api/keys/register
PUT /api/keys/rotate
DELETE /api/keys/{key_id}
```

### Monitoring
```
GET /monitor/usage
GET /monitor/limits
GET /monitor/health
```

## Directory Structure
```
mcp_server/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
├── scripts/
├── tests/
├── .env.example
├── requirements.txt
└── docker-compose.yml
```

## Security Considerations
- All API keys are encrypted at rest
- Access tokens are required for all operations
- Regular key rotation is enforced
- All actions are logged and monitored

## Contributing
1. Create a feature branch
2. Make your changes
3. Submit a pull request

## Contact
- GitHub: [@Jmedina008](https://github.com/Jmedina008) 