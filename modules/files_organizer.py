import os
import shutil
from utils.security import is_safe_path

def move_files(source: str, destination: str, extension: str = None, keyword: str = None) -> int:
    
    if not is_safe_path(source) or not is_safe_path(destination):
        raise PermissionError("Ruta protegida por seguridad.")

    if not os.path.exists(source):
        raise FileNotFoundError("La carpeta de origen no existe.")

    files_to_move = []
    
    # Filtrado
    for filename in os.listdir(source):
        if extension and not filename.lower().endswith(extension.lower()):
            continue
        if keyword and keyword.lower() not in filename.lower():
            continue
            
        files_to_move.append(filename)

    if not files_to_move:
        return 0

    # Crear destino si no existe
    if not os.path.exists(destination):
        os.makedirs(destination)

    moved_count = 0
    for filename in files_to_move:
        try:
            shutil.move(os.path.join(source, filename), os.path.join(destination, filename))
            moved_count += 1
        except Exception as e:
            print(f"Error moviendo {filename}: {e}")
            continue

    return moved_count