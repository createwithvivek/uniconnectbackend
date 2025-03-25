#!/usr/bin/env bash
# Exit on error
set -o errexit
set -o nounset

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Create directories if they don't exist
echo "Creating static and media directories..."
mkdir -p static staticfiles media

# Migrate database
echo "Making and applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser only if not exists
echo "Checking for existing superuser..."
DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-adminpassword}"

SUPERUSER_EXISTS=$(echo "from django.contrib.auth import get_user_model; User=get_user_model(); print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())" | python manage.py shell | tail -n 1)

if [ "$SUPERUSER_EXISTS" = "False" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
    echo "from django.contrib.auth import get_user_model; User=get_user_model(); u=User.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save()" | python manage.py shell
else
    echo "Superuser already exists. Skipping creation."
fi

echo "Build and setup completed successfully!"
