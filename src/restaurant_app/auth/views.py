import functools

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..infrastructure.cache import Cache
from ..infrastructure.container import Container
from ..infrastructure.logger import LOG
from ..shared.view_helpers import clear_session, get_user_from_session, set_user_to_session
from .models import User

bp = Blueprint("auth", __name__)


@bp.get("/login-required")
def show_login():
    """show the login form if there is no authenticated user available"""
    LOG.info("view auth/login-required")
    return render_template("auth/login.html")


@bp.get("/logout")
@inject
def logout(cache: Cache = Provide[Container.cache]):
    """perform a logout and redirect to the root URL"""
    LOG.info("view auth/logout")
    user = get_user_from_session()
    if user is not None:
        clear_session()
    return redirect("/")


@bp.post("/login")
@inject
def login(cache: Cache = Provide[Container.cache]):
    """this is a very, very simple login/auth method which does not really validate the user.
    in reality one would use a real authentication system!!
    """
    LOG.info("view auth/login")
    login_email = request.form.get("login.email")
    if login_email is None or login_email == "":
        # redirect to the login-form again
        flash("No email was supplied!")
        return redirect(url_for("auth.show_login"))

    clear_session()
    user = User(id=1, display_name="Restaurant Admin", email=login_email)
    set_user_to_session(user)
    return redirect("/")


def login_required(view):
    """a decorator which redirects to the auth form to perform a login"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = get_user_from_session()
        if user is not None:
            return view(**kwargs)
        return redirect(url_for("auth.show_login"))

    return wrapped_view
