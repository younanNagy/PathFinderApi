#!/bin/sh

# Only run migrations if this is the web service
if [ "$SKIP_MIGRATIONS" != "true" ]; then
  echo "Running migrations..."
  python manage.py migrate

  echo "Loading sample data..."
  python manage.py loaddata test_data.json
else
	echo "Skip migration"
fi

echo "Starting application..."
exec "$@"