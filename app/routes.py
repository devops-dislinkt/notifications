from flask import Blueprint, request
from service import toggle_notif
from flask import render_template

api = Blueprint("api", __name__)  # private -> requires login


@api.get("/")
def na():
    return render_template("index.html")


@api.get("/notifications/<string:observed_username>")
def toggle_notif_profile(observed_username: str):
    user: str = request.headers.get("user")
    try:
        toggle_notif(observed_username, user)

        return "Notification status updated", 200
    except Exception as err:
        return "Not valid params: {}".format(err), 404
