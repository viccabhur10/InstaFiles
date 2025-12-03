import os
from PIL import Image

def convert_image(input_path: str, output_path: str, format_name: str):
    """Abre una imagen y la guarda en otro formato."""
    if not os.path.exists(input_path):
        raise FileNotFoundError("La imagen original no existe.")

    img = Image.open(input_path)

    # Conversión necesaria para guardar como JPEG o PDF si hay transparencia
    if img.mode in ("RGBA", "P") and format_name in ["JPEG", "PDF"]:
        img = img.convert('RGB')

    if format_name == "ICO":
        img.save(output_path, format='ICO', sizes=[(256, 256)])
    else:
        img.save(output_path)