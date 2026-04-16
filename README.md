# Buchi Pet Adoption API

Buchi Pet Adoption API is a production-oriented backend for a pet adoption platform built with FastAPI and PostgreSQL. It allows users to create pets, search across local and external dog data, add customers, create adoption requests, fetch adoption history within a date range, and generate adoption reports.

The project is structured around Clean Architecture principles so the API layer, business logic, domain model, and infrastructure concerns remain clearly separated and easier to maintain as the application grows.

## What The API Supports

- Create pets with photo upload and local file storage
- Search pets using filters such as type, age, gender, size, and `good_with_children`
- Merge local pet results with dog data from TheDogAPI
- Prioritize local pets over external results
- Add customers with unique phone numbers
- Create adoption requests for local pets and external dogs
- Fetch adoption requests within a date range
- Generate adoption statistics by pet type and weekly adoption counts

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Gunicorn with Uvicorn workers
- Docker and Docker Compose
- Pytest
- TheDogAPI for external dog search

## Project Structure

```text
app/
  api/              FastAPI routes, dependency wiring, error handlers
  application/      Service layer and business orchestration
  core/             Config and shared exceptions
  domain/           Entities, enums, repository interfaces, value objects
  infrastructure/   SQLAlchemy models, repositories, external integrations, storage
  schemas/          Request and response models
tests/
  unit/             Unit tests for application logic
  integration/      API-level integration tests
docker/             Container entrypoint script
```

## Architecture Notes

The application follows a practical Clean Architecture approach:

- The `domain` layer contains the business model and contracts
- The `application` layer coordinates use cases through services
- The `infrastructure` layer handles PostgreSQL, file storage, and TheDogAPI integration
- The `api` layer stays thin and only translates HTTP requests into service calls

This keeps business rules out of controllers and persistence details out of the domain layer.

## External API Behavior

The project uses TheDogAPI as its only external provider.

- External results are only used when the search includes `dog`
- Local pets support multiple pet types such as dogs, cats, and birds
- Search results always return local pets first
- External dog data is normalized into the internal pet model
- Missing external fields are handled safely rather than crashing the API

## Running The Project

### Option 1: Docker

This is the recommended way to run the project.

```bash
docker-compose up --build
```

Once the containers are up:

- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- PostgreSQL from your host machine: `localhost:5433`

Notes:

- PostgreSQL is created automatically by Docker
- Table creation runs automatically during container startup
- A local `.env` file is optional because `docker-compose.yml` includes working defaults
- If you want real external dog results, set `THEDOGAPI_API_KEY` in your shell or in a local `.env` file

### Option 2: Local Development

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

## Environment Variables

Example values are provided in [.env.example](/Users/naomi/Downloads/buchi-pet-adoption-api/.env.example).

Important settings:

- `DATABASE_URL`
- `THEDOGAPI_API_KEY`
- `MEDIA_ROOT`
- `MEDIA_URL_BASE`
- `GUNICORN_WORKERS`

## API Endpoints

### `POST /create_pet`

Creates a pet in the local database and stores uploaded photo files locally.

### `GET /get_pets`

Searches local pets first, then fills remaining results with external dogs when applicable.

### `POST /add_customer`

Creates a customer or returns the existing customer when the phone number already exists.

### `POST /adopt`

Creates an adoption request. If the selected pet is external, a local snapshot is created before the adoption request is stored.

### `GET /get_adoption_requests`

Returns adoption requests within a date range.

### `POST /generate_report`

Returns adoption statistics by pet type and weekly adoption counts.

## Testing

Run the full test suite with:

```bash
pytest
```

The test setup includes:

- Unit tests for application services, especially pet search orchestration
- Integration tests for the main API endpoints
- Mocked external provider behavior
- Isolated test database setup
- Repeatable execution without depending on a live external API


## Production Readiness

The project includes a few practical production-focused touches:

- Gunicorn with Uvicorn workers
- Dockerized application and database setup
- Environment-based configuration
- Centralized API error handling
- PostgreSQL-backed persistence
- Unit and integration test coverage
- Local file storage served through URL paths

## Additional Value

Beyond the core requirements, the project also includes:

- Centralized API error handling
- Bonus reporting endpoint
- External dog search integration with local-first result merging
- External pet snapshot support during adoption
- Docker-based PostgreSQL and application setup
- Gunicorn-based production serving
- Postman collection and environment files for demo and testing


## Current Limitations

- TheDogAPI only provides dog data, so external search is intentionally limited to dogs
- External dog fields such as age, gender, and `good_with_children` may be missing
- Migrations are not set up yet; the project currently creates tables automatically at startup

## Author

Built as the backend for the Buchi pet adoption application using FastAPI, PostgreSQL, and Clean Architecture principles.
