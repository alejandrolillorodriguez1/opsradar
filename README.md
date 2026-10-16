# OpsRadar

OpsRadar is an operations management platform designed to help teams detect order delays, investigate issues, and track incidents through resolution.

The project follows a backend-first approach, with a React frontend planned after the core API and business workflows are implemented.

## Project Status

Early development. The features below describe the planned scope and are not yet implemented.

## Problem

Operations teams often rely on spreadsheets and manual checks to identify delayed orders. This makes it difficult to prioritize issues, assign ownership, and maintain a clear history of decisions.

OpsRadar aims to bring these workflows into one platform, connecting order data with actionable incidents.

## Planned Core Features

- Organization-based workspaces with isolated data.
- User authentication and role-based permissions.
- Order creation, retrieval, and management.
- CSV imports with validation and error reporting.
- Background processing with retries and duplicate prevention.
- Rule-based detection of delayed orders.
- Incident assignment, prioritization, and resolution.
- Audit history for key operational actions.
- Dashboard with order and incident metrics.

## Technology Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- pytest

### Frontend

- React
- TypeScript
- Vite

### Infrastructure and Delivery

- Docker and Docker Compose
- GitHub Actions
- AWS
- Terraform

The background processing technology will be selected when the import workflow is designed.

## Repository Structure

- `backend/` — API, business logic, database migrations, and tests.
- `frontend/` — Web application, to be developed after the backend.
- `docs/` — Architecture notes and technical decisions.

Docker Compose configuration will be maintained at the repository root.

## Development Roadmap

1. Set up the backend, database, and local container environment.
2. Implement the initial order API and database migrations.
3. Add authentication, organizations, and permissions.
4. Build reliable CSV import workflows.
5. Implement delay detection and incident management.
6. Validate critical workflows and configure continuous integration.
7. Build the frontend.
8. Deploy to AWS and document the system.

## Quality Goals

- Prevent access to data belonging to another organization.
- Handle invalid imports with clear, actionable errors.
- Support retries without creating duplicate orders.
- Keep incident decisions traceable.
- Test critical business workflows.
- Make local development and deployment reproducible.

## Local Development

Setup instructions will be added once the initial application and Docker Compose environment are available.

Local credentials and secrets must remain outside version control. An example configuration file will document the required settings using placeholder values.

## Future Extension

After the core platform is complete, an AI assistant may be added to summarize incidents and suggest next steps using traceable sources.

Order calculations and delay detection will remain deterministic.

## Project Purpose

OpsRadar is a portfolio and learning project focused on practical backend engineering, multi-tenant application design, reliable data processing, and cloud deployment.

Demo environments will use synthetic data.
