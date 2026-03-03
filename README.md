# User Management Service

A robust user authentication and management service built with FastAPI. Provides comprehensive user account management including traditional authentication, OAuth integration (Google & GitHub), and complete CRUD operations.

## 🎯 Overview

This FastAPI-based service provides a complete user management solution for modern web applications. It supports multiple authentication methods, secure password handling, and flexible account management capabilities.

### Key Features

- **🔐 Authentication**: Traditional username/password and OAuth (Google, GitHub)
- **👤 User Management**: Complete CRUD operations for user accounts
- **🔒 Password Security**: Bcrypt-based password hashing with complexity requirements
- **📧 Email Validation**: Built-in email validation and uniqueness checks
- **🚦 Account Status**: Support for active, suspended, and deleted states
- **🔑 JWT Tokens**: Secure token-based authentication for API access
- **🔍 Search**: Filter and search users by username, email, or status
- **📄 API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📋 API Endpoints

### Authentication
- `POST /api/users/register` - Register new user account
- `POST /api/users/login` - Traditional login with username/password
- `POST /api/users/oauth/login` - OAuth login (Google/GitHub)
- `POST /api/users/oauth/github/callback` - GitHub OAuth callback handler

### User CRUD
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/username/{username}` - Get user by username
- `GET /api/users/email/{email}` - Get user by email
- `GET /api/users/` - List all users (with pagination and filtering)
- `PUT /api/users/{user_id}` - Update user information
- `DELETE /api/users/{user_id}` - Delete user (soft or hard delete)

### Account Management
- `POST /api/users/{user_id}/change-password` - Change user password
- `POST /api/users/{user_id}/suspend` - Suspend user account
- `POST /api/users/{user_id}/activate` - Activate suspended account

### Health Checks
- `GET /` - Basic health check
- `GET /health` - Detailed health check with component status

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────┐
│           API Layer (FastAPI)               │
│  - User Routes                              │
│  - Request/Response DTOs                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Service Layer                       │
│  - User Service                             │
│  - Authentication Logic                     │
│  - Password Management                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Repository Layer                       │
│  - User Repository                          │
│  - Database Operations                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Database Layer (PostgreSQL)            │
│  - SQLAlchemy ORM Models                    │
└─────────────────────────────────────────────┘
```

### Project Structure

```
user-management-service/
├── app/
│   ├── api/                    # API route handlers
│   │   └── user_routes.py     # User management endpoints
│   ├── core/                   # Core configuration & utilities
│   │   ├── config.py          # Environment configuration
│   │   ├── database.py        # Database connection
│   │   ├── jwt_utils.py       # JWT token utilities
│   │   ├── db_init.py         # Database initialization
│   │   └── logging_config.py  # Logging setup
│   ├── models/                # SQLAlchemy ORM models
│   │   └── user.py            # User model
│   ├── repositories/          # Data access layer
│   │   └── user_repo.py       # User repository
│   ├── schemas/               # Pydantic DTOs
│   │   └── user_dto.py        # User request/response schemas
│   ├── services/              # Business logic layer
│   │   └── user_service.py    # User service
│   └── main.py                # FastAPI application entry point
├── docker-compose.yml         # Docker compose configuration
├── Dockerfile                 # Container image definition
├── requirements.txt           # Python dependencies
_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# OAuth Configuration (Optional)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Application Settings
APP_NAME=User Management Service
ENVIRONMENT=development
DEBUG=False
LOG_LEVEL=INFO
```

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd user-management-service
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   createdb userdb
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

6. **Access API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Usage Examples

### Register a New User

```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login with Credentials

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### Get User Details

```bash
curl -X GET "http://localhost:8000/api/users/{user_id}" \
  -H "Authorization: Bearer {your-jwt-token}"
```

### Update User Information

```bash
curl -X PUT "http://localhost:8000/api/users/{user_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {your-jwt-token}" \
  -d '{
    "email": "newemail@example.com",
    "name": "John Doe"
  }'
```

### Change Password

```bash
curl -X POST "http://localhost:8000/api/users/{user_id}/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {your-jwt-token}" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!"
  }'
```

### List Users with Pagination

```bash
curl -X GET "http://localhost:8000/api/users/?skip=0&limit=10&status=active" \
  -H "Authorization: Bearer {your-jwt-token}"
```

### Search Users

```bash
curl -X GET "http://localhost:8000/api/users/?search=john" \
  -H "Authorization: Bearer {your-jwt-token}"
```

## 🔐 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Bcrypt hashing with salt

### OAuth Support
- **Google OAuth 2.0**: Sign in with Google accounts
- **GitHub OAuth**: Sign in with GitHub accounts
- Automatic account creation for new OAuth users
- Profile picture and name sync from OAuth providers

### JWT Authentication
- Secure token-based authentication
- Configurable expiration time
- Token refresh capability
- Protected endpoints with bearer token validation

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.110.0
- **Server**: Uvicorn 0.27.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.27 ORM
- **Async Database**: AsyncPG 0.29.0
- **Validation**: Pydantic 2.5.0
- **Authentication**: JWT (PyJWT 2.8.0) + OAuth
- **Password Hashing**: bcrypt 4.1.2
- **HTTP Client**: httpx 0.27.0 (for OAuth)
- **Email Validation**: email-validator 2.1.0

## 📊 Database Schema

### User Table

| Column | Type | Description |
|--------|------|-------------|
| user_id | VARCHAR(36) | Primary key (UUID) |
| username | VARCHAR(50) | Unique username |
| email | VARCHAR(255) | Unique email address |
| password_hash | VARCHAR(255) | Bcrypt hashed password |
| name | VARCHAR(255) | Full name (optional) |
| picture | VARCHAR(500) | Profile picture URL |
| provider | VARCHAR(50) | OAuth provider (google, github) |
| provider_id | VARCHAR(255) | OAuth provider user ID |
| created_at | TIMESTAMP | Account creation time |
| last_active_at | TIMESTAMP | Last activity time |
| last_login | TIMESTAMP | Last login time |
| status | ENUM | active, suspended, deleted |

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
```

## 📝 Configuration

Key configuration options in `app/core/config.py`:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `JWT_ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- OAuth client credentials for Google and GitHub

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use strong, unique values for all secrets
2. **Database**: Use managed PostgreSQL service with regular backups
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Monitoring**: Set up logging and monitoring solutions
6. **Scaling**: Use load balancer for horizontal scaling

### Health Checks

- `GET /`: Basic health check returns service status
- `GET /health`: Detailed health check with component status

## 📖 API Documentation

Once the service is running, comprehensive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[Your License Here]

## 📧 Contact

[Your Contact Information]
- **cold_start_matching_factor** - Weights for cold-start mode

## 📝 License

This project is part of a research initiative at SLIIT (Sri Lanka Institute of Information Technology).

## 📧 Contact

For questions or support, please contact the development team.

## 🙏 Acknowledgments

- Built with FastAPI for high-performance async capabilities
- PostgreSQL for robust relational data management
- SQLAlchemy for elegant ORM abstractions
- Research conducted at SLIIT

---

**Note**: This is a research project focused on adaptive user profiling in AI/LLM applications. The service is designed for integration with conversational AI systems to provide personalized user experiences based on behavioral analysis.
