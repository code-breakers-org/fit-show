#!/bin/bash

if [ -z "${DJANGO_ENV}" ]; then
    echo "DJANGO_ENV cannot be empty"
    exit 1
fi

case "${DJANGO_ENV}" in
    dev|prod|qa|preprod)
        echo "DJANGO_ENV is set correctly to ${DJANGO_ENV}"
        ;;
    *)
        echo "DJANGO_ENV must be one of: dev, prod, qa, preprod"
        exit 1
        ;;
esac
