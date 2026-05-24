#!/usr/bin/make -f

.PHONY: alembic-downgrade alembic-help alembic-init alembic-init-template \
alembic-list-templates alembic-revision alembic-revision-and-upgrade \
alembic-show-branches alembic-show-current alembic-show-heads \
alembic-show-history alembic-show-revision-details alembic-upgrade \
alembic-docker-upgrade-current alembic-docker-revision alembic-docker-revision-auto \
alembic-docker-upgrade alembic-docker-current \
create-dot-env-file look-at-env-example source-env \
docker-build docker-remove docker-run docker-stop docker-compose-up docker-compose-down \
docker-mode docker-mode-stop local-db-mode local-db-mode-stop docker-logs local-db-logs \
help \
poetry-add-group poetry-add-package poetry-add-requirements-txt \
poetry-config-list poetry-env-info poetry-env-info-path poetry-env-list \
poetry-env-remove-all poetry-export-to-requirements poetry-install \
poetry-install-all-extras poetry-install-extras poetry-install-no-root \
poetry-install-only poetry-install-only-root poetry-install-sync \
poetry-install-with poetry-install-without poetry-lock poetry-lock-no-update \
poetry-lock-update poetry-pip-freeze poetry-pip-freeze-to-txt-file \
poetry-remove-group poetry-remove-lock-file poetry-remove-package \
poetry-shell poetry-show-latest-top-level poetry-update \
poetry-update-dry-run poetry-version \
isort-src black-src pylint-app pylint-path \
pytest \
sphinx-apidoc sphinx-build-html sphinx-build-html-for-gh-pages \
sphinx-clean-up sphinx-coverage-report sphinx-gen-docs \
sphinx-gen-docs-and-coverage sphinx-regen-docs sphinx-regen-docs-and-coverage \
uvicorn-run uvicorn-run-app-on-port



help:  # Show the available commands
	@echo "\nAvailable MAKE commands:"
	@echo "========================"

	@echo "\nAlembic commands:"
	@echo "  alembic-downgrade"
	@echo "  alembic-help"
	@echo "  alembic-init"
	@echo "  alembic-init-template"
	@echo "  alembic-list-templates"
	@echo "  alembic-revision"
	@echo "  alembic-revision-and-upgrade"
	@echo "  alembic-show-branches"
	@echo "  alembic-show-current"
	@echo "  alembic-show-heads"
	@echo "  alembic-show-history"
	@echo "  ≈"
	@echo "  alembic-upgrade"
	@echo "  alembic-docker-upgrade-current"
	@echo "  alembic-docker-revision MSG=your_message"
	@echo "  alembic-docker-revision-auto MSG=your_message"
	@echo "  alembic-docker-upgrade REV=head"
	@echo "  alembic-docker-current"

	@echo "\nDocker commands:"
	@echo "  docker-build"
	@echo "  docker-remove"
	@echo "  docker-run"
	@echo "  docker-stop"
	@echo "  docker-compose-up"
	@echo "  docker-compose-down"
	@echo ""
	@echo "Docker Mode (All services in containers):"
	@echo "  docker-mode                  # Start FastAPI, Postgres, MongoDB in Docker"
	@echo "  docker-mode-stop             # Stop Docker mode"
	@echo "  docker-logs                  # View FastAPI logs in Docker mode"
	@echo ""
	@echo "Local DB Mode (Local Postgres + Docker MongoDB/FastAPI):"
	@echo "  local-db-mode                # Start FastAPI, MongoDB in Docker (use local Postgres)"
	@echo "  local-db-mode-stop           # Stop Local DB mode"
	@echo "  local-db-logs                # View FastAPI logs in Local DB mode"

	@echo "\nEnvironment (.env) Management commands:"
	@echo "  create-dot-env-file"
	@echo "  look-at-env-example"
	@echo "  source-env"

	@echo "\nGeneral commands:"
	@echo "  help"

	@echo "\nPoetry commands:"
	@echo "  poetry-add-group"
	@echo "  poetry-add-package"
	@echo "  poetry-add-requirements-txt"
	@echo "  poetry-config-list"
	@echo "  poetry-env-info"
	@echo "  poetry-env-info-path"
	@echo "  poetry-env-list"
	@echo "  poetry-env-remove-all"
	@echo "  poetry-export-to-requirements"
	@echo "  poetry-install"
	@echo "  poetry-install-all-extras"
	@echo "  poetry-install-extras"
	@echo "  poetry-install-no-root"
	@echo "  poetry-install-only"
	@echo "  poetry-install-only-root"
	@echo "  poetry-install-sync"
	@echo "  poetry-install-with"
	@echo "  poetry-install-without"
	@echo "  poetry-lock"
	@echo "  poetry-lock-no-update"
	@echo "  poetry-lock-update"
	@echo "  poetry-pip-freeze"
	@echo "  poetry-pip-freeze-to-txt-file"
	@echo "  poetry-remove-group"
	@echo "  poetry-remove-lock-file"
	@echo "  poetry-remove-package"
	@echo "  poetry-shell"
	@echo "  poetry-show-latest-top-level"
	@echo "  poetry-update"
	@echo "  poetry-update-dry-run"
	@echo "  poetry-version"

	@echo "\nPylint commands:"
	@echo "  isort-src"
	@echo "  black-src"
	@echo "  pylint-app"
	@echo "  pylint-path"

	@echo "\nPytest commands:"
	@echo "  pytest"

	@echo "\nUvicorn commands:"
	@echo "  uvicorn-run"
	@echo "  uvicorn-run-app-on-port"

	@echo "\nSphinx commands:"
	@echo "  sphinx-apidoc"
	@echo "  sphinx-build-html"
	@echo "  sphinx-build-html-for-gh-pages"
	@echo "  sphinx-clean-up"
	@echo "  sphinx-coverage-report"
	@echo "  sphinx-gen-docs"
	@echo "  sphinx-gen-docs-and-coverage"
	@echo "  sphinx-regen-docs"
	@echo "  sphinx-regen-docs-and-coverage"



# --- General Commands -------------------------------------------------------
create-dot-env-file: # Create the .env file for environment variables to be set from.
	@if [ -f .env ]; then \
		echo "File .env already exists. No action taken."; \
	else \
		cp .env.example .env; \
		echo "File .env created successfully from .env.example."; \
		echo "Be sure to update the .env file with your own values for the environment variables."; \
	fi

source-env:  # Source the .env file
	@if [ -f .env ]; then \
		source .env; \
		echo "Sourced .env file."; \
	else \
		echo "Error: .env file not found."; \
		exit 1; \
	fi

look-at-env-example:  # Show the .env.example file
	cat .env.example


# --- POETRY Commands --------------------------------------------------------
poetry-version:  # Show poetry version
	poetry --version

poetry-config-list:  # List all the configuration settings
	poetry config --list

poetry-shell:  # Start the virtual environment shell
	poetry shell

# poetry install commands
poetry-install:  # Install the dependencies
	poetry install

poetry-install-all-extras:  # Install all the extras dependencies
	poetry install --all-extras

poetry-install-extras:  # Install the extras dependency group
	@read -p "Enter the extras dependency group to install: " package_name; \
	poetry install --extras $$package_name

poetry-install-with:  # Install the package group with the dependencies
	@read -p "Enter the package group name to install with: " package_name; \
	poetry install --with $$package_name

poetry-install-no-root:  # Install the dependencies without the root package
	poetry install --no-root

poetry-install-only-root:  # Install only the root package
	poetry install --only-root

poetry-install-only:  # Install only the package
	@read -p "Enter the package name to install: " package_name; \
	poetry install --only $$package_name

poetry-install-without:  # Install the package without the dependencies
	@read -p "Enter the package name to install without: " package_name; \
	poetry install --without $$package_name

poetry-install-sync:  # Install the dependencies and sync the lock file
	poetry install --sync

# Poetry lock file commands
poetry-lock:  # Lock the dependencies
	poetry lock

poetry-lock-update:  # Update the lock file
	poetry lock --update

poetry-lock-no-update:  # Lock the dependencies without updating the lock file
	poetry lock --no-update

poetry-update:  # Update the dependencies
	poetry update

poetry-update-dry-run:  # Update the dependencies without installing
	poetry update --dry-run

# poetry environment management commands
poetry-env-list:  # List all the environments
	poetry env list

poetry-env-info:  # Show the info of the virtual environment poetry manages
	poetry env info

poetry-env-info-path:  # Show the path of the  virtual environment
	poetry env info --path

poetry-env-remove-all:  # Remove all the environments
	poetry env remove --all

# poetry package management commands
poetry-add-package:  # Add the package
	@read -p "Enter the package name to add: " package; \
	poetry add $$package

poetry-remove-package:  # Remove the package
	@read -p "Enter the package name to remove: " package; \
	poetry remove $$package

poetry-add-group:  # Add the group
	@read -p "Enter the group name to add: " group_name; \
	poetry add --group $$group_name

poetry-remove-group:  # Remove the group
	@read -p "Enter the group name to remove: " group_name; \
	poetry remove --group $$group_name

poetry-remove-lock-file:  # Remove the lock file
	rm -f poetry.lock

poetry-show-latest-top-level:  # Show the latest top-level package
	poetry show --latest --top-level

