#!/usr/bin/env bash
set -o errexit
set -o nounset

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating directories for static and media..."
mkdir -p static staticfiles media

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Environment variables (passed via Render environment)
DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-adminpassword}"
DJANGO_SUPERUSER_PHONE="${DJANGO_SUPERUSER_PHONE:-1234567890}"
DJANGO_SUPERUSER_ROLE="${DJANGO_SUPERUSER_ROLE:-admin}"

# Programmatically create superuser (works with custom fields)
echo "Checking if superuser exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    print("Creating superuser...")
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}",
        phone="${DJANGO_SUPERUSER_PHONE}",
        role="${DJANGO_SUPERUSER_ROLE}"
    )
else:
    print("Superuser already exists. Skipping creation.")
END

echo "Build and setup completed successfully!"
