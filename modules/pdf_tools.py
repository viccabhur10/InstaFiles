import os
from pypdf import PdfReader, PdfWriter

def merge_pdfs(input_paths: list, output_path: str):
    merger = PdfWriter()

    for path in input_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        merger.append(path)

    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"
        
    merger.write(output_path)
    merger.close()
    return output_path

def extract_pages(input_path: str, output_path: str, start_page: int, end_page: int, except_pages: list = None):
    if not os.path.exists(input_path):
        raise FileNotFoundError("El archivo original no existe.")
        
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    
    if start_page < 1 or end_page > total_pages or start_page > end_page:
        raise ValueError(f"Rango inválido. El documento tiene {total_pages} páginas.")

    exceptions_set = set()
    if except_pages:
        for p in except_pages:
            try:
                page_num = int(str(p).strip())
                exceptions_set.add(page_num)
            except (ValueError, TypeError):
                continue

    for i in range(start_page - 1, end_page):
        # 'i' es el índice interno de Python (empieza en 0).
        human_page_num = i + 1
        
        if human_page_num not in exceptions_set:
            writer.add_page(reader.pages[i])

    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"

    with open(output_path, "wb") as f:
        writer.write(f)
        
    return output_path

def protect_pdf(input_path: str, output_path: str, password: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError("El archivo original no existe.")
    
    if not password:
        raise ValueError("La contraseña no puede estar vacía.")

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copiar todas las páginas
    for page in reader.pages:
        writer.add_page(page)

    # Encriptar
    writer.encrypt(password)

    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path