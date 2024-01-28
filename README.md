# Django Project Boilerplate

## Table Of Contents

- [Getting Started](#getting-started)
- [Notes](#notes)
    - [Database host & name](#database-host--name)
- [dbdocs](#dbdocs)

## Getting Started

1. If you wish to use a Makefile, please consider installing make by referring to
   the [Make documentation](https://www.gnu.org/software/make/).
   The Makefile is provided to include general commands that can be used consistently, enhancing development speed.

2. Please run below command to add pre-commit hook, for code quality assurance:
    ```bash
    # If `make` is installed
    $ make githook

    # or

    # If `make` is an unrecognized command
    $ git config --local core.hooksPath ./.githooks/
    ```
   Make sure you will have your pipeline on GitLab, referencing `.gitlab-ci.yml` file.<br><br>

### Run With Docker

1. Build the dockerfile (Note: If you don't have docker and docker compose already installed follow the instructions
   of [Docker official docs](https://docs.docker.com/compose/install/) to install them):

> Note that you should pass following environment variables in order to be able to build your docker images:

- `APP_NAME` to name docker images and hosts. example: `${APP_NAME}_postgres_${DJANGO_ENV}`
- `DJANGO_ENV`  to name docker images and hosts. example: `${APP_NAME}_postgres_${DJANGO_ENV}`
- `DJANGO_PORT` in order to run backend server on the specific port. example: `8000`
- `POSTGRES_PASSWORD` need it to create config based on given password
- `POSTGRES_USER` need it to create config based on given username
- `POSTGRES_DB` need it to create config based on given database name and create it in database
- `POSTGRES_EXPOSE_PORT` to be able to access the DB through outside the docker
- `POSTGRES_PORT` to map it with expose port
- `REDIS_PASSWORD` need it to create config based on given password
- `REDIS_DISABLE_COMMANDS` need it to disable commands when creating config. example: `FLUSHDB,FLUSHALL`
- `REDIS_PORT` to map it with expose port
- `REDIS_EXPOSE_PORT` to be able to access the redis through outside the docker

 ```bash
    $ docker compose  build
    $ docker compose  up
 ```

2. To run with **pgadmin**

> Note that you should pass following environment variables in order to be able to build your docker images:

- `PGADMIN_EXPOSE_PORT` to be able to access the pgadmin through your browser. example: `127.0.0.1:5050`
- `PGADMIN_DEFAULT_EMAIL` set a default email to be able to log in
- `PGADMIN_DEFAULT_PASSWORD` set a default password to be able to log in

 ```bash
    $ docker compose --profile pgadmin  build
    $ docker compose --profile pgadmin up
 ```

> To stop docker compose with pgadmin use this command `docker compose --profile pgadmin down`

> To connect the DB through pgadmin (run with docker), you should set host name based on your db docker
> hostname `${APP_NAME}_postgres_${DJANGO_ENV}`

# dbdocs

To use dbdocs in this project, you need to install Node.js based on your operating system.
For more details, [Visit Node.js Downloads](https://nodejs.org/en/download) .

After installing Node.js, run the following two commands to initialize dbdocs:

```bash
  $ make install-dbdocs
  $ make initial-dbdocs
```

