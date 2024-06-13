# Makefile

# Define a variable for the poetry command to keep it DRY
POETRY = poetry
MANAGER = python main.py
PORT = 8008

# Load poetry
.PHONY: load
load:
	export PATH="$$HOME/.local/bin:$$PATH"

# Install dependencies
.PHONY: install
install:
	$(POETRY) install

# Install pre-commit hooks
.PHONE: install-pre-commit
install-pre-commit:
	$(POETRY) run pre-commit uninstall
	$(POETRY) run pre-commit install

# Check code style
.PHONY: lint
lint:
	$(POETRY) run pre-commit run --all-files

# Make migrations
.PHONY: make-migrations
make-migrations:
	$(POETRY) run $(MANAGER) makemigrations

# Execute migrations
.PHONY: execute-migrate
execute-migrate:
	$(POETRY) run $(MANAGER) migrate

# Make and execute migrations
.PHONY: migrate
migrate: make-migrations execute-migrate ;

# Update project dependencies
.PHONY: update
update: install migrate install-pre-commit ;

# Run the Django development server
.PHONY: dev
dev:
	$(POETRY) run $(MANAGER) runserver $(PORT)

# Run the Django development server with a specific port
.PHONY: run
run:
	$(POETRY) run daphne main:asgi --port $(PORT) --bind 0.0.0.0

# Create a superuser
.PHONY: superuser
superuser:
	$(POETRY) run $(MANAGER) createsuperuser
