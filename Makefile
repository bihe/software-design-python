PROJECTNAME=$(shell basename "$(PWD)")

# Make is verbose in Linux. Make it silent.
MAKEFLAGS += --silent

VERSION="1.0.0-"
COMMIT=`git rev-parse HEAD | cut -c 1-8`
BUILD=`date -u +%Y%m%d.%H%M%S`

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)


## set the default architecture should work for most Linux systems
ARCH := amd64

UNAME_M := $(shell uname -m)
ifeq ($(UNAME_M), x86_64)
	ARCH = amd64
endif
ifeq ($(UNAME_M), arm64)
	ARCH = arm64
endif


.PHONY: all run run-flask class-diagram create-db

all: help

# ---------------------------------------------------------------------------
# application tasks
# ---------------------------------------------------------------------------

run: ## run the python application
	@echo "  >  executing flask application"
	python src/run.py

run-flask: ## run the application using flask
	@echo "  >  executing flask application"
	flask --app src/restaurant_app run

test: ## run the unit-tests of the application
	@echo "  >  run unit tests"
	pytest --cov

class-diagram: ## generate a class-diagram with pyreverse
	@echo "  >  generate a class-diagram with pyreverse"
	pyreverse -o plantuml --verbose --colorized --ignore=restaurant_repository_test.py --ignore=service_test.py --ignore=menu_repository_test.py --ignore=repository_test_helpers.py --ignore=reservation_repo_test.py --ignore=table_repo_test.py -p restaurant_app -d ./doc ./src/restaurant_app

db-create: ## create the database based on the models
	@echo "  >  create the database / update models"
	flask --app src/restaurant_app db create app.db

db-import: ## import initial data into database
	@echo "  >  import initial data from 'initial_restaurant_data.json'"
	flask --app src/restaurant_app db import ./data/initial_restaurant_data.json

container-build: ## build container image of the restaurant-app
	@echo "  >  build the container-image"
	docker build -t restaurant_app -f ./container/Dockerfile -t restaurant_app .

container-run: ## run the estaurant-app container
	@echo "  >  run the container-image"
	docker stop restaurant-app && docker rm restaurant-app && docker run -p 9000:9000 --name restaurant-app restaurant_app

## Help:
help: ## Show this help.
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} { \
		if (/^[a-zA-Z_-]+:.*?##.*$$/) {printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2} \
		else if (/^## .*$$/) {printf "  ${CYAN}%s${RESET}\n", substr($$1,4)} \
		}' $(MAKEFILE_LIST)
