from flask import Flask, jsonify, request
import NasControl as nas
import RelayControl as relay
import RGBStripControl as rgb

# CONSTANT
port = 80
host = "0.0.0.0"
enableDebug = True

app = Flask(__name__)

relay.init()
rgb.init()


@app.route("/", methods=["POST"])
def main():
    return "Main"


@app.route("/turn_on_nas", methods=["POST"])
def turn_on_nas():
    nas.turn_on()


@app.route("/get_relay_pin", methods=["POST"])
def get_relay_pin():
    data = relay.get_pin()

    return jsonify(data)


@app.route("/turn_on", methods=["POST"])
def turn_on():
    data = request.args.get('in')
    pin = int(data)

    relay.turn_on(pin)

    return "Acceso in: " + str(pin)


@app.route("/turn_off", methods=["POST"])
def turn_off():
    data = request.args.get('in')
    pin = int(data)

    relay.turn_off(pin)

    return "Spento in: " + str(pin)


@app.route("/get_rgb_pin", methods=["POST"])
def get_rgb_pin():
    data = rgb.get_pin()

    return jsonify(data)


if __name__ == "__main__":
    app.run(host=host, port=port, debug=enableDebug)
