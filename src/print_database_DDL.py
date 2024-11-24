import os
import sys

from sqlalchemy import create_mock_engine

from restaurant_app.infrastructure.environment import setup_environment
from restaurant_app.store.database import Base


# the function is used to get the DDL from sqlalchemy and print the SQL
def dump_ddl(sql, *multiparams, **params):
    """print the DDL string"""
    print(sql.compile(dialect=engine.dialect))


if __name__ == "__main__":
    # setup environment to also get data from dotenv
    setup_environment("./")

    # retrieve the database URL from the environment
    db_url = os.getenv("DATABASE_URI")
    if db_url is None or db_url == "":
        CRED = "\033[91m"
        CEND = "\033[0m"
        print(CRED + "Error: 'DATABASE_URI' environment variable is NOT available!" + CEND)
        sys.exit(-1)

    engine = create_mock_engine(db_url, dump_ddl)
    Base.metadata.create_all(engine, checkfirst=False)
