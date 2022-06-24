from flask import Blueprint, request
from app import service
from flask import render_template, jsonify

api = Blueprint("api", __name__)  # private -> requires login


@api.get("/")
def na():
    return render_template("index.html")


@api.post("/notifications/<string:observed_username>")
def toggle_notif_profile(observed_username: str):
    user: str = request.headers.get("user")
    try:
        service.toggle_notif(observed_username, user)

        return "Notification status updated", 200
    except Exception as err:
        return "Not valid params: {}".format(err), 404


@api.get('/notifications/<string:observed_username>')
def get_notif_status(observed_username: str):
    '''
    Get current notification status for observed username. 
    Does currently logged in user has turned on or turned off 
    notifications for observed user?
    If notif turned on returns true, if notif turned off returns false.
    '''
    user: str = request.headers.get('user')
    try:
        is_notif_turned_on = service.get_notif_status(observed_username, user)
        return jsonify(is_notif_turned_on)
    except Exception as err:
        return "Not valid params: {}".format(err), 404
