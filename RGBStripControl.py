import RPi.GPIO as GPIO
from time import sleep

pin = {
    'RED_PIN': 17,
    'GREEN_PIN': 27,
    'BLUE_PIN': 22
}

GPIO.setwarnings(False)


def init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin['RED_PIN'], GPIO.OUT)
    GPIO.setup(pin['GREEN_PIN'], GPIO.OUT)
    GPIO.setup(pin['BLUE_PIN'], GPIO.OUT)

    # for color in pin:
    #     GPIO.setup(pin[color], GPIO.OUT)

    # resetAllColor()


# DA CONTROLLARE
# def valueController(value):
#     if value >= 0 or value <= 255:
#         return True
#
#     return False


def get_pin():
    return pin


def resetAllColor():
    GPIO.output(pin['RED_PIN'], GPIO.LOW)
    GPIO.output(pin['GREEN_PIN'], GPIO.LOW)
    GPIO.output(pin['BLUE_PIN'], GPIO.LOW)


def setRedColor():
    resetAllColor()
    GPIO.output(pin['RED_PIN'], GPIO.HIGH)


def setGreenColor():
    resetAllColor()
    GPIO.output(pin['GREEN_PIN'], GPIO.HIGH)


def setBlueColor():
    resetAllColor()
    GPIO.output(pin['BLUE_PIN'], GPIO.HIGH)


def setWhiteColor():
    resetAllColor()
    GPIO.output(pin['RED_PIN'], GPIO.HIGH)
    GPIO.output(pin['GREEN_PIN'], GPIO.HIGH)
    GPIO.output(pin['BLUE_PIN'], GPIO.HIGH)


def setRedBrightness(value):
    red_pwm = GPIO.PWM(pin['RED_PIN'], 500)
    red_pwm.start(value)


# def setGreenBrightness(value):


def setBlueBrightness(value):
    blue_pwm = GPIO.PWM(pin['BLUE_PIN'], 500)
    blue_pwm.start(value)


init()
resetAllColor()
# green_pwm = GPIO.PWM(pin['GREEN_PIN'], 500)
# green_pwm.start(100)
# green_pwm.ChangeFrequency(50)
# setGreenBrightness(50)

# # QUESTO IN BASSO FUNZIONA, SISTEMARE LE FUNZIONI
# # frequency 500 Hz
# led_pwm = GPIO.PWM(pin['GREEN_PIN'], 500)
#
# # duty cycle = 100
# led_pwm.start(100)
#
# while True:
#     led_pwm.ChangeDutyCycle(100)
#     sleep(1)
#     led_pwm.ChangeDutyCycle(80)
#     sleep(1)
#     led_pwm.ChangeDutyCycle(60)
#     sleep(1)
#     led_pwm.ChangeDutyCycle(40)
#     sleep(1)
#     led_pwm.ChangeDutyCycle(20)
#     sleep(1)
#     led_pwm.ChangeDutyCycle(0)
#     sleep(1)


# init()
#
# setRedColor()
# sleep(1)
# setGreenColor()
# sleep(1)
# setBlueColor()
# sleep(1)
# setWhiteColor()
# sleep(1)
# resetAllColor()