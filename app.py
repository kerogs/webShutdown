from flask import Flask, render_template, request, redirect, url_for
import os
from configparser import ConfigParser
from colorama import Fore, init
import logging

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'{PATH_PROJECT}\server.log', encoding='utf-8', level=logging.DEBUG)

config = ConfigParser()
config.read(f'{PATH_PROJECT}/config.ini')

init(autoreset=True)

CONF_LOCAL_SHARE = config['Server'].getboolean('local_share')
if CONF_LOCAL_SHARE:
    HOST = "0.0.0.0"
    HOST_SHARE = "Enabled"
else:
    HOST = "127.0.0.1"
    HOST_SHARE = "Disabled"

CONF_DEBUG = config['Server'].getboolean('debug')
CONF_PORT = config['Server'].getint('port')
CONF_PASSWORD = config['Login']['password']

CONF_OS = config['Shutdown']['os']
CONF_CUSTOM_SHUTDOWN = config['Shutdown']['custom_shutdown']
if CONF_CUSTOM_SHUTDOWN == "False":
    CONF_CUSTOM_SHUTDOWN = False

if CONF_CUSTOM_SHUTDOWN is False:
    if CONF_OS not in ["Windows", "Linux", "Mac"]:
        print(f"{Fore.RED}Error OS not recognized. in {Fore.YELLOW}config.ini{Fore.RED} you put {Fore.YELLOW}os={Fore.BLUE}{CONF_OS}{Fore.RED} but you can only use {Fore.BLUE}Windows|Linux|Mac{Fore.RED}.")
        exit()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    password = request.form['password']
    if password == CONF_PASSWORD:
        if CONF_CUSTOM_SHUTDOWN:
            logger.info("Shutting down...")
            os.system(CONF_CUSTOM_SHUTDOWN)
            return "Shutting down..."
        else:
            if(CONF_OS == "Windows"):
                logger.info("Shutting down...")
                os.system("shutdown /s /t 1")
                return "Shutting down..."
            elif(CONF_OS == "Linux") or (CONF_OS == "Mac"):
                logger.info("Shutting down...")
                os.system("shutdown now")
                return "Shutting down..."
            else:
                logger.error("Error OS not recognized")
                return "Error OS not recognized", 500
    else:
        logger.error("Incorrect password")
        return "Incorrect password", 401
    
if __name__ == '__main__':
    print(f"{Fore.YELLOW}=====================")
    print(f"{Fore.YELLOW}WEBSHUTODWN")
    print(f"{Fore.YELLOW}Created by : Kerogs")
    print(f"{Fore.YELLOW}Version : 1.0.0")
    print(f"{Fore.YELLOW}Github : https://github.com/kerogs/webShutdown")
    print(f"{Fore.YELLOW}=====================")
    print("")
    print(f"{Fore.GREEN}[DEBUG : {CONF_DEBUG}] {Fore.WHITE}| {Fore.RED}[PORT : {CONF_PORT}] {Fore.WHITE}| {Fore.BLUE}[HOST_SHARE : {HOST_SHARE}]")
    print(f"{Fore.CYAN}[OS : {CONF_OS}] {Fore.WHITE}| {Fore.CYAN}[CUSTOM_SHUTDOWN : {CONF_CUSTOM_SHUTDOWN}]")
    print(f"For configuration check the init file at {Fore.BLUE}{PATH_PROJECT}\config.ini")
    logger.info("Server started")
    app.run(debug=CONF_DEBUG, host=HOST, port=CONF_PORT)