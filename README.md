# Django Project Boilerplate

## Table Of Contents

- [Getting Started](#getting-started)
- [Notes](#notes)
    - [Database host & name](#database-host--name)
- [dbdocs](#dbdocs)


## Getting Started
  1. If you wish to use a Makefile, please consider installing make by referring to the [Make documentation](https://www.gnu.org/software/make/).
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


1. Build the dockerfile (Note: If you don't have docker and docker compose -f docker-compose.local.yml already
   installed (** Consider renaming the environment variables' files to .django, .postgres and .redis **)
   flow the instructions of [Docker official docs](https://docs.docker.com/compose/install/) to install them):

    ```bash
    $ docker compose -f docker-compose.yml build
    ```
2. Your image is ready, and you can run your project by typing `$ docker compose -f docker-compose.local.yml up -d` in
   the terminal

## Notes

### Database host & name

If you are going to change the database container name from starter_database to another name such as project_x_database.
Consider changing the .postgres env file accordingly.
You should set the host name
to project_x_database.


# dbdocs
To use dbdocs in this project, you need to install Node.js based on your operating system.
For more details, [Visit Node.js Downloads](https://nodejs.org/en/download) .

After installing Node.js, run the following two commands to initialize dbdocs:

```bash
  $ make install-dbdocs
  $ make initial-dbdocs
```

