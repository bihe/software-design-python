# A multi-stage build docker file
# https://docs.docker.com/build/building/multi-stage/
#
# the first) stage is used to build the application
# the main advantage is, that NO build-tools need to be available locally
# everything is done "inside" the image
#
# there are a couple of images available: https://hub.docker.com/_/python/

FROM python:3.12-bookworm AS builder

# define a place where the output of the build is put
WORKDIR /app

# initial project setup
COPY pyproject.toml .
COPY src ./src

RUN pip install --upgrade pip
RUN pip install --no-cache-dir .
# we need mysql/mariadb support
RUN pip install PyMySQL

# ---------------------------------------------------------------------------
# the second) stage is used for runtime/production
# we have now a different base-image which is smaller for production
FROM python:3.12-slim-bookworm

WORKDIR /opt/restaurant_app

# Copy the installed dependencies and app from the previous stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# still we needs some additional stuff
# we need mariadb library (very, very similar to mysql) to access the db
# this is the runtime library dependency of mysqlclient
RUN apt-get update && apt-get install -y libmariadb3
RUN pip install gunicorn

# it is a best practise to create a seperate user and not execute everything with root
RUN useradd -d /opt/restaurant_app restaurant-app-user

# copy our project to the application directory
RUN chown restaurant-app-user /opt/restaurant_app
COPY --chown=restaurant-app-user ./app.db /opt/restaurant_app/app.db
COPY --chown=restaurant-app-user ./static /opt/restaurant_app/static
COPY --chown=restaurant-app-user ./templates /opt/restaurant_app/templates
COPY --from=builder --chown=restaurant-app-user /app/src/run.py /opt/restaurant_app/run.py
COPY --from=builder --chown=restaurant-app-user /app/src/restaurant_app /opt/restaurant_app/restaurant_app

USER restaurant-app-user
EXPOSE 9000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=9000

#CMD ["python","run.py"]
CMD ["gunicorn","-w", "4", "-b", "0.0.0.0:9000", "restaurant_app:create_app()"]
