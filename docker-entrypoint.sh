#!/bin/bash

# Apply database migrations
echo "Apply 'default' database migrations"
python manage.py migrate

echo "Apply 'data_bank' database migrations"
python manage.py migrate data_store --database=data_bank

# Collects Static Folders
echo "Apply database migrations"
python manage.py collectstatic

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000