#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until /usr/bin/pg_isready -h "$host" -U "myuser" -d "mydatabase"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
