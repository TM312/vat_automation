#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# echo "Waiting for postgres upgrade"

# exec python manage.py db upgrade

# echo "PostgreSQL upgraded"

exec "$@"
