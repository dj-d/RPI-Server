import requests

URL_ONE = "http://192.168.0.204"
URL_TWO = "http://192.168.0.205"

smart = "/smart"
status = "/status"


def send_command(url, params):
    try:
        return requests.get(url=url + smart, params=params).text
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400


def get_status(url):
    try:
        return requests.get(url=url + smart + status).json()
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400
