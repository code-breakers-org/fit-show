#!/bin/bash

POSTGRES="${POSTGRES_HOST}:${POSTGRES_PORT}"
echo "Wait for POSTGRES=${POSTGRES}"

wait-for-it ${POSTGRES}

echo "Collect static files"
make collect-static

echo "Apply database migrations"
make make-migrations
make migrate

if [ "$DJANGO_ENV" == "dev" ]
then
  echo "Running in ${DJANGO_ENV} mode..."
  make run-dev
else
  echo "Running in ${DJANGO_ENV} mode..."
  make run
fi

