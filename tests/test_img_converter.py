import pytest
import os
from modules.img_converter import convert_image
from PIL import Image

def test_error_si_imagen_no_existe():
    with pytest.raises(FileNotFoundError):
        convert_image("ruta/falsa.jpg", "salida.pdf", "PDF")

def test_crea_imagen_correctamente(tmp_path):
    # 1. Crear una imagen falsa pequeñita para probar
    origen = tmp_path / "test.png"
    img = Image.new('RGB', (60, 30), color = 'red')
    img.save(origen)
    
    destino = str(tmp_path / "test.pdf")
    
    # 2. Convertir
    convert_image(str(origen), destino, "PDF")
    
    # 3. Verificar que se creó el archivo
    assert os.path.exists(destino)