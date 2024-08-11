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


.PHONY: all run

all: help

# ---------------------------------------------------------------------------
# application tasks
# ---------------------------------------------------------------------------

run: ## run the python application
	@-$(MAKE) -s python-run

run-flask: ## run the application using flask
	@-$(MAKE) -s flask-run

# ---------------------------------------------------------------------------
# internal tasks
# ---------------------------------------------------------------------------

python-run:
	@echo "  >  executing flask application"
	python run_app.py

flask-run:
	@echo "  >  executing flask application"
	flask --app restaurant_app run

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
