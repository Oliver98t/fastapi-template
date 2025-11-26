# FastAPI Template

A production-ready FastAPI template with authentication, role-based access control, database migrations, and comprehensive API endpoints.

## 🚀 Features

- **FastAPI** - Modern, fast web framework with automatic OpenAPI documentation
- **JWT Authentication** - Secure token-based authentication with role-based access control
- **SQLModel + SQLAlchemy** - Type-safe database operations with Pydantic integration
- **Alembic** - Database migration management
- **PostgreSQL** - Production-ready database with Docker support
- **Role-Based Access Control** - Admin, Read-Write, and Read-Only privilege levels
- **Docker Ready** - Complete containerization with docker-compose
- **Comprehensive Testing** - Pytest integration with test client
- **Admin Tools** - Interactive user creation scripts
- **MIT Licensed** - Fully open source with proper documentation

## 📋 Prerequisites

- **Python 3.11+** (recommended)
- **PostgreSQL** (or use Docker Compose)
- **Docker & Docker Compose** (optional but recommended)

## 🛠️ Quick Setup

### Option 1: Using Setup Script (Recommended)

```bash
# Clone the repository
git clone https://github.com/Oliver98t/fastapi-template.git
cd fastapi

# Run setup script to copy environment file and create directories
source setup.sh

# Edit environment variables
nano .env  # or use your preferred editor
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/Oliver98t/fastapi-template.git
cd fastapi

# Copy environment template
cp example.env .env

# Create alembic versions directory
mkdir -p app/alembic/versions
```

## 🐳 Running with Docker Compose (Recommended)

```bash
# Start all services (API + PostgreSQL)
docker compose up --build

# In a new terminal, run database migrations
docker compose exec fastapi_example_backend alembic upgrade head

# Create an admin user (optional)
docker compose exec fastapi_example_backend python admin/create_user.py
```

The API will be available at `http://localhost:8000`

## 💻 Local Development Setup

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

Edit your `.env` file with your database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
SECRET=your-secret-key-here
```

### 3. Database Setup
# 
update "sqlalchemy.url" in the alembic.ini file if you have changed variables in the .env file

```bash
# Navigate to app directory (where alembic.ini is located)
cd app

# Run migrations
alembic upgrade head

# Go back to project root
cd ..
```

### 4. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔐 Authentication & User Management

### User Privilege Levels

- **Admin (0)**: Full access to all endpoints
- **Read-Write (1)**: Access to read and modify items
- **Read-Only (2)**: Access to read items only

### Creating Users

#### Option 1: Using Admin Script (Interactive)

```bash
# Local development
python app/admin/create_user.py

# With Docker
docker compose exec fastapi_example_backend python admin/create_user.py
```

#### Option 2: Using API Endpoints

1. First, create an admin user using the script above
2. Login to get a token
3. Use the `/users/` endpoint with admin token to create more users

### Authentication Flow

1. **Login**: POST to `/users/token` with username/password
2. **Get Token**: Receive JWT access token
3. **Use Token**: Include in Authorization header: `Bearer <token>`

Example:
```bash
# Login
curl -X POST "http://localhost:8000/users/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"

# Use token for authenticated requests
curl -X GET "http://localhost:8000/items/" \
  -H "Authorization: Bearer <your-token>"
```

## 📚 API Endpoints

### Public Endpoints
- `GET /` - Health check
- `POST /users/token` - User authentication

### User Management (Admin Only)
- `GET /users/` - List all users
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user (full)
- `PATCH /users/{user_id}` - Update user (partial)
- `DELETE /users/{user_id}` - Delete user

### Item Management (Read-Write Access)
- `GET /items/` - List all items (with pagination)
- `POST /items/` - Create new item
- `GET /items/{item_id}` - Get item details
- `PUT /items/{item_id}` - Update item (full)
- `PATCH /items/{item_id}` - Update item (partial)
- `DELETE /items/{item_id}` - Delete item

### Protected Routes
- `GET /protected` - Test authentication (Read-Write access)

## 📖 API Documentation

Once the server is running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Management

### Migrations with Alembic

```bash
# Create a new migration
cd app
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

### Docker Environment

```bash
# Create migration in Docker
docker compose exec fastapi_example_backend alembic revision --autogenerate -m "Description"

# Apply migrations in Docker
docker compose exec fastapi_example_backend alembic upgrade head
```

## 🧪 Testing

Run the test suite:

```bash
# Local testing
pytest

# With coverage
pytest --cov=app

# Docker testing
docker compose exec fastapi_example_backend pytest
```

## 📁 Project Structure

```
fastapi/
├── app/                          # Main application package
│   ├── admin/                    # Admin tools and scripts
│   │   └── create_user.py       # Interactive user creation
│   ├── alembic/                 # Database migrations
│   │   ├── versions/            # Migration files
│   │   └── env.py              # Alembic environment config
│   ├── auth/                    # Authentication utilities
│   │   └── encrypt.py          # JWT, hashing, auth dependencies
│   ├── database/                # Database layer
│   │   ├── base_schemas.py     # User models and enums
│   │   ├── schemas.py          # Custom models (items)
│   │   ├── base_orm.py         # Base CRUD operations
│   │   ├── orm.py              # Model-specific ORMs
│   │   └── connection.py       # Database connection setup
│   ├── routers/                 # API route handlers
│   │   ├── base_routers.py     # Generic CRUD router + UserRouter
│   │   └── routers.py          # Custom routers (items)
│   ├── main.py                  # FastAPI application entry point
│   ├── api_test.py             # API tests
│   └── alembic.ini             # Alembic configuration
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # Application container config
├── requirements.txt             # Python dependencies
├── example.env                  # Environment template
├── setup.sh                    # Quick setup script
├── pytest.ini                  # Pytest configuration
└── README.md                   # This documentation
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | 5432 |
| `DB_USER` | Database username | - |
| `DB_PASSWORD` | Database password | - |
| `DB_NAME` | Database name | - |
| `SECRET` | JWT secret key | - |
| `API_HOST` | API server host | 0.0.0.0 |
| `API_PORT` | API server port | 8000 |
| `NODE_ENV` | Environment | development |

### JWT Configuration

JWT tokens expire after 30 minutes by default. Modify `ACCESS_TOKEN_EXPIRE_MINUTES` in `app/auth/encrypt.py` to change this.

## 🔧 Development

### Adding New Models

1. Create model in `app/database/schemas.py`
2. Create ORM class in `app/database/orm.py`
3. Create router in `app/routers/routers.py`
4. Add router to `app/main.py`
5. Generate migration: `alembic revision --autogenerate`

### Custom Authentication

Extend the authentication system by:
- Adding new privilege levels in `UserPrivilege` enum
- Creating new auth dependency functions in `auth/encrypt.py`
- Using them in your route decorators

## 🐛 Troubleshooting

### Common Issues

1. **Migration errors**: Ensure database is running and accessible
2. **Permission denied**: Check user privileges match endpoint requirements
3. **Token errors**: Verify `SECRET` key is set and consistent
4. **Import errors**: Make sure you're running from the correct directory

### Docker Issues

```bash
# Rebuild containers
docker compose down
docker compose up --build

# View logs
docker compose logs fastapi_example_backend
docker compose logs fastapi_example_db

# Connect to database
docker compose exec fastapi_example_db psql -U oli98 -d postgres
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the source code headers for details.

## 👨‍💻 Author

**Oliver Tattersfield** - [Oliver98t](https://github.com/Oliver98t)

---

🌟 If this template helps you, please give it a star!
