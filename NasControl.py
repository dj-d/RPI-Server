import os

# TODO: prima di avviare il comando la prima lanciare "sudo apt-get install etherwake" per installare l'applicativo
# FATTO


def turn_on():
    os.system("wakeonlan your_nas_mac_address")
