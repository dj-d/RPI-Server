import requests

URL = "http://192.168.0.206"

tv = "/tv"
sound = "/soundbar"
last_selection = "/last_selections"


def send_command(device, action):
    try:
        return requests.get(url=URL + device, params=action).text
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400


def get_status():
    try:
        return requests.get(url=URL + sound + last_selection).json()
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400
