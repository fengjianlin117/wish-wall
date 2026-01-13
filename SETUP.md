# Wish Wall - Setup Guide

**Last Updated:** 2026-01-13 13:36:30 UTC

## Overview

Wish Wall is a full-stack web application built with Docker. This guide will help you set up and run the application locally.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)
- Git
- Node.js 18+ (for local frontend development, optional)
- Python 3.11+ (for local backend development, optional)

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/fengjianlin117/wish-wall.git
cd wish-wall
```

### 2. Configure Environment Variables

Update the `backend/.env` file with your configuration:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and update:
- `SECRET_KEY`: Generate a secure key
- `DB_PASSWORD`: Set a strong database password
- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`: For email functionality
- `CORS_ALLOWED_ORIGINS`: Update frontend URL

### 3. Start the Application

```bash
docker-compose up -d
```

This will start:
- **Frontend** (Nginx): http://localhost:80
- **Backend** (Django/Gunicorn): http://localhost:8000
- **PostgreSQL Database**: localhost:5432
- **Redis Cache**: localhost:6379

### 4. Initialize the Database

The `start.sh` script runs migrations automatically, but you can also run them manually:

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Create a Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

Access the admin panel at: http://localhost:8000/admin

## Development Setup (Local)

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

The backend will run on http://localhost:8000

## Docker Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v
```

### Rebuild Images

```bash
docker-compose up -d --build
```

### Access Services

```bash
# Backend shell
docker-compose exec backend bash

# Database shell
docker-compose exec postgres psql -U postgres -d wish_wall_db

# Frontend shell
docker-compose exec frontend bash
```

## Project Structure

```
wish-wall/
├── frontend/                 # React/Vue.js frontend application
│   ├── nginx.conf           # Nginx configuration
│   ├── Dockerfile
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                  # Django backend application
│   ├── .env                 # Environment variables
│   ├── start.sh            # Startup script
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
├── docker-compose.yml       # Docker Compose configuration
├── SETUP.md                 # This file
└── ...
```

## Troubleshooting

### Port Already in Use

If port 80, 8000, or 5432 is already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8080:80"      # Changed from 80:80
```

### Database Connection Error

1. Ensure PostgreSQL container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs postgres`
3. Verify `DB_HOST` in `.env` matches service name in `docker-compose.yml`

### Frontend Not Loading

1. Clear browser cache (Ctrl+Shift+Delete)
2. Check Nginx logs: `docker-compose logs frontend`
3. Verify `CORS_ALLOWED_ORIGINS` in backend `.env`

### Permission Denied on start.sh

```bash
chmod +x backend/start.sh
docker-compose up -d
```

## Production Deployment

Before deploying to production:

1. Update `SECRET_KEY` in `.env` with a secure value
2. Set `APP_ENV=production`
3. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
4. Configure external database and Redis
5. Set up SSL/TLS certificates
6. Configure appropriate logging
7. Use environment-specific `.env` files

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Contact: fengjianlin117@example.com
