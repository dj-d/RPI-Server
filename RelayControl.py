import RPi.GPIO as GPIO

pin = {
    "in1": 2,
    "in2": 3,
    "in3": 4,
    "in4": 14
}

GPIO.setwarnings(False)


def init():
    GPIO.setmode(GPIO.BCM)

    for i in pin:
        GPIO.setup(pin[i], GPIO.OUT)
        GPIO.output(pin[i], GPIO.HIGH)

    # GPIO.setup(pin["in1"], GPIO.OUT)
    # GPIO.output(pin["in1"], GPIO.HIGH)
    #
    # GPIO.setup(pin["in2"], GPIO.OUT)
    # GPIO.output(pin["in2"], GPIO.HIGH)
    #
    # GPIO.setup(pin["in3"], GPIO.OUT)
    # GPIO.output(pin["in3"], GPIO.HIGH)
    #
    # GPIO.setup(pin["in4"], GPIO.OUT)
    # GPIO.output(pin["in4"], GPIO.HIGH)


def get_pin():
    return pin


def turn_on(pin_num):
    GPIO.output(pin_num, GPIO.LOW)


def turn_off(pin_num):
    GPIO.output(pin_num, GPIO.HIGH)


# DA CONTROLLARE
def pin_verify(pin_num):
    i = 0
    is_pin = False

    while not is_pin & i < len(pin) & pin_num != pin:
        if pin_num != pin[i]:
            i = i + 1
        else:
            is_pin = True

    return is_pin
