# A multi-stage build docker file
# https://docs.docker.com/build/building/multi-stage/
#
# the first) stage is used to build the application
# the main advantage is, that NO build-tools need to be available locally
# everything is done "inside" the image
#
# there are a couple of images available: https://hub.docker.com/_/python/

FROM python:3.12-alpine AS builder

# define a place where the output of the build is put
WORKDIR /app

# initial project setup
COPY pyproject.toml .
COPY src ./src
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip --quiet --no-cache-dir install --upgrade pip && \
    pip --quiet --no-cache-dir install --no-cache-dir . && \
    pip --quiet --no-cache-dir install PyMySQL && \
    pip --quiet --no-cache-dir install gunicorn

# ---------------------------------------------------------------------------
# the second) stage is used for runtime/production
FROM python:3.12-alpine
WORKDIR /opt/restaurant_app

# Copy the installed dependencies and app from the previous stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# still we needs some additional stuff
# we need mariadb library (very, very similar to mysql) to access the db
RUN apk add --no-cache mariadb-connector-c

# it is a best practise to create a seperate user and not execute everything with root
RUN addgroup -g 1000 -S restaurant-app-user && \
    adduser -u 1000 -S restaurant-app-user -G restaurant-app-user -H -h /opt/restaurant_app

# copy our project to the application directory
RUN chown restaurant-app-user /opt/restaurant_app
COPY --chown=restaurant-app-user ./app.db /opt/restaurant_app/app.db
COPY --from=builder --chown=restaurant-app-user /app/src/run.py /opt/restaurant_app/run.py
COPY --from=builder --chown=restaurant-app-user /app/src/restaurant_app /opt/restaurant_app/restaurant_app
COPY --chown=restaurant-app-user ./container/run_gunicorn.py /opt/restaurant_app/run_gunicorn.py

# some minor hardening; remove things
RUN rm -rf /usr/sbin && rm -rf /usr/bin && rm -rf /etc/apk && rm -rf /etc/fstab && rm -rf /usr/share/apk && rm -rf /sbin && rm -rf /bin

USER restaurant-app-user
EXPOSE 9000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=9000

#CMD ["/usr/local/bin/python3.12", "/opt/restaurant_app/run.py"]
CMD ["/usr/local/bin/python3.12", "/opt/restaurant_app/run_gunicorn.py", "-w", "4", "-b", "0.0.0.0:9000", "restaurant_app:create_app()"]

