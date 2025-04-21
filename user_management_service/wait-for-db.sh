#!/bin/sh
set -e

host="${DB_HOST:-postgres}"
port="${DB_PORT:-5432}"

echo "Waiting for database at $host:$port..."
until nc -z "$host" "$port"; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done

>&2 echo "Database is up - continuing"
exec "$@" 