#!/bin/bash

POSTGRES="${POSTGRES_HOST}:${POSTGRES_PORT}"
echo "Wait for POSTGRES=${POSTGRES}"

wait-for-it ${POSTGRES}

if [ "$DJANGO_ENV" == "dev" ]
then
  echo "Running in ${DJANGO_ENV} mode..."
  make run-dev
else
  echo "Running in ${DJANGO_ENV} mode..."
  make run
fi

