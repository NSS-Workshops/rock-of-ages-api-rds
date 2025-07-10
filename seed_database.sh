#!/bin/bash

# Load environment variables
set -a
source .env
set +a

echo "🗄️  Setting up PostgreSQL database..."

# Run Django migrations
echo "⚙️  Running Django migrations..."
python3 manage.py migrate

echo "📋 Creating app-specific migrations..."
python3 manage.py makemigrations rockapi

echo "🔧 Applying app migrations..."
python3 manage.py migrate rockapi

echo "📊 Loading seed data..."
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata types
python3 manage.py loaddata rocks

echo "✅ Database setup complete!"
echo "🔗 Database connection: ${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo "👤 Database user: ${DB_USER}"
