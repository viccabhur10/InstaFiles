# InstaFiles - Automatizador de Escritorio

InstaFiles es un proyecto desarrollado con Python y CustomTkinter diseñado para realizar tareas en nuestro PC.
Las funciones que contiene actualmente son:
- Mover archivos de unas carpetas a otras en masa, pudiendo organizarlas por nombre del fichero. 
- Generar un .word rellenado automaticamente por Inteligencia artificial (Ollama) insertando en el mismo lugar nombre de fichero, ruta y prompt.
- Covertidor de .jpg a diferentes extensiones de archivos.

Proyecto desarrollado por Víctor José Cabrera Hurtado.

## Requisitos

- **Python 3.10** o superior.
- **Ollama**: Motor de IA local (necesario para el módulo de redacción).
- Dependencias de Python listadas en `requirements.txt`.
- Sistema Operativo: Windows (recomendado), compatible con Linux/macOS.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/viccabhur10/InstaFiles
cd InstaFiles
```

### 2. Entorno virtual

## 2.1 Crear entorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual
En Linux/macOS:

```bash
source venv/bin/activate
```

## 2.2 Instalar dependencias del entorno virtual

```bash
pip install -r requirements.txt
```

### 3. Configurar IA (Ollama)
Este proyecto requiere la configuración del modelo de lenguaje.

## 3.1 Instalación y descarga del modelo
Descargar e instalar Ollama de la página oficial. A continuación, abrir una terminal y ejecutar el siguiente comando para descargar el modelo:

```bash
ollama pull llama3.2
```

## 3.2 Verificación
Asegurarse de que el servicio de Ollama está corriendo en segundo plano (accesible en localhost:11434).

### 4. Iniciar la aplicación

```bash
python main.py
```

La interfaz gráfica se abrirá inmediatamente.

### 5. Generar ejecutable portatil de InstaFiles

```bash
pyinstaller --noconfirm --onefile --windowed --icon "assets/icono.ico" --name "InstaFiles" --add-data "assets;assets" --collect-all customtkinter main.py
```

### 6. Estructura de carpetas
- InstaFiles/: Directorio raíz del proyecto.

    - modules/: Contiene los diferentes módulos del proyecto.

    - ui/: Contiene la interfaz gráfica.

    - utils/: Utilidades transversales y seguridad.

    - tests/: Tests unitarios y de integración.

    - assets/: Recursos estáticos (imágenes e iconos).

    - README.md: Documentación del proyecto.

    - .gitignore: Archivo de configuración de Git.

    - requirements.txt: Archivo con las dependencias de Python.

    - main.py: Punto de entrada de la aplicación.

## 6.1. Estructura de módulos

- files_organizer.py: Archivo para la organización y movimiento de archivos con filtros.

- ai_writer.py: Cliente para la comunicación con la API de Ollama y generación de .docx.

- img_converter.py: Motor de Conversion de imágenes basado en Pillow.

## 6.2. Estructura de interfaz
La interfaz está construida con CustomTkinter:

- main_window.py: Contiene la clase InstaFilesApp. Gestiona la creación de pestañas, widgets y la orquestación de eventos de usuario.

### 7. Ejecución de tests

## 7.1. Tests de Pytest
Para ejecutar la batería completa de tests, ejecutar el siguiente comando en el directorio raíz:

```bash
pytest
```