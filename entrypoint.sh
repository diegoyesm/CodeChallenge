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

# Make migrations first
python manage.py makemigrations dbdata

# Apply migrations before flush
python manage.py migrate

# Only flush after migrations have been applied
python manage.py flush --no-input

exec "$@"