import sys
import os


# Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)