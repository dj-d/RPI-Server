import requests

URL = "http://192.168.0.207"

relay = "/relay"
rgb = "/rgb"
status = "/status"


def send_smart_command(params):
    try:
        return requests.get(url=URL + rgb + relay, params=params).text
    except requests.exceptions.RequestException:
        return 500


def get_smart_status():
    try:
        return requests.get(url=URL + rgb + relay + status).json()
    except requests.exceptions.RequestException:
        return 500


def send_rgb_command(params):
    try:
        return requests.get(url=URL + rgb, params=params).text
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400


def get_rgb_status():
    try:
        return requests.get(url=URL + rgb + status).json()
    except requests.exceptions.ConnectionError:
        return 500
    except requests.exceptions.RequestException:
        return 400
