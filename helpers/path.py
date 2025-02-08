import os, sys

def get_base_path():
    if getattr(sys, 'frozen', False):  # Si c'est un EXE généré par PyInstaller
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))