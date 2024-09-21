import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ..infrastructure.logger import LOG

bp = Blueprint("auth", __name__)


@bp.get("/login-required")
def show_login():
    """show the login form if there is no authenticated user available"""
    LOG.info("view auth/login-required")

    return render_template("auth/login.html")


@bp.get("/logout")
def logout():
    """show the login form if there is no authenticated user available"""
    LOG.info("view auth/logout")
    session.clear()
    return redirect("/")


@bp.post("/login")
def login():
    """this is a very, very simple login/auth method which does not really validate the user.
    in reality one would use a real authentication system!!
    """
    LOG.info("view auth/login")
    login_email = request.form.get("login.email")
    if login_email is None or login_email == "":
        # redirect to the login-form again
        flash("No email was supplied!")
        return redirect(url_for("auth.show_login"))

    session.clear()
    session["user"] = login_email
    return redirect("/")


@bp.before_app_request
def load_logged_in_user():
    if session.get("user") is None:
        g.user = "Anonymous"
    else:
        g.user = session.get("user")


def login_required(view):
    """a decorator which redirects to the auth form to perform a login"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user") is None:
            return redirect(url_for("auth.show_login"))
        return view(**kwargs)

    return wrapped_view
