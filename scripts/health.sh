#!/bin/sh

curl --fail http://localhost:${DJANGO_PORT}/health || exit 1
