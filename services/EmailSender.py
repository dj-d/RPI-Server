import smtplib

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'YOUR_EMAIL'
PASSWORD = 'YOUR_EMAIL_PASSWORD'
GMAIL_HOST = 'YOUR_EMAIL_HOST'
GMAIL_PORT = 465
domain = 'localhost'
port = '5000'


def send_mail(email, message, subject):
    # set up the SMTP server
    s = smtplib.SMTP_SSL(host=GMAIL_HOST, port=GMAIL_PORT)
    s.ehlo()
    s.login(MY_ADDRESS, PASSWORD)

    # create a message
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

    return True


def send_otp(email, otp):
    message = "Il tuo codice di verifica per rpi-app è: " + "\n" + str(otp)
    subject = "rpi-app OTP Code"

    return send_mail(email, message, subject)


def send_reset_password(email):
    link_change_password = domain + ":" + port + "/change-password"
    message = "Clicca sul link sottostante per resettare la password." + "\n" + link_change_password + "\n" + "Se non sei stato tu a chiedere di resettare la password ti consigliamo di contattarci."
    subject = "Password reset"

    return send_mail(email, message, subject)
