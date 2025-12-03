from modules.ai_writer import check_ollama_connection

def test_verifica_conexion():
    resultado = check_ollama_connection()
    assert isinstance(resultado, bool)