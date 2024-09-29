import pytest
from flask import Flask
from flask.testing import FlaskClient

from restaurant_app import create_app

from ..shared.view_helpers import get_hash_value


@pytest.fixture()
def app() -> Flask:  # type: ignore
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

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
        assert "The Restaurant Name" in response.text


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