# poetry export plugin https://pypi.org/project/poetry-plugin-export/
poetry-export-to-requirements:  # Export the dependencies to a requirements file
	poetry export -f requirements.txt --output requirements.txt --without-hashes

poetry-pip-freeze:  # Show the pip freeze
	poetry run pip freeze

poetry-pip-freeze-to-txt-file:  # Show the pip freeze
	poetry run pip freeze > requirements.txt

poetry-add-requirements-txt:  # Add the requirements file
	@read -p "Enter the requirements file path to add: " requirements_file; \
	poetry add cat(requirements.txt)



# --- Testing & Linting Commands ---------------------------------------------
pytest:  # Run the pytest
	poetry run pytest --verbose

isort-src:  # Run isort on src directory
	poetry run isort src/

black-src:  # Run black on src directory
	poetry run black src/

pylint-app:  # Run the pylint on the src directory
	poetry run pylint --verbose src

pylint-path:  # Run the pylint on the path
	@read -p "Enter the path to run the pylint: " path; \
	poetry run pylint --verbose $$path



# --- FastAPI UVICORN Commands -----------------------------------------------
uvicorn-run:  # Run the FastAPI app using Uvicorn
	poetry run uvicorn src.main:app --reload

uvicorn-run-app-on-port:  # Run the command in the virtual environment
	@read -p "Enter the PORT you like the application to run on: " port; \
	poetry run uvicorn src.main:app --reload --port $$port



# --- Alembic Commands -------------------------------------------------------
alembic-init:  # Initialize the Alembic
	@read -p "Enter the Alembic directory path: " directory_path; \
	poetry run alembic init "$$directory_path"

alembic-init-template:  # Initialize the Alembic with a template
	poetry run tree . -d
	@read -p "Enter the Alembic directory path: " directory_path; \
	poetry run alembic list_templates
	@read -p "Enter the alembic template name: " template_name; \
	poetry run alembic init "$$directory_path" --template $$template_name

alembic-revision:  # Create a new revision
	@read -p "Enter the revision message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"

alembic-revision-and-upgrade:  # Create a new revision and upgrade
	@read -p "Enter the revision message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"
	poetry run alembic upgrade head

alembic-upgrade:  # Upgrade to the head
	poetry run alembic upgrade head

alembic-downgrade:  # Downgrade to the previous version
	poetry run alembic downgrade -1

alembic-show-history:  # Show the alembic history
	poetry run alembic history

alembic-show-current:  # Show the current revision
	poetry run alembic current

alembic-show-heads:  # Show the alembic heads
	poetry run alembic heads

alembic-show-branches:  # Show the alembic branches
	poetry run alembic branches

alembic-list-templates:  # List the available templates
	poetry run alembic list_templates

alembic-show-revision-details:  # Show the Alembic configuration
	poetry run alembic history
	@read -p "Enter the revision id: " revision_id; \
	poetry run alembic show $$revision_id

alembic-help:  # Show the Alembic help
	poetry run alembic --help

alembic-docker-upgrade-current:  # Start Docker services and run Alembic upgrade+current inside fastapi_server
	@echo "Running Alembic in Docker mode (.env.docker)..."
	docker compose --env-file .env.docker up -d postgres_db fastapi_server
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic upgrade head
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic current

alembic-docker-revision:  # Create a manual Alembic revision in Docker (requires MSG="...")
	@test -n "$(MSG)" || (echo "Usage: make alembic-docker-revision MSG=your_message" && exit 1)
	docker compose --env-file .env.docker up -d postgres_db fastapi_server
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic revision -m "$(MSG)"

alembic-docker-revision-auto:  # Create autogen Alembic revision in Docker (requires MSG="...")
	@test -n "$(MSG)" || (echo "Usage: make alembic-docker-revision-auto MSG=your_message" && exit 1)
	docker compose --env-file .env.docker up -d postgres_db fastapi_server
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic revision --autogenerate -m "$(MSG)"
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic current

alembic-docker-upgrade:  # Upgrade Alembic in Docker (optional REV, default=head)
	docker compose --env-file .env.docker up -d postgres_db fastapi_server
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic upgrade $(if $(REV),$(REV),head)
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic current

alembic-docker-current:  # Show current Alembic revision in Docker
	docker compose --env-file .env.docker up -d postgres_db fastapi_server
	docker compose --env-file .env.docker exec fastapi_server poetry run alembic current



# --- Docker Commands --------------------------------------------------------
docker-build:  # Build the Docker image
	docker build -t fastapi-app .

docker-run:  # Run the Docker container
	docker run -d --name fastapi-app -p 8000:8000 fastapi-app

docker-stop:  # Stop the Docker container
	docker stop fastapi-app

docker-remove:  # Remove the Docker container
	docker rm fastapi-app

docker-compose-up:  # Run the Docker compose environment
	docker-compose up

docker-compose-down:  # Stop the Docker compose environment
	docker-compose down

# --- Docker Mode Commands (Postgres + MongoDB + FastAPI in containers) -----
docker-mode:  # Start all services in Docker (FastAPI, Postgres, MongoDB)
	@echo "🐳 Starting Docker mode (isolated Docker volumes)..."
	docker compose --env-file .env.docker up -d postgres_db mongo_db fastapi_server
	@echo "✅ Docker mode started!"
	@echo "📊 FastAPI: http://localhost:1337"
	@echo "🐘 Postgres: postgres_db:5432"
	@echo "🍃 MongoDB: mongo_db:27017"
	@echo ""
	@echo "View logs with: make docker-logs"

docker-mode-stop:  # Stop Docker mode services
	@echo "🛑 Stopping Docker mode..."
	docker compose --env-file .env.docker down
	@echo "✅ Docker mode stopped!"

docker-logs:  # View FastAPI logs in Docker mode
	docker compose --env-file .env.docker logs -f fastapi_server

# --- Local DB Mode Commands (Local Postgres + Docker MongoDB/FastAPI) -------
local-db-mode:  # Start FastAPI and MongoDB in Docker, connect to local Postgres
	@echo "🏠 Starting Local DB mode (Docker FastAPI+MongoDB, local Postgres)..."
	@echo "ℹ️  Ensure local Postgres is running on 127.0.0.1:5432"
	docker compose --env-file .env.localdb -f docker-compose.yml -f docker-compose.localdb.yml up -d
	@echo "✅ Local DB mode started!"
	@echo "📊 FastAPI: http://localhost:1337"
	@echo "🐘 Postgres: 127.0.0.1:5432 (local)"
	@echo "🍃 MongoDB: mongo_db:27017 (Docker)"
	@echo ""
	@echo "View logs with: make local-db-logs"

local-db-mode-stop:  # Stop Local DB mode services
	@echo "🛑 Stopping Local DB mode..."
	docker compose -f docker-compose.yml -f docker-compose.localdb.yml down
	@echo "✅ Local DB mode stopped!"

local-db-logs:  # View FastAPI logs in Local DB mode
	docker compose -f docker-compose.yml -f docker-compose.localdb.yml logs -f fastapi_server



# --- Sphinx Commands --------------------------------------------------------
sphinx-apidoc:  # Generate Sphinx .rst files
	poetry run sphinx-apidoc -o docs/sphinx/source/rst/api src/api
	poetry run sphinx-apidoc -o docs/sphinx/source/rst/core src/core
	poetry run sphinx-apidoc -o docs/sphinx/source/rst/db src/db
	poetry run sphinx-apidoc -o docs/sphinx/source/rst/middlewares src/middlewares
	poetry run sphinx-apidoc -o docs/sphinx/source/rst/utils src/utils
	echo "Sphinx .rst files generated successfully!"

#sphinx-apidoc:  # Generate Sphinx .rst files
#	poetry run sphinx-apidoc -o docs/sphinx/source/ src/

sphinx-build-html:  # Build the Sphinx HTML documentation
	poetry run sphinx-build -b html -d docs/sphinx/build/doctrees docs/sphinx/source docs/sphinx/build/html

sphinx-build-html-for-gh-pages:  # Build the Sphinx HTML documentation
	poetry run sphinx-build -b html -d docs/sphinx/build/doctrees docs/sphinx/source gh-pages

sphinx-coverage-report:  # Generate a documentation coverage report
	poetry run sphinx-build -M coverage docs/sphinx/source docs/sphinx/build

sphinx-clean-up:  # Clean up all Sphinx generated files
	rm -rf docs/sphinx/build/*
	rm -rf docs/sphinx/source/rst

sphinx-gen-docs: sphinx-apidoc sphinx-build-html  # Generate Sphinx documentation
	@echo "Sphinx documentation generated successfully!"

sphinx-gen-docs-and-coverage: sphinx-apidoc sphinx-build-html sphinx-coverage-report  # Generate Sphinx documentation
	@echo "Sphinx documentation and coverage report generated successfully!"

sphinx-regen-docs: sphinx-clean-up sphinx-apidoc sphinx-build-html  # Regenerate Sphinx documentation
	@echo "Sphinx documentation regenerated successfully!"

sphinx-regen-docs-and-coverage: sphinx-clean-up sphinx-apidoc sphinx-build-html sphinx-coverage-report # Regenerate Sphinx documentation
	@echo "Sphinx documentation and coverage report was regenerated successfully!"
