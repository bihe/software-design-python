import functools

from flask import Blueprint, redirect, render_template, session, url_for

from ..infrastructure.logger import LOG

bp = Blueprint("auth", __name__)


@bp.get("/login-required")
def show_login():
    """show the login form if there is no authenticated user available"""
    LOG.info("view auth/login-required")

    return render_template("auth/login.html")


@bp.post("/login")
def login():
    """this is a very, very simple login/auth method which does not really validate the user.
    in reality one would use a real authentication system!!
    """
    LOG.info("view auth/login")
    session.clear()
    session["user"] = "Restaurant Admin"
    return redirect("/")


def login_required(view):
    """a decorator which redirects to the auth form to perform a login"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user") is None:
            return redirect(url_for("auth.show_login"))
        return view(**kwargs)

    return wrapped_view
