<#
.SYNOPSIS
The powershell 'cli.ps1' scipt provides the most-often used commands for this application in a convenient was.

.DESCRIPTION
USAGE
    .\cli.ps1 <command>

COMMANDS
    run                 execute the flask-application via src/run.py
    run-flask           exectue the flask-application as a flask-app via flask and --app
    test                run unit-tests of the application via pytest
    class-diagram       generate class-diagrams of the application via pyreverse (output as plantuml)
    db-create           generate the database schema based on the code-first approach through SqlAlchemy
    db-import           import initial data into the database vai ./data/initial_restaurant_data.json
    container-build     create container-image of the application
    container-run       run the application container
    help, -?            show this help message
#>
param(
  [Parameter(Position=0)]
  [ValidateSet("run", "run-flask", "test", "class-diagram", "db-create", "db-import", "container-build", "container-run", "help")]
  [string]$Command
)

function Command-Help { Get-Help $PSCommandPath }

function Command-run {
    Write-Host "  >  executing flask application" -ForegroundColor Blue
    iex "python src/run.py"
}

function Command-run-flask {
    Write-Host "  >  executing flask application as a module" -ForegroundColor Blue
    iex "flask --app src/restaurant_app run"
}

function Command-test {
    Write-Host "  >  run unit tests" -ForegroundColor Blue
    iex "pytest --cov --cov-report=lcov:lcov.info --cov-report=term"
}

function Command-class-diagram {
    Write-Host "  >  generate a class-diagram with pyreverse" -ForegroundColor Blue
	iex "pyreverse -o plantuml --verbose --colorized --ignore=restaurant_repository_test.py --ignore=service_test.py --ignore=menu_repository_test.py --ignore=repository_test_helpers.py --ignore=reservation_repo_test.py --ignore=table_repo_test.py -p restaurant_app -d ./doc ./src/restaurant_app"
}

function Command-db-create {
    Write-Host "  >  create the database / update models" -ForegroundColor Blue
    iex "flask --app src/restaurant_app db create app.db"
}

function Command-db-import {
    Write-Host "  >  import initial data from 'initial_restaurant_data.json'" -ForegroundColor Blue
    iex "flask --app src/restaurant_app db import ./data/initial_restaurant_data.json"
}

function Command-container-build {
    Write-Host "  >  build the container-image" -ForegroundColor Blue
    iex "docker build -t restaurant_app -f ./container/Dockerfile ."
}

function Command-container-run {
    Write-Host "  >  run the container-image" -ForegroundColor Blue
    iex "docker stop restaurant-app || true && docker rm restaurant-app || true && docker run -p 9000:9000 --name restaurant-app restaurant_app"
}


if (!$Command) {
    Command-Help
    exit
}

switch ($Command) {
    "run" { Command-run }
    "run-flask" { Command-run-flask }
    "test" { Command-test }
    "class-diagram" { Command-class-diagram }
    "db-create" { Command-db-create }
    "db-import" { Command-db-import }
    "container-build" { Command-container-build }
    "container-run" { Command-container-run }
    "help"  { Command-Help }
}
