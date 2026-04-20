import os

def limpiar_terminal():
    #para Windows
    if os.name == 'nt':
        os.system('cls')
    #para Linux y macOS (posix)
    else:
        os.system('clear')