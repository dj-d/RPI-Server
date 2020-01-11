from flask import Flask, jsonify, request
from services import PowerStrip as pStrip, RemoteController as controller, \
    RGBController as rgbController
from services.login_service import LoginService
from models.user_models import Schema

REQUEST_ERROR = "Request error"
CONNECTION_ERROR = "Device connection error"

domain = "YOUR_DOMAIN"

host = "0.0.0.0"
port = 5000
debug = True

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return "It working..."


# RGB
@app.route(rgbController.rgb + rgbController.relay, methods=["POST"])
def rgb_smart():
    if is_valid_api_key(request.headers.get("api_key")):
        action = request.args.get("action")
        pin = request.args.get("in")

        params = {'action': action, 'in': pin}

        cmd = rgbController.send_smart_command(params=params)

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


@app.route(rgbController.rgb + rgbController.relay + rgbController.status, methods=["POST"])
def rgb_relay_status():
    if is_valid_api_key(request.headers.get("api_key")):
        cmd = rgbController.get_smart_status()

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


@app.route(rgbController.rgb, methods=["POST"])
def rgb():
    if is_valid_api_key(request.headers.get("api_key")):
        red = request.args.get("red")
        green = request.args.get("green")
        blue = request.args.get("blue")

        params = {'red': red, 'green': green, 'blue': blue}

        cmd = rgbController.send_rgb_command(params=params)

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


@app.route(rgbController.rgb + rgbController.status, methods=["POST"])
def rgb_status():
    if is_valid_api_key(request.headers.get("api_key")):
        cmd = rgbController.get_rgb_status()

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


# Power strips
@app.route(pStrip.smart, methods=["POST"])
def power_strip():
    if is_valid_api_key(request.headers.get("api_key")):
        num = request.args.get("num")
        action = request.args.get("action")
        pin = request.args.get("in")

        params = {'action': action, 'in': pin}

        if num == "one":
            cmd = pStrip.send_command(pStrip.URL_ONE, params)
        elif num == "two":
            cmd = pStrip.send_command(pStrip.URL_TWO, params)
        else:
            return response_request_error()

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


@app.route(pStrip.smart + pStrip.status, methods=["POST"])
def power_strip_status():
    if is_valid_api_key(request.headers.get("api_key")):
        num = request.args.get("num")

        if num == "one":
            cmd = pStrip.get_status(pStrip.URL_ONE)
        elif num == "two":
            cmd = pStrip.get_status(pStrip.URL_TWO)
        else:
            return response_request_error()

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


# TV API
@app.route(controller.tv, methods=["POST"])
def tv():
    if is_valid_api_key(request.headers.get("api_key")):
        action = {'action': request.args.get("action")}

        cmd = controller.send_command(controller.tv, action)

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


# SOUNDBAR API
@app.route(controller.sound, methods=["POST"])
def sound_bar():
    if is_valid_api_key(request.headers.get("api_key")):
        action = {'action': request.args.get("action")}

        cmd = controller.send_command(controller.sound, action)

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


@app.route(controller.sound + controller.last_selection, methods=["POST"])
def sound_bar_last_status():
    if is_valid_api_key(request.headers.get("api_key")):
        cmd = controller.get_status()

        if not cmd:
            return response_request_error()
        elif cmd == 500:
            return response_connection_error()
        else:
            return make_response(True, cmd, 200)
    else:
        return response_request_error()


# SIGN-IN API
@app.route("/signup", methods=["POST"])
def sign_up():
    req_data = request.get_json(force=True)
    api_key = LoginService().create_user(req_data['name'], req_data['surname'], req_data['email'], req_data['password'])
    if not api_key:
        return make_response(False, 'Impossibile completare la registrazione', 500)

    return make_response(True, "OK", 200)


# LOGIN API
@app.route("/login", methods=["POST"])
def login():
    req_data = request.get_json(force=True)
    email = req_data['email']
    api_key = req_data['api_key']
    otp_code = req_data['otp']

    login_service = LoginService()
    if login_service.user_login(email, api_key, otp_code) and login_service.clear_otp(api_key, otp_code):
        return make_response(True, "Ok", 200)
    else:
        login_service.clear_otp(api_key, otp_code)
        return make_response(False, 'Utente non valido', 400)


@app.route("/request-otp", methods=["POST"])
def request_otp():
    req_data = request.get_json(force=True)
    email = req_data['email']
    api_key = req_data['api_key']

    login_service = LoginService()
    if login_service.user_exist(email, api_key):
        if login_service.set_otp_code(email, api_key):
            return make_response(True, 'Mail inviata', 200)
        return make_response(True, 'Errore invio codice otp', 500)
    return make_response(False, 'Utente non valido', 400)


# RESET PASSWORD
@app.route("/reset-password", methods=["POST"])
def send_reset_password():
    req_data = request.get_json(force=True)
    if LoginService().send_reset_pw(req_data['email'], req_data['api_key']):
        return make_response(True, 'Mail inviata', 200)
    else:
        return make_response(False, 'Errore invio mail', 500)


# CHANGE PASSWORD
@app.route("/change-password", methods=["POST"])
def change_password():
    # todo: ritornare form per cambio pw, si portebbe usare l otp dalla mail
    pass


def is_valid_api_key(api_key):
    return LoginService().check_api_key(api_key)


def make_response(is_valid, info, error_code):
    return jsonify({"valid": is_valid, 'info': info}), error_code


def response_request_error():
    return make_response(False, REQUEST_ERROR, 400)


def response_connection_error():
    return make_response(False, CONNECTION_ERROR, 500)


if __name__ == "__main__":
    Schema()
    app.run(host=host, port=port, debug=debug)
