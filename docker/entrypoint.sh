#!/bin/sh
set -e

# Run migrations with a small retry in case the DB is briefly unreachable
# (e.g. when pg_isready succeeds before POSTGRES_DB is fully provisioned).
attempts=0
until alembic upgrade head; do
    attempts=$((attempts + 1))
    if [ "$attempts" -ge 10 ]; then
        echo "alembic upgrade head failed after $attempts attempts; giving up" >&2
        exit 1
    fi
    echo "alembic upgrade head failed (attempt $attempts); retrying in 1s..." >&2
    sleep 1
done

exec "$@"
