# Database Management Challenge

A complete solution for managing department, job, and employee data with support for bulk operations, data analysis, backup, and restore functionality.

## Overview

This application provides a robust API for managing company data including departments, jobs, and hired employees. It supports bulk insert operations, data reporting, and complete backup/restore functionality. The application is containerized using Docker for easy deployment and consistent operation across environments.

## Features

- **Data Management**:
  - Create and manage departments, jobs, and employee records
  - Support for bulk data operations
  - RESTful API interface

- **Data Analysis**:
  - Analyze employee hiring by quarter
  - Identify departments exceeding average hiring rates

- **Backup & Restore**:
  - Complete database backup in AVRO format
  - Selective table restoration
  - Interactive restoration client

## Architecture

The application is built with:
- **Django & Django REST Framework**: Backend API framework
- **PostgreSQL**: Database for persistent storage
- **Docker & Docker Compose**: Containerization for consistent deployment
- **AVRO**: Data serialization for backups

## Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CodeChallenge
   ```

2. Start the application:
   ```bash
   cd dbchallenge
   docker-compose build
   docker-compose up
   ```

The application will be available at http://localhost:8000/

## API Endpoints

### Data Management

- **Departments**:
  - `GET/POST /api/departments/`: Manage individual departments
  - `GET/POST /api/departments-list-serializer/`: List or create multiple departments in one request
  - `GET/POST /api/departments-bulk-list-serializer/`: Bulk create departments

- **Jobs**:
  - `GET/POST /api/job-bulk-list-serializer/`: Bulk create jobs

- **Hired Employees**:
  - `GET/POST /api/hired-employee-bulk-list-serializer/`: Bulk create hired employees

### Data Analysis

- **GET /api/employees-hired-quarter/**: Get hired employees by quarter, department, and job
- **GET /api/employees-hired-department/**: Get departments exceeding average hiring rate

### Backup & Restore

- **GET /api/backup/**: Create a backup of all tables in AVRO format
- **GET /api/list-backups/**: List all available backups
- **POST /api/restore-table/**: Restore a specific table from a backup

## Utility Clients

The `dbload` directory contains utility scripts for interacting with the API:

### Data Loading

- **load_department.py**: Load departments individually from CSV
- **load_bulk_department.py**: Bulk load departments from CSV
- **load_bulk_jobs.py**: Bulk load jobs from CSV
- **load_bulk_hired_employees.py**: Bulk load hired employees from CSV

### Backup & Restore

- **backup_client.py**: Create a backup of all tables in AVRO format
- **restore_client.py**: Interactive client for restoring tables from backups

## Using Utility Clients

### Loading Data

1. Load department data:
   ```bash
   python dbload/load_bulk_department.py
   ```

2. Load job data:
   ```bash
   python dbload/load_bulk_jobs.py
   ```

3. Load hired employee data:
   ```bash
   python dbload/load_bulk_hired_employees.py
   ```

### Backup & Restore

1. Create a backup:
   ```bash
   python dbload/backup_client.py
   ```

2. List and restore from backups (interactive mode):
   ```bash
   python dbload/restore_client.py
   ```

3. Command-line restoration:
   ```bash
   # List all backups
   python dbload/restore_client.py list
   
   # Restore a specific table (using the backup index)
   python dbload/restore_client.py department 1
   ```

## Docker Solution

The application is containerized using Docker with the following components:

- **dbmigration**: The Django application container
  - Runs the Django development server
  - Applies migrations
  - Serves the API endpoints

- **dbmigration-db**: PostgreSQL database container
  - Stores all application data
  - Persists data using Docker volumes

### Docker Compose Configuration

The `docker-compose.yml` file defines the service configuration:

```yaml
services:
  dbmigration:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/usr/src/app/
    ports:
      - "0.0.0.0:8000:8000"
    env_file:
      - ./.env.dev
    depends_on:
      - dbmigration-db
  dbmigration-db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres

volumes:
  postgres_data:
```

### Dockerfile

The application container is built from the `Dockerfile`:

```dockerfile
# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
```

### entrypoint.sh

The entrypoint script ensures migrations are applied before starting the application:

```bash
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Create migrations directory if it doesn't exist
mkdir -p /usr/src/app/dbdata/migrations
touch /usr/src/app/dbdata/migrations/__init__.py

# Make migrations before attempting to apply them
python manage.py makemigrations dbdata
python manage.py migrate

exec "$@"
```

## Development

### Adding New Features

1. Modify the Django models in `dbdata/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update API views in `dbdata/views.py`
5. Add routes in `dbdata/urls.py`

### Database Schema

The application uses the following models:

- **Department**: Basic department information
- **Job**: Available job positions
- **HiredEmployee**: Employee records with relationships to department and job

## Interacting with the PostgreSQL Database

You can connect directly to the PostgreSQL database for advanced queries and data inspection using several methods:

### Using Docker CLI

1. Find the container ID of the PostgreSQL container:
   ```bash
   docker ps
   ```

2. Connect to the PostgreSQL container using psql:
   ```bash
   docker exec -it <container_id> psql -U postgres
   ```
   
   For example:
   ```bash
   docker exec -it dbchallenge_dbmigration-db_1 psql -U postgres
   ```

3. Once connected, you can:
   - List all databases: `\l`
   - Connect to the app database: `\c postgres`
   - List all tables: `\dt`
   - View table schema: `\d dbdata_department`
   - Query data: `SELECT * FROM dbdata_department;`
   - Exit psql: `\q`

### Using an External PostgreSQL Client

You can also connect using your preferred PostgreSQL client (e.g., pgAdmin, DBeaver) with these credentials:

- **Host**: localhost
- **Port**: 5432 (default PostgreSQL port)
- **Database**: postgres
- **Username**: postgres
- **Password**: postgres

### Common SQL Queries

Here are some useful queries for inspecting the data:

1. View all departments:
   ```sql
   SELECT * FROM dbdata_department;
   ```

2. View all jobs:
   ```sql
   SELECT * FROM dbdata_job;
   ```

3. View all hired employees with their department and job names:
   ```sql
   SELECT 
       e.id, 
       e.name, 
       e.datetime, 
       d.department, 
       j.job
   FROM 
       dbdata_hiredemployee e
   JOIN 
       dbdata_department d ON e.department_id_id = d.id
   JOIN 
       dbdata_job j ON e.job_id_id = j.id;
   ```

4. Count employees by department:
   ```sql
   SELECT 
       d.department, 
       COUNT(*) as employee_count
   FROM 
       dbdata_hiredemployee e
   JOIN 
       dbdata_department d ON e.department_id_id = d.id
   GROUP BY 
       d.department
   ORDER BY 
       employee_count DESC;
   ```

5. View employees hired in 2021 by quarter:
   ```sql
   SELECT 
       d.department,
       j.job,
       EXTRACT(QUARTER FROM e.datetime) as quarter,
       COUNT(*) as count
   FROM 
       dbdata_hiredemployee e
   JOIN 
       dbdata_department d ON e.department_id_id = d.id
   JOIN 
       dbdata_job j ON e.job_id_id = j.id
   WHERE 
       EXTRACT(YEAR FROM e.datetime) = 2021
   GROUP BY 
       d.department, j.job, quarter
   ORDER BY 
       d.department, j.job, quarter;
   ```

### Database Maintenance

You may occasionally need to perform database maintenance tasks:

1. Reset a table (remove all rows):
   ```sql
   TRUNCATE TABLE dbdata_department CASCADE;
   ```

2. Backup the database using pg_dump (run from host terminal):
   ```bash
   docker exec -it dbchallenge_dbmigration-db_1 pg_dump -U postgres postgres > postgres_backup.sql
   ```

3. Restore from a SQL backup (run from host terminal):
   ```bash
   cat postgres_backup.sql | docker exec -i dbchallenge_dbmigration-db_1 psql -U postgres
   ```

Note that the application's AVRO backup/restore functionality provides a more integrated approach for application-level backups, but direct database access gives you more flexibility for ad-hoc queries and database maintenance.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.