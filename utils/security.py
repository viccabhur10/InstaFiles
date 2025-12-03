import os

# Rutas prohibidas
FORBIDDEN_PATHS = [
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "/bin", "/usr", "/etc"
]

def is_safe_path(path: str) -> bool:
    if not path:
        return False
    abs_path = os.path.abspath(path)
    for forbidden in FORBIDDEN_PATHS:
        # Comparamos ignorando mayúsculas/minúsculas
        if abs_path.lower().startswith(os.path.abspath(forbidden).lower()):
            return False
    return True