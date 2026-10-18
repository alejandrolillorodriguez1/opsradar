# Architecture and Technical Decisions

This document explains how OpsRadar is structured, what each component does,
and why it exists.

It is updated as the application evolves. Planned components are identified
explicitly and should not be treated as implemented features.

## 1. Local Development Environment

The local environment uses Docker Compose to run two services:

- `backend`: the FastAPI application.
- `db`: the PostgreSQL database server.

Compose connects both services through an internal network. The backend
reaches PostgreSQL using `db` as the hostname and `5432` as the port.

Inside the backend container, `localhost` refers to the backend container
itself, not the database.

### Why Docker?

Docker provides a consistent runtime without requiring Python or PostgreSQL
to be installed directly on each developer's machine.

### Why Docker Compose?

The application requires multiple services. Compose describes how to build,
configure, connect, and run them together.

## 2. Infrastructure and Dependency Files

### `compose.yaml`

Defines the local services, environment variables, ports, and volumes.

The backend waits for the PostgreSQL health check to pass before starting.
This coordinates startup but does not replace connection error handling
inside the application.

The backend source directory is mounted into the container, and Uvicorn
runs with automatic reload for development.

### `backend/Dockerfile`

Defines how to build the backend image.

It installs dependencies before copying application code so Docker can
reuse the dependency installation layer when only the source code changes.

Dependencies are installed using the lockfile. Development dependencies
are excluded from the current image.

### `backend/.dockerignore`

Excludes unnecessary or sensitive files from the Docker build context.

This reduces the files sent to the builder and helps prevent accidental
inclusion of local environments, caches, and secrets.

### `.gitignore`

Excludes local and generated files from version control.

Git ignore rules and Docker ignore rules serve different purposes:
one controls Git tracking, while the other controls Docker build inputs.

### `backend/pyproject.toml`

Declares project metadata, direct dependencies, development dependencies,
and tool configuration.

It expresses the dependency requirements of the project.

### `backend/uv.lock`

Records the exact dependency resolution, including transitive dependencies.

It is committed to Git so environments can install the same resolved
dependency versions.

## 3. Environment Configuration

### `.env`

Stores local configuration values used by Docker Compose.

Compose substitutes these values into the service configuration.
Variables are passed to containers through their `environment` settings.

This file is excluded from Git.

### `.env.example`

Documents the required environment variables using placeholder values.

It is committed to Git so developers know which settings to provide.

### PostgreSQL Initialization Variables

`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` initialize PostgreSQL
when its data directory is empty.

Changing these variables later does not automatically modify users,
passwords, or databases already stored in an existing volume.

## 4. Application Files

### `backend/app/__init__.py`

Identifies the application directory as a Python package.

### `backend/app/main.py`

Creates the FastAPI application and defines its metadata.

The current `/health` endpoint confirms that the API can respond to an
HTTP request. It does not check database connectivity.

### `backend/app/core/config.py`

Defines the application settings using `BaseSettings` from
`pydantic-settings`.

It reads and validates the following environment variables:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Required settings have no default values. Missing or invalid configuration
causes validation to fail when settings are loaded.

The database password uses `SecretStr`, which masks its value in normal
representations. This does not encrypt the password.

The `get_settings` function uses `lru_cache` to reuse the validated settings
within a process.

#### Why centralize settings?

A single configuration module avoids reading environment variables
throughout the codebase and provides consistent validation.

Deployment environments can provide different values without changing
application code.

## 5. Database Access Design

The following describes the intended responsibilities of `session.py`.
Implementation and connectivity must be verified separately.

### `backend/app/db/session.py`

Configures database access using three components:

1. A SQLAlchemy connection URL.
2. An engine.
3. A session factory.

#### Connection URL

The URL specifies the PostgreSQL driver, host, port, database, and credentials.

It is constructed with `URL.create` rather than manual string concatenation
to handle special characters in credentials correctly.

The selected driver is `postgresql+psycopg`.

#### Engine

The engine manages database connectivity and a pool of reusable connections.

Creating an engine does not immediately establish a database connection.

`pool_pre_ping=True` checks connections before they are reused to help
detect stale connections. It does not automatically retry failed business
transactions.

#### Session Factory

`SessionLocal` creates SQLAlchemy sessions.

A session provides a working context for database operations and transactions.
Sessions must be closed after use and must not be shared across concurrent
requests.

A successful write transaction is committed. Failed transactions require
rollback.

With `expire_on_commit=False`, loaded object attributes are not automatically
expired after a commit. Their values may become stale if another transaction
changes the database.

### Why These Libraries?

- Psycopg enables communication between Python and PostgreSQL.
- SQLAlchemy manages connections, SQL operations, ORM models, and transactions.
- Alembic versions changes to the database schema through migration files.

Installing these dependencies does not create application tables.

## 6. Data Persistence

PostgreSQL stores its data in the named volume `db_data`.

The volume is mounted at `/var/lib/postgresql/data`, matching the PostgreSQL
17 image used by this project.

Replacing a container does not delete its named volume.

`docker compose down` preserves the volume. Running it with `-v` removes
the project volumes and their stored data.

A persistent volume is not a backup.

## 7. Current Configuration Flow

Local `.env` file
→ Docker Compose variable substitution
→ Backend environment variables
→ Settings validation in `config.py`
→ Database configuration in `session.py`
→ PostgreSQL

Loading settings verifies configuration values. Executing a database query
is required to verify connectivity.

## 8. Upcoming Work

- Verify database connectivity.
- Define the SQLAlchemy declarative base in `db/base.py`.
- Configure Alembic.
- Implement the first database model and migration.
- Add request-scoped database sessions.