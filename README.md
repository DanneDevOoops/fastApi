[![Static Badge](https://img.shields.io/badge/Python-v3.11.7-blue)](https://devguide.python.org/versions/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)  
![Workflow Status](https://github.com/DMoest/fastApi/actions/workflows/install_and_test_application.yml/badge.svg)  
[![Build & deploy documentation to GH-pages](https://github.com/DanneDevOoops/fastApi/actions/workflows/build_and_deploy_sphinx_docs.yml/badge.svg)](https://github.com/DanneDevOoops/fastApi/actions/workflows/build_and_deploy_sphinx_docs.yml)

# Python FastAPI Application

This `FastAPI` application serves as a foundation for building backend
APIs using python and FastAPI. It provides a pre-configured template with
essential tools, configurations, and a basic application structure to
accelerate development. The aim is to offer a starting point that you can
customize by selecting the components that best suit your project's needs.

**NOTE:** This project is currently under development and may not be fully
functional.

## Preconfigured Tools Overview

This project is configured with a suite of tools commonly used in FastAPI
applications. Below is a list of these tools with a brief description of
their purpose:

1. [Poetry](https://python-poetry.org/) - A tool for virtual environment and
   dependency management in Python projects, simplifying dependency handling
   for both local and containerized environments.
2. [FastAPI](https://fastapi.tiangolo.com/) - A modern, high-performance web
   framework for building APIs with Python, known for its ease of use and
   speed.
3. [Alembic](https://alembic.sqlalchemy.org/en/latest/) - A database migration
   tool for managing and evolving database schemas.
4. [SQLAlchemy](https://www.sqlalchemy.org/) - A powerful ORM (
   Object-Relational Mapper) used for interacting with relational SQL
   databases.
5. [Beanie](https://docs.beanie-odm.org/) - An ODM (Object-Document Mapper) for
   interacting with MongoDB databases.
6. [Pytest](https://docs.pytest.org/en/7.4.x/) - A testing framework used for
   writing and running tests in Python.
7. [PyLint](https://pylint.pycqa.org/en/latest/) - A code quality tool used for
   checking code quality and adherence to coding standards.
8. [PostgreSQL](https://www.postgresql.org/) - A robust, open-source relational
   database used for storing application data.
9. [MongoDB](https://www.mongodb.com/) - A NoSQL document database used for
   flexible data storage.
10. [SQLite](https://www.sqlite.org/index.html) - A self-contained, file-based
    relational database, useful for local development and testing.
11. [Docker](https://www.docker.com/) - A containerization platform used for
    building, shipping, and running applications in isolated containers.
12. [Sphinx](https://www.sphinx-doc.org/en/master/) - A documentation generator
    used for creating API documentation from docstrings.
13. [Logger](https://docs.python.org/3/library/logging.html) - A built-in
    Python module for logging application events, errors, and warnings.

You can easily customize this template by removing or adding tools based on
your project's requirements. FastAPI's flexibility allows for seamless
integration with various libraries and tools.

## Getting Started

To get started with this application, follow the step-by-step instructions
below. The instructions are divided into sections for clarity. If you are
already familiar with setting up Python applications, you can use your
prefered method and skip sections 1 and 2 and proceed to go directly for  
section 3 for configuring the environment variables in your `.env` file.

**Note:** Keep in mind the tools configured in this project. If you choose to
use alternative tools/methods, you may need to adjust the subsequent steps
accordingly.

Otherwise, a good starting point is to `clone the code repository` and quickly
review the `Makefile` file located in the `project's root` directory. Now
you get a gimpse of the available commands and how to use them.

<details><summary style="font-size: 14px; font-weight: bold; 
color: lightgoldenrodyellow;">Clone the repository</summary>

This project is hosted on GitHub. You can checkout the
[github repository here](https://github.com/DanneDevOoops/fastApi). To move
forward and start using the project, you need to clone the repository to your
local machine. You can do this by following these steps:

1. Open a terminal and navigate to a directory where you like to clone the
   repository into.
2. Clone the github repository to your local machine:

```shell
git clone https://github.com/DanneDevOoops/fastApi \
&& cd fastApi
```

</details>

### A first look at the Makefile

The `Makefile` provides a set of commands for managing the application, running
tests, and performing other common development tasks. It simplifies command
execution and serves as a central reference for operations related to the tools
configured in this application. If you intend to extend this template, consider
adding commands for frequently used tools or operations to the `Makefile` for
easier access as you see fit.

If `make` is not installed on your system or you need to learn more about its
usage, refer to the official
[GNU make page](https://www.gnu.org/software/make/).

If you need to check for `make` on your system:

```shell
which make \ 
&& \
make --version 
```

As you follow these instructions further, you'll encounter references to the
`Makefile` for executing commands. If you like to see a list of available
make commands, run:

```shell
make help
```

### Virtualenv & Project Dependencies

For a `python-application` to work corectly and not to clutter
the `global python installation`, it is recommended and best practice to
create a new `virtual environment` (a.k.a `virtualenv`) intended for this
project only and install all the project dependencies into that `virtualenv`.

<details><summary style="font-size: 14px; font-weight: bold; 
color: lightgoldenrodyellow;">Configuring a python virtualenv & installing the project 
dependencies into it</summary>

This project is configured to use [Poetry](https://python-poetry.org/) for
Python package and environment management. While Poetry is the primary tool,
you can use alternative methods for managing your Python virtual environments
and installing dependencies. If you prefer a different approach, be aware that
it is not covered in this documentation, and you'll need to adapt the
instructions accordingly. Refer to the `pyproject.toml` file to identify the
project's dependencies. Also note that the `Makefile` is configured to work
with Poetry, so if you choose to use a different method, you may need to
modify the `Makefile` to suit your needs.

1. Ensure Poetry is installed on your system. If not, follow the
   [python-poetry installation guide](https://python-poetry.org/docs/#installation).

2. Create and activate a virtual environment for the project:

   ```shell
   make poetry-shell
   ```

   Verify the virtual environment is active:

   ```shell
   make poetry-env-info
   ```

   The command `poetry env info` displays information about the virtual
   environment. If the information is visible, you can proceed to install
   the dependencies.

3. Install the project dependencies into the activated virtualenv:

   ```shell
   make poetry-install
   ``
   `

   Verify that the dependencies are installed correctly into your virtualenv:

   ```shell
   make poetry-show-latest-top-level
   ```

   This shows the top level of project's dependencies, their installed
   versions, the latest available versions, and a brief description
   from [pypypi.org](https://pypi.org/). If you could verify the virtualenv
   and the installed dependencies, you are ready to move on.

   **NOTE:** `Poetry` have several neat ways to check the installed
   dependencies and their underlying packages. If needed poetry have the
   ability to resolve dependency version issues, update when new versions
   are available and much more. If you are not knowledgeable about Poetry,
   make sure to read up a little on it. It is a great tool!

</details>

### Environment Variables are stored in the .env file

Next we need to start thinking of the required `environment variables` for the
application to function correctly. These variables should be defined in a
`.env` file located in the `project's root directory`. The `.env` file must
be sourced before starting the application so that the application can read
the variables.

`IMPORTANT!` Ensure that your `.env` file remains private and is never shared.
This file contains sensitive information that should not be exposed. Never
commit the `.env` file to any version control repository, as it is intended to
store secrets securely. If you discover any data from the `.env` file in a
public or private repository, or exposed in any other way, consider that data
compromised. Immediately secure the data by changing the values in the `.env`
file and any other location where the data is used. Review your security
procedures and policies to prevent future leaks. This is critical for
maintaining the security of your application and your users' data. `CAUTION 
PLEASE!`

<details><summary style="font-size: 14px; font-weight: bold; color: 
lightgoldenrodyellow;">Setting environment variables in a .env file</summary>

With that said, if you have not already had a look at the `.env.example`
file, do so now. Here is a quick way to do it:

```shell
make look-at-env-example
```

Then create a new `.env` file from the `.env.example` file
using the following command:

```shell
make create-dot-env-file
```

After running this command, a `.env` file will be created in the `root` of your
project. Inspect it to ensure it contains the same variables as the
`.env.example` file. You can then start to edit it to set `your own 
values` for these variables.

The `.env` file is organized into sections, each containing environment  
variables related to specific application parts, modules or services used
by the application.
The main sections are:

1. Environments
2. Application basics
3. Security (JWTs & API keys)
4. Application loggers
5. PostgreSQL database
6. MongoDB database
7. SQLite database

As you go about developing your project, you may need to `add more 
variables to the .env` file. To do this, add the new variable to the .env
file and then define a corresponding configuration in the
`src/core/env_config.py` module. This allows the application to read and
use the variable through the `settings object` initialized during the
`application startup lifecycle` in `src/main.py`.

#### Application Environment

* `ENV_NAME` - References the environment you are running the application in.
* `PYENV_VERSION` - References the `pyenv` version you are using. This is
  optional and can be set to any value you choose. If you intend to use
  this its menat to load the correct `virtualenv` for the project automatically
  when you start the application when able to do so.
* `APP_NAME` - The name of the application. This is used for logging and
  other purposes.
* `APP_HOST` - The host of the application. Default value is `0.0.0.0`.
* `APP_PORT` - The port of the application. Default value is `1337`.
* `APP_RELOAD` - The reload option for the application. Default value is
  `True`. This is used for development purposes only. In production, this
  should be set to `False`.
* `APP_DEBUG` - The debug option for the application. Default value is `True`.
  This is used for development purposes only. In production, this should be
  set to `False`.

#### Application Security & external services

* `APP_ALGORITHM` - The algorithm used for encoding and decoding JWTs. Default
  value is `HS256`.
* `APP_JWT_SECRET_KEY` - The secret key used for encoding and decoding JWTs.
  This should be a long random string. No default value is provided. You must
  set this value and recomendation is to use some sort of string generator to
  generate a long random string. Never expose it, never loose it and never
  share this value with anyone.

This next section is intended to store api keys for external services to
access the api. For working with the api you need to register the api keys with
here and configure it in the `src/core/env_config.py` module. The
namespaces for the keys below, except the `APP_HEALTH_CHECK_API_KEY`, are
just examples but try rather to be more explicit about the namespace you
choose in relation to the service you are using.

**Note:** This could potentially be moved to a more secure position as a
hashed value in a database or similar later on. So concider this a work in
progress atm!

* `APP_HEALTH_CHECK_API_KEY` - The API key used for accessing the health check
  service. This is used for testing purposes only and is intentially
  separated from other api keys so it can be swapped out easily. No default
  provided here.
* `APP_1_API_KEY` - The API key used by application nr. 1 for accessing the
  API with. No default provided here. **First Note:** This is just a example
  palceholder for a API key, but you can and should use a more descriptive
  namespace for your API keys when registering them as a external service with
  your api.

#### Loggers

* `APP_LOGGER_NAME` - The name of the application logger.
* `CONSOLE_LOGGER_LEVEL` - The logging level for the console logger.
* `CONSOLE_LOGGER_FORMAT` - The logging format for the console logger.
* `CONSOLE_LOGGER_PROPAGATE` - The propagate option for the console logger.
* `FILE_LOGGER_LEVEL` - The logging level for the file logger.
* `FILE_LOGGER_FILE_NAME` - The file name for the file logger output.
* `FILE_LOGGER_FILE_SIZE` - The file size for the file logger. This is used for
  rotating the log files. Its specified in bytes. Default value is `10MB`.
* `FILE_LOGGER_FILE_COUNT` - The number of log files to keep for the file
  logger. Default value is `5`. This means that the application will keep the
  last 5 log files and delete the rest. This is used for rotating the log
  files and not to clutter the disk with log files.
* `FILE_LOGGER_DIR` - The directory for the file logger. Default value is
  `./logs` by intention and needs to be that value for the application
  logger to work both with writing to a docker volume and writing locally.
* `FILE_LOGGER_FORMAT` - The logging format for the file logger.
* `FILE_LOGGER_MODE`- The mode for the file logger. Default value is `w` for
  writing to the file. This means that the application will overwrite the log
  file if it exists. If you want to append to the log file, you can change
  this value to `a`.
* `FILE_LOGGER_PROPAGATE` - The propagate option for the file logger.
* `FILE_LOGGER_DOCKER_HOST_MACHINE_PATH` - The path to the log file on the host
  machine. This is used for writing the log file to a docker volume. Place
  this where you want your logs to be written to on the host machine.

The rest of the environment variables in the `.env` file are related to
databases and this will be explained in the section related to each
database type.

</details>

### Database configuration

The application supports integration with three types of databases:

* PostgreSQL - A robust, open-source relational database for structured data.
* MongoDB - A flexible, document-oriented NoSQL database for unstructured data.
* SQLite - A lightweight, file-based relational database ideal for development
  and testing.

This documentation assumes you are already familiar with basic database setup
and management. The following sections provide guidance on configuring the
application to connect to an existing database, but do not cover general
database administration or creation.

<details><summary style="font-size: 14px; font-weight: bold;
color: lightgoldenrodyellow;">PostgreSQL</summary>

#### PostgreSQL as a part of the application

To establish a PostgreSQL database connection, the API application uses the
`@contextmanager` function `app_lifespan` in `src/main.py` to manage the
application lifecycle. All routes that interact with the PostgreSQL
database are registered through the api_v1_router.

If you need guidance on creating a PostgreSQL database, refer to the
repository's `Wiki` or other external resources. This section only covers the
environment variables required to connect to an existing PostgreSQL database,
assuming you already have the necessary credentials.

##### Connecting application to PostgreSQL

To connect the application to a PostgreSQL database, set the following
variables in your .env file:

* `PG_DB_NAME`: Name of the PostgreSQL database to connect to.
* `PG_DB_HOST`: Host address of the PostgreSQL server. Default is 0.0.0.0. If
  using Docker Compose, set this to the internal host IP of the Postgres
  container.
* `PG_DB_PORT`: Port for the PostgreSQL server (default: 5432).
* `PG_DB_USERNAME`: Username for the PostgreSQL database.
* `PG_DB_PASSWORD`: Password for the PostgreSQL database.
* `PG_DB_BACKUP_DIR`: Directory for storing database backups (default: .
  /db_dumps). This should remain unchanged for Docker compatibility.
* `PG_DB_DOCKER_HOST_MACHINE_BACKUP_PATH`: Path on the host machine for
  storing backup files when using Docker volumes.

You may also adjust advanced settings as needed:

* `PG_DB_FUTURE` (default: True)
* `PG_DB_ECHO` (default: False)
* `PG_DB_AUTO_COMMIT` (default: False)
* `PG_DB_CONNECTION_POOL_SIZE` (default: 100)
* `PG_DB_MAX_OVERFLOW` (default: 0)
* `PG_DB_PRE_PING` (default: False)
* `PG_DB_EXPIRE_ON_COMMIT` (default: False)

For more details on Docker configuration, see the Postgres Docker image
documentation.

If you do not wish to use PostgreSQL, comment out its
`connection initialization` and the `api_v1_router` registration in
`src/main.py` to disable related features.

##### Database migrations, SQLAlchemy and Alembic

The `api_v1_router` uses `SQLAlchemy` for `ORM` operations and `Alembic` for
database `migrations`. To initialize your database tables, first check for
pending migrations:

```shell
make alembic-show-current
```

If migrations are pending, apply them with this command:

```shell
make alembic-upgrade-head
```

After running migrations, your database tables will be created and ready for
use.

---

</details>



<details><summary style="font-size: 14px; font-weight: bold;
color: lightgoldenrodyellow;">MongoDB</summary>

Similar to the PostgreSQL database connection, the MongoDB database connection
is established during the application startup within the `@contextmanager`
function `app_lifespan` in `src/main.py`. API routes that interact with the
MongoDB database are registered through the `api_v2_router`.

To connect to a MongoDB database, set the following environment variables in
your `.env` file:

* `MONGO_DB_NAME` - The name of the MongoDB database. This is the database that
  the application will connect to.
* `MONGO_DB_HOST` - The host of the MongoDB database. This is the address of
  the database server. Default value is `
* `MONGO_DB_PORT` - The port of the MongoDB database. Default value is `27017`.
* `MONGO_DB_USERNAME` - The username for the MongoDB database. This is the
  user that the application will use to connect to the database.
* `MONGO_DB_PASSWORD` - The password for the MongoDB database. This is the
  password that the application will use to connect to the database.
* `MONGO_DB_DOCKER_HOST_VOLUME_PATH` - The path to the MongoDB database files
  on the host machine. This is used for writing the database files to a
  `docker volume`. Place this where you want your database files to be
  written to on the host machine.

Once configured, you should be able to access the database and run queries
through the API routes registered in the `api_v2_router`.

To disable MongoDB integration, comment out its connection initialization and
the api_v2_router registration in src/main.py. This will prevent the
application from attempting to connect to MongoDB or expose related API routes.

---

</details>

### Running the application locally

By now you should be able to start the application. The application is
configured to run both locally and in a Docker container. The startup
commands are configured in the `Makefile` and can be executed using the
`make` command.

This would be the most basic of commands to start the application with:

```shell
make uvicorn-run
```

In case you like to start it locally but on a specific port, you can do so
by running the command and you will be prompted to enter the port you want
to run the application on:

```shell
make uvicorn-run-port
```

Now the application should be running and you can access it from postman or
another API client making a request to any of the routes defined in the
registered api routers.

### Running the application in Docker

If you like to run the application in a Docker container, you can do so by
running the following command:

```shell
make docker-compose-up
```

Now the containers will be pulled from Docker Hub and started. Same
principal applies to this as to running it locally. You can access the
application from postman or another API client making a request to any of
the routes defined in the registered api routers.



---

## Working with the code base

### Documenting the code base

To bring a project forward and to make it easier for other developers to
understand the code, it is important to document the code and the API. This
project is configured to use `Sphinx` for generating documentation from the
docstrings in the code. The documentation is generated in the `docs` folder
and can be viewed in a web browser. Since we use FastAPI there is a
built in `OpenAPI Swagger UI` that automatically updates as you write more
routes and register them to the application. A simple Wiki is also
avaliable in the repository that provides some additional information.

<details><summary style="font-size: 14px; font-weight: bold;
color: lightgoldenrodyellow;">Documentation tools</summary>

#### Sphinx documentation

This project uses `Sphinx` to automatically generate documentation from the
code's `docstrings`. The generated documentation is located in the docs
directory and can be viewed in a web browser. By building documentation
directly from the source code, Sphinx ensures that the documentation
remains accurate and up to date. The documentation is intended to be
configured in a `CICD pipeline` for rebuilding and deploying automatically
whenever changes are pushed to the `main branch` of the repository.

#### OpenAPI Swagger UI

FastAPI provides interactive API documentation using Swagger UI, which allows
you to explore and test API routes directly from your browser. After starting
the application, visit http://localhost:<PORT_OF_YOUR_CHOICE>/docs to access
the Swagger interface.

You do not need to configure anything for this to work. The application is
configured to automatically generate the Swagger UI documentation based on
the API routes and their associated docstrings. The Swagger UI provides a
user-friendly interface for testing the API endpoints, viewing request and
response schemas, and understanding the available operations.

#### Wiki

There are a few `Wiki pages` available in the repository that provide
additional information about the project. The wiki is intended to be a
place for more detailed information about the project, including
some extra information about the tools used in the project, how to use them
and how to configure them.

</details>

### Linting for code quality and a more consistent code base

The project have PyLint configures to enable you to check the code quality.
PyLint is a powerful static code analysis tool that helps maintain high
code quality by automatically checking Python code for errors, enforcing
coding standards, and identifying potential issues such as unused variables,
code smells, and stylistic inconsistencies. By integrating PyLint into your
development workflow, you can catch bugs early, ensure adherence to best
practices, and improve the overall readability and maintainability of your
codebase.

### Automated formatting in pull requests

The CI workflow includes `isort` and `black` formatting behavior for pull
requests:

* For PRs opened from branches in this repository, CI can auto-format `src/`
  and push a commit back to the PR branch.
* For PRs opened from forks, CI runs check-only validation (`isort --check-only`
  and `black --check`) and reports formatting issues without pushing changes.

To match CI locally before pushing, run:

```shell
make isort-src
make black-src
```

<details><summary style="font-size: 14px; font-weight: bold; 
color: lightgoldenrodyellow;">Using Pylint</summary>

To lint the entire code base in `src directory` you can run the following
command:

```shell
make pylint-app
```

If you like to lint just a specific file or directory, you can do so by
running the command and you will be prompted to enter the file or
directory you want to lint:

```shell
make pylint-path
```

</details>

### Testing the code base

There are many approaches to testing, and the strategy you choose is up to you.
This project is set up to use `PyTest` for testing the codebase. PyTest is a
powerful and flexible framework that makes it straightforward to write simple,
scalable tests for a variety of scenarios.

<details><summary style="font-size: 14px; font-weight: bold; 
color: lightgoldenrodyellow;">Using PyTest</summary>

### Running PyTest

This application uses PyTest for testing. To ensure code quality, run the tests
locally before pushing changes to the repository. Tests are also executed
automatically in the CI/CD pipeline on the stage and main branches to verify
that the code functions as expected.

To run the test suite, use:

```shell
make pytest
```

The badge at the top of the repository indicates the status of the tests
in the CI/CD pipeline. If the tests pass, the badge will be green. If the
tests fail, the badge will be red. This provides a quick overview of the
code's health and functionality of the code base.

</details>
