# migration-init.sh
#!/bin/bash

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run Django migrations and load initial test data
python manage.py migrate
python manage.py loaddata test_data.json