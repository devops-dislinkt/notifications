from app.models import Notification
from app.database import create, delete_instance
import requests
from os import environ

URL = f"http://{environ['SERVICE_HOST']}:{environ['SERVICE_PORT']}/api/profile/following?approved=true"

def get_all_following(follower_username):
    try:
        response = requests.get(URL, headers={'user': follower_username})
        json = response.json()
        if response.status_code != 200:
            print(f"Api responded with code: {response.status_code}")
            return None
        return json
    except Exception as err:
        print(f"An error occured : f{err}")
        return None

def toggle_notif(observed_username: str, subscriber_username: str):

    list = get_all_following(subscriber_username)
    if not is_following(list, observed_username):
        raise Exception("User can not update notifications status for non follower.")

    notif_object = Notification.query.get((subscriber_username, observed_username))

    if (not notif_object):
        create(Notification({ 'subscriber_username' : subscriber_username, 'observed_username': observed_username}))
    else:
        delete_instance(notif_object)


def is_following(list, username_to_find):
    """Checks if username_to_find exist in given list."""
    for req in list:
        if req['following'][0]['username'] == username_to_find:
            return True

    return False