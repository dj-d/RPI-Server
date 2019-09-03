import os

# TODO: prima di avviare il comando la prima lanciare "sudo apt-get install etherwake" per installare l'applicativo
# FATTO


def turn_on():
    os.system("wakeonlan C8:54:4B:7A:92:C8")
