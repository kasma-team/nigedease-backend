# Nigedease Backend

This is the backend service for the Nigedease application, consisting of two main services:
- Core Service (Port 8000)
- User Management Service (Port 8001)

## Prerequisites

- Docker
- Docker Compose
- Git

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd nigedease-backend
```

2. Create a `.env` file in the root directory with the following variables:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
```

3. Build and start the services:
```bash
docker-compose up --build
```

The services will be available at:
- Core Service: http://localhost:8000
- User Management Service: http://localhost:8001

## Development

To run the services in development mode with hot-reloading:

```bash
docker-compose up
```

## API Documentation

Once the services are running, you can access the API documentation at:
- Core Service: http://localhost:8000/swagger/
- User Management Service: http://localhost:8001/swagger/

## Database

The application uses PostgreSQL as the database. The database is automatically created and initialized when the services start up.

## Testing

To run the tests:

```bash
docker-compose exec core_service python manage.py test
docker-compose exec user_management python manage.py test
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run the tests
4. Submit a pull request 