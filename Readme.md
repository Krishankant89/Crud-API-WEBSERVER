# CRUD API Web Server

A simple **Flask + SQLAlchemy** REST API for managing student records with full CRUD operations, healthcheck endpoint, and database migrations via Flask-Migrate.

## Features

- Student CRUD (`create`, `read all`, `read by id`, `update`, `delete`)
- Email uniqueness validation
- JSON-based request/response handling
- Healthcheck endpoint
- SQLite support via `DATABASE_URL`
- Migration support with Flask-Migrate (Alembic)

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv
- SQLite (default)

## Project Structure

```text
Crud-API-WEBSERVER/
|-- app/
|   |-- __init__.py        # App factory, DB init, error handlers
|   |-- config.py          # Environment-based configuration
|   |-- logger.py          # App logger config
|   |-- models.py          # Student model
|   `-- routes.py          # API endpoints
|-- migrations/            # Alembic migration files
|-- tests/
|   `-- test_students.py
|-- .env
|-- Makefile
`-- run.py                 # App entry point
```

## API Base URL

```text
http://127.0.0.1:5000/api/v1
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/healthcheck` | Service health status |
| POST | `/students` | Create student |
| GET | `/students` | Get all students |
| GET | `/students/<id>` | Get student by ID |
| PUT | `/students/<id>` | Update student |
| DELETE | `/students/<id>` | Delete student |

## Request Examples

### Create Student

`POST /api/v1/students`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 21
}
```

### Update Student

`PUT /api/v1/students/1`

```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 22
}
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:

```env
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///students.db
```

4. Run migrations:

```bash
flask db upgrade
```

5. Start the app:

```bash
python3 run.py
```

## Makefile Commands

```bash
make run      # Run application
make migrate  # Create migration
make upgrade  # Apply migration
make test     # Run tests
make docker-build APP_VERSION=1.0.0                     # Build semver-tagged image
make docker-run APP_VERSION=1.0.0 PORT=5000            # Run container
make docker-stop                                       # Stop running container
```

## Docker Usage

The repository includes a **multi-stage Dockerfile**:

- `builder` stage installs Python dependencies into a virtual environment.
- `runtime` stage copies only runtime artifacts (venv + app code), runs as non-root user, and keeps image size small.

### Build Image (Semver Tag)

Use explicit semantic version tags (avoid `latest`):

```bash
docker build -t crud-api-webserver:1.0.0 .
```

Or via Makefile:

```bash
make docker-build APP_VERSION=1.0.0
```

### Run Container with Runtime Environment Variables

You can inject environment variables at runtime:

```bash
docker run --rm -d \
  --name crud-api-webserver \
  -p 5000:5000 \
  -e PORT=5000 \
  -e DATABASE_URL=sqlite:///students.db \
  crud-api-webserver:1.0.0
```

Or via Makefile:

```bash
make docker-run APP_VERSION=1.0.0 PORT=5000 DATABASE_URL=sqlite:///students.db
```

### Healthcheck

```bash
curl http://127.0.0.1:5000/api/v1/healthcheck
```

## Response Behavior

- `400` for missing/invalid request body
- `404` when student/resource is not found
- `409` when `email` already exists
- `500` for internal server errors

## Notes

- The app uses the Flask app factory pattern (`create_app`).
- Student `email` is unique at both API and database level.