import datetime
import os

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from restaurant_app import create_app

from ..shared.view_helpers import get_hash_value
from ..store.entities import AddressEntity, RestaurantEntity
from ..store.restaurant_repository import RestaurantRepository


@pytest.fixture()
def app() -> Flask:  # type: ignore
    # overwrite config-values via environment
    # use sqlite database in memory
    os.environ["DATABASE_URI"] = "sqlite://"
    # define a test-secret
    os.environ["SECRET_KEY"] = "very-secret"

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    # initialize the database for the tests
    db = app.container.db()
    db.drop_database()
    db.create_database()

    # fill the database with some defined values - start with the restaurant
    restaurant_repo = RestaurantRepository(db.managed_session)

    def in_transaction(session: Session):
        repo = restaurant_repo.new_session(session)
        repo.save(RestaurantEntity(
            name="Restaurant-Test-Name",
            open_from=datetime.time(10, 0, 0),
            open_until=datetime.time(22, 0, 0),
            open_days="TUESDAY;WEDNESDAY",
            address=AddressEntity(street="Teststrasse 1", city="Salzburg", zip="5020", country="AT")
        ))

    restaurant_repo.unit_of_work(in_transaction)

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_routes_without_session_login(client: FlaskClient):
    # without a login any call should be redirected to login-required
    response = client.get("/restaurants")
    assert response.headers.get("Location") == "/login-required"

    response = client.get("/restaurant/1")
    assert response.headers.get("Location") == "/login-required"


def test_login(client: FlaskClient):
    response = client.post("/login", data={"login.email": "test@email.com", "login.password": "12345678"})
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302
    assert response.status_code == 302  # HTTP-OK
    assert response.headers.get("Location") == "/"  # redirect to start-page

    # if no email-address was supplied an error is shown
    # note: there still is a redirect to login-required
    response = client.post("/login", data={"login.email": "", "login.password": ""}, follow_redirects=True)
    assert len(response.history) == 1
    assert "No email was supplied!" in response.text


def test_restaurant_list(client: FlaskClient):
    with client:
        # we use the login to have a valid session!
        client.post(
            "/login",
            data={
                "login.email": "test@email.com",
            },
            follow_redirects=True,
        )

        # very roughly validate the restaurant-view
        response = client.get("/restaurants")
        assert response.status_code == 200
        assert "List of restaurants" in response.text
        assert "Restaurant-Test-Name" in response.text


def test_restaurant_edit(client: FlaskClient):
    with client:
        # we use the login to have a valid session!
        client.post(
            "/login",
            data={
                "login.email": "test@email.com",
            },
            follow_redirects=True,
        )

        # show the edit-restaurant view
        response = client.get(f"/restaurant/1?h={get_hash_value("1")}")
        assert response.status_code == 200
        assert "Restaurant:" in response.text

        # without the hash-value a 400 http status-code should be returned
        response = client.get("/restaurant/1")
        assert response.status_code == 400  # bad-request
        assert "the value does not match the supplied hash" in response.text

        # invalid restaurant-id
        response = client.get(f"/restaurant/999999?h={get_hash_value("999999")}")
        assert response.status_code == 404
        assert "cannot find restaurant by id '999999'" in response.text
