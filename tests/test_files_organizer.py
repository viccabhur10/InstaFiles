import os
import pytest
from modules.files_organizer import move_files

def test_move_files_basic(tmp_path):
    """Prueba básica: mueve todo lo que hay en una carpeta."""
    # 1. PREPARACIÓN (Setup)
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()
    
    (source / "archivo1.txt").write_text("contenido prueba")
    (source / "archivo2.jpg").write_text("imagen prueba")

    # 2. ACCIÓN
    moved_count = move_files(str(source), str(dest))

    # 3. VERIFICACIÓN (Assert)
    assert moved_count == 2
    assert not os.path.exists(str(source / "archivo1.txt"))
    assert not os.path.exists(str(source / "archivo2.jpg"))
    assert os.path.exists(str(dest / "archivo1.txt"))
    assert os.path.exists(str(dest / "archivo2.jpg"))

def test_move_files_filter_extension(tmp_path):
    """Prueba de filtro: solo mueve los PDFs."""
    # 1. Setup
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()
    
    (source / "documento.pdf").write_text("soy un pdf")
    (source / "notas.txt").write_text("soy texto")

    # 2. Act (Pedimos mover solo .pdf)
    count = move_files(str(source), str(dest), extension=".pdf")

    # 3. Assert
    assert count == 1
    assert os.path.exists(str(dest / "documento.pdf"))
    assert os.path.exists(str(source / "notas.txt"))

def test_move_files_filter_keyword(tmp_path):
    """Prueba de filtro: solo mueve archivos con la palabra 'factura'."""
    # 1. Setup
    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()
    
    (source / "factura_enero.txt").write_text("...")
    (source / "lista_compra.txt").write_text("...")

    # 2. Act
    count = move_files(str(source), str(dest), keyword="factura")

    # 3. Assert
    assert count == 1
    assert os.path.exists(str(dest / "factura_enero.txt"))
    assert os.path.exists(str(source / "lista_compra.txt"))