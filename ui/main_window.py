import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import webbrowser
from PIL import Image
from utils.paths import resource_path

from modules import files_organizer, ai_writer, img_converter, pdf_tools

class InstaFilesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE VENTANA ---
        self.title("InstaFiles - Automatizador PC")
        self.geometry("950x750")
        
        try:
            self.iconbitmap(resource_path(os.path.join("assets", "icono.ico")))
        except:
            pass

        # --- CARGA DE IMÁGENES ---
        self.img_mover_big = self.load_asset_image("mover.png", fixed_height=50)
        self.img_ia_big = self.load_asset_image("ia.png", fixed_height=50)
        self.img_foto_big = self.load_asset_image("img.png", fixed_height=50)
        
        # --- PESTAÑAS ---
        self.tabview = ctk.CTkTabview(self, width=900, height=700)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_mover = self.tabview.add("Organizador")
        self.tab_ia = self.tabview.add("Redactor IA (Ollama)")
        self.tab_img = self.tabview.add("Conversor")
        self.tab_pdf = self.tabview.add("Herramientas PDF") 
        

        # Inicializar pestañas
        self.setup_organizer_tab()
        self.setup_ai_tab()
        self.setup_converter_tab()
        self.setup_pdf_tab()

    def load_asset_image(self, filename, fixed_height=30):
        """Carga una imagen de la carpeta assets redimensionándola."""
        path = resource_path(os.path.join("assets", filename))
        if os.path.exists(path):
            original_img = Image.open(path)
            ratio = original_img.width / original_img.height
            new_width = int(fixed_height * ratio)
            return ctk.CTkImage(light_image=original_img, dark_image=original_img, size=(new_width, fixed_height))
        return None

    def select_folder(self, entry_widget):
        """Abre diálogo para seleccionar carpeta y la pone en el entry."""
        path = filedialog.askdirectory()
        if path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, path)
            entry_widget.xview_moveto(1)

    # =======================================================
    # TAB 1: ORGANIZADOR (Organizer)
    # =======================================================
    def setup_organizer_tab(self):
        frame = self.tab_mover
        
        ctk.CTkLabel(frame, text=" Organización de Archivos", image=self.img_mover_big, compound="left", font=("Segoe UI", 26, "bold")).pack(pady=(20, 30))

        main_content = ctk.CTkFrame(frame, fg_color="transparent")
        main_content.pack(anchor="center")

        input_frame = ctk.CTkFrame(main_content)
        input_frame.pack(pady=10, padx=20, fill="x")
        input_frame.grid_columnconfigure(1, weight=1) 

        # Origen
        ctk.CTkLabel(input_frame, text="Origen:", font=("Arial", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="e")
        self.entry_org_source = ctk.CTkEntry(input_frame, width=400, height=35)
        self.entry_org_source.grid(row=0, column=1, padx=10, sticky="we")
        ctk.CTkButton(input_frame, text="📂", width=50, height=35, font=("Segoe UI Emoji", 20), command=lambda: self.select_folder(self.entry_org_source)).grid(row=0, column=2, padx=15)

        # Destino
        ctk.CTkLabel(input_frame, text="Destino:", font=("Arial", 14)).grid(row=1, column=0, padx=15, pady=15, sticky="e")
        self.entry_org_dest = ctk.CTkEntry(input_frame, width=400, height=35)
        self.entry_org_dest.grid(row=1, column=1, padx=10, sticky="we")
        ctk.CTkButton(input_frame, text="📂", width=50, height=35, font=("Segoe UI Emoji", 20), command=lambda: self.select_folder(self.entry_org_dest)).grid(row=1, column=2, padx=15)

        # Filtros
        filter_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        filter_frame.pack(pady=20, anchor="center")

        ctk.CTkLabel(filter_frame, text="Tipo de archivo (ej: .pdf):").grid(row=0, column=0, padx=10, sticky="e")
        self.entry_org_ext = ctk.CTkEntry(filter_frame, width=120)
        self.entry_org_ext.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(filter_frame, text="Buscar por palabras (Opcional):").grid(row=0, column=2, padx=10, sticky="e")
        self.entry_org_keyword = ctk.CTkEntry(filter_frame, width=250)
        self.entry_org_keyword.grid(row=0, column=3, padx=10)

        ctk.CTkButton(frame, text="MOVER ARCHIVOS", fg_color="#e63946", hover_color="#d62828", height=50, font=("Arial", 16, "bold"), command=self.run_organizer).pack(pady=30)

    def run_organizer(self):
        source = self.entry_org_source.get()
        dest = self.entry_org_dest.get()
        ext = self.entry_org_ext.get()
        keyword = self.entry_org_keyword.get()

        try:
            # Llamamos al módulo lógico
            count = files_organizer.move_files(source, dest, ext, keyword)
            
            if count > 0:
                messagebox.showinfo("Hecho", f"Se movieron {count} archivos correctamente.")
            else:
                messagebox.showinfo("Info", "No se encontraron archivos para mover con esos criterios.")
                
        except PermissionError:
            messagebox.showerror("Seguridad", "¡Acceso denegado! Estás intentando mover archivos de una carpeta protegida del sistema.")
        except FileNotFoundError:
            messagebox.showerror("Error", "La carpeta de origen no existe.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    # =======================================================
    # TAB 2: REDACTOR IA (AI Writer)
    # =======================================================
    def setup_ai_tab(self):
        frame = self.tab_ia
        
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(pady=(20, 10), fill="x", padx=20)
        ctk.CTkLabel(header_frame, text=" Redactor IA Local", image=self.img_ia_big, compound="left", font=("Segoe UI", 26, "bold")).pack(side="left")
        
        self.lbl_ollama_status = ctk.CTkLabel(header_frame, text="Comprobando...", font=("Arial", 14, "bold"))
        self.lbl_ollama_status.pack(side="right", padx=10)
        
        # Config manual
        self.config_frame = ctk.CTkFrame(frame, border_width=1, border_color="#E07A5F")
        self.config_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(self.config_frame, text="Configuración Manual (NO TOCAR si arriba dice CONECTADO):", font=("Arial", 11, "bold"), text_color="#E07A5F").pack(anchor="w", padx=15, pady=(10, 5))
        
        path_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.entry_ollama_exe = ctk.CTkEntry(path_frame, placeholder_text="Ruta al .exe de Ollama")
        self.entry_ollama_exe.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(path_frame, text="Buscar .exe", width=90, command=self.find_ollama_exe).pack(side="left", padx=5)
        ctk.CTkButton(path_frame, text="Forzar Inicio", width=100, fg_color="#E07A5F", hover_color="#D06A4F", command=self.force_start_ollama).pack(side="left", padx=5)
        
        btn_help = ctk.CTkButton(frame, text="¿No tienes Ollama instalado? Descárgalo aquí", fg_color="transparent", text_color="#4cc9f0", hover=False, command=lambda: webbrowser.open("https://ollama.com/download"))
        btn_help.pack(pady=(0, 20))

        # Inputs Documento
        work_frame = ctk.CTkFrame(frame)
        work_frame.pack(padx=40, fill="x", pady=10)
        work_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(work_frame, text="Nombre archivo:", font=("Arial", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="e")
        self.entry_doc_name = ctk.CTkEntry(work_frame, height=35, placeholder_text="Ej: Trabajo_Historia")
        self.entry_doc_name.grid(row=0, column=1, padx=10, sticky="we", columnspan=2)

        ctk.CTkLabel(work_frame, text="Guardar en:", font=("Arial", 14)).grid(row=1, column=0, padx=15, pady=15, sticky="e")
        self.entry_doc_path = ctk.CTkEntry(work_frame, height=35, placeholder_text="Selecciona una carpeta...")
        self.entry_doc_path.grid(row=1, column=1, padx=10, sticky="we")
        ctk.CTkButton(work_frame, text="📂", width=50, height=35, font=("Segoe UI Emoji", 20), command=lambda: self.select_folder(self.entry_doc_path)).grid(row=1, column=2, padx=15)

        ctk.CTkLabel(frame, text="Prompt (Instrucciones para la IA):", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(15, 5))
        self.text_prompt = ctk.CTkTextbox(frame, height=120)
        self.text_prompt.pack(fill="x", padx=40, pady=5)

        self.btn_generate = ctk.CTkButton(frame, text="GENERAR DOCUMENTO", fg_color="#2a9d8f", hover_color="#21867a", height=50, font=("Arial", 16, "bold"), command=self.run_ai_generation)
        self.btn_generate.pack(pady=20)

        self.check_ollama_loop()

    def find_ollama_exe(self):
        file = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        if file:
            self.entry_ollama_exe.delete(0, "end")
            self.entry_ollama_exe.insert(0, file)

    def check_ollama_loop(self):
        """Verifica el estado de Ollama periódicamente."""
        is_connected = ai_writer.check_ollama_connection()
        if is_connected:
            self.lbl_ollama_status.configure(text="🟢 CONECTADO", text_color="#2dc653")
            self.ollama_ready = True
        else:
            self.lbl_ollama_status.configure(text="🔴 DESCONECTADO", text_color="#d00000")
            self.ollama_ready = False
        
        self.after(5000, self.check_ollama_loop)

    def force_start_ollama(self):
        exe_path = self.entry_ollama_exe.get()
        if os.path.exists(exe_path) and exe_path.endswith("ollama.exe"):
            try:
                subprocess.Popen([exe_path, "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
                messagebox.showinfo("Iniciando", "Espera 10 segundos y el estado debería cambiar a VERDE.")
                self.after(8000, self.check_ollama_loop) 
            except Exception as e:
                messagebox.showerror("Error", f"Error al lanzar el exe: {e}")
        else:
            messagebox.showwarning("Ruta inválida", "Selecciona el archivo 'ollama.exe' válido.")

    def run_ai_generation(self):
        # 1. Validaciones UI
        if not hasattr(self, 'ollama_ready') or not self.ollama_ready:
            messagebox.showerror("Error", "Ollama no está conectado. Revisa el indicador arriba a la derecha.")
            return

        prompt = self.text_prompt.get("1.0", "end-1c")
        name = self.entry_doc_name.get()
        path = self.entry_doc_path.get()

        if not name or len(prompt) < 5 or not path:
            messagebox.showwarning("Faltan datos", "Por favor rellena nombre, ruta y el prompt deseado.")
            return

        # 2. Bloqueo UI
        self.btn_generate.configure(state="disabled", text="Pensando... (Esto puede tardar)")
        self.update()

        # 3. Llamada al Módulo
        try:
            full_path = ai_writer.generate_doc(prompt, name, path)
            messagebox.showinfo("Éxito", f"Documento creado en:\n{full_path}")
        except Exception as e:
            messagebox.showerror("Error IA", f"Ocurrió un error: {str(e)}")
        finally:
            self.btn_generate.configure(state="normal", text="GENERAR DOCUMENTO")

    # =======================================================
    # TAB 3: CONVERSOR IMÁGENES (Image converter)
    # =======================================================
    def setup_converter_tab(self):
        frame = self.tab_img
        
        ctk.CTkLabel(frame, text=" Conversor de Formatos", image=self.img_foto_big, compound="left", font=("Segoe UI", 26, "bold")).pack(pady=(20, 40))

        main_content = ctk.CTkFrame(frame, fg_color="transparent")
        main_content.pack(anchor="center", fill="x", padx=50)
        main_content.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(main_content, text="Seleccionar imagen:", font=("Arial", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="e")
        self.entry_img_path = ctk.CTkEntry(main_content, height=35, placeholder_text="Ninguna imagen seleccionada", state="readonly")
        self.entry_img_path.grid(row=0, column=1, padx=10, sticky="we")
        
        ctk.CTkButton(main_content, text="📂", width=50, height=35, font=("Segoe UI Emoji", 20), command=self.select_image_file).grid(row=0, column=2, padx=15)

        format_frame = ctk.CTkFrame(frame, fg_color="transparent")
        format_frame.pack(pady=20)
        ctk.CTkLabel(format_frame, text="Convertir a formato:", font=("Arial", 14)).pack(side="left", padx=15)
        self.combo_format = ctk.CTkComboBox(format_frame, values=["PDF", "PNG", "JPEG", "WEBP", "ICO"], width=150, height=35, font=("Arial", 14))
        self.combo_format.set("PDF")
        self.combo_format.pack(side="left")
        
        ctk.CTkButton(frame, text="CONVERTIR IMAGEN", fg_color="#0077b6", hover_color="#0096c7", height=50, font=("Arial", 16, "bold"), command=self.run_converter).pack(pady=30)
        
        self.selected_img_path = None

    def select_image_file(self):
        file = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.webp *.bmp")])
        if file:
            self.selected_img_path = file
            self.entry_img_path.configure(state="normal")
            self.entry_img_path.delete(0, "end")
            self.entry_img_path.insert(0, file)
            self.entry_img_path.xview_moveto(1)
            self.entry_img_path.configure(state="readonly")

    def run_converter(self):
        if not self.selected_img_path or not os.path.exists(self.selected_img_path):
            messagebox.showwarning("Atención", "Selecciona una imagen primero.")
            return
        
        target_format = self.combo_format.get()
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{target_format.lower()}",
            filetypes=[(target_format, f"*.{target_format.lower()}")],
            title="Guardar como..."
        )

        if save_path:
            try:
                img_converter.convert_image(self.selected_img_path, save_path, target_format)
                messagebox.showinfo("Éxito", f"Imagen convertida a {target_format} correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al convertir: {str(e)}")


# =======================================================
    # TAB 4: HERRAMIENTAS PDF
    # =======================================================
    def setup_pdf_tab(self):
        frame = self.tab_pdf
        
        # Sub-pestañas internas para organizar las 3 funciones PDF
        self.pdf_tabs = ctk.CTkTabview(frame, height=400)
        self.pdf_tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_merge = self.pdf_tabs.add("Unir PDFs")
        tab_extract = self.pdf_tabs.add("Extraer Páginas")
        tab_protect = self.pdf_tabs.add("Proteger")
        
        # --- 1. UNIR (MERGE) ---
        ctk.CTkLabel(tab_merge, text="Selecciona varios archivos para unirlos en uno solo:", font=("Arial", 14)).pack(pady=10)
        
        self.list_merge_files = ctk.CTkTextbox(tab_merge, height=100)
        self.list_merge_files.pack(pady=5, padx=20, fill="x")
        self.list_merge_files.insert("0.0", "Ningún archivo seleccionado...\n")
        self.list_merge_files.configure(state="disabled")
        
        self.files_to_merge = [] # Lista de rutas
        
        btn_frame = ctk.CTkFrame(tab_merge, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Seleccionar PDFs (+)", command=self.select_pdfs_to_merge).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar Lista", fg_color="#E07A5F", command=self.clear_merge_list).pack(side="left", padx=5)
        
        ctk.CTkButton(tab_merge, text="UNIR Y GUARDAR", fg_color="#2a9d8f", height=40, font=("Arial", 14, "bold"), command=self.run_pdf_merge).pack(pady=20)

        # --- 2. EXTRAER (SPLIT) ---
        ctk.CTkLabel(tab_extract, text="Archivo PDF origen:").pack(pady=(15,5))
        
        extract_input_frame = ctk.CTkFrame(tab_extract, fg_color="transparent")
        extract_input_frame.pack(fill="x", padx=20)
        self.entry_pdf_extract_src = ctk.CTkEntry(extract_input_frame, placeholder_text="Selecciona PDF...")
        self.entry_pdf_extract_src.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(extract_input_frame, text="📂", width=40, command=lambda: self.select_file_for_entry(self.entry_pdf_extract_src)).pack(side="left", padx=5)
        
        range_frame = ctk.CTkFrame(tab_extract)
        range_frame.pack(pady=20)
        ctk.CTkLabel(range_frame, text="Desde pág:").pack(side="left", padx=5)
        self.entry_page_start = ctk.CTkEntry(range_frame, width=50)
        self.entry_page_start.pack(side="left", padx=5)
        ctk.CTkLabel(range_frame, text="Hasta pág:").pack(side="left", padx=5)
        self.entry_page_end = ctk.CTkEntry(range_frame, width=50)
        self.entry_page_end.pack(side="left", padx=5)
        ctk.CTkLabel(range_frame, text="Excepto:").pack(side="left", padx=5)
        self.except_pages = ctk.CTkEntry(range_frame, width=50)
        self.except_pages.pack(side="left", padx=5)
        
        ctk.CTkButton(tab_extract, text="EXTRAER PÁGINAS", fg_color="#e9c46a", text_color="black", height=40, font=("Arial", 14, "bold"), command=self.run_pdf_extract).pack(pady=20)

        # --- 3. PROTEGER (ENCRYPT) ---
        ctk.CTkLabel(tab_protect, text="Archivo PDF a proteger:").pack(pady=(15,5))
        protect_input_frame = ctk.CTkFrame(tab_protect, fg_color="transparent")
        protect_input_frame.pack(fill="x", padx=20)
        self.entry_pdf_protect_src = ctk.CTkEntry(protect_input_frame, placeholder_text="Selecciona PDF...")
        self.entry_pdf_protect_src.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(protect_input_frame, text="📂", width=40, command=lambda: self.select_file_for_entry(self.entry_pdf_protect_src)).pack(side="left", padx=5)
        
        ctk.CTkLabel(tab_protect, text="Contraseña:").pack(pady=(10,5))
        self.entry_pdf_pwd = ctk.CTkEntry(tab_protect, show="*")
        self.entry_pdf_pwd.pack(pady=5)
        
        ctk.CTkButton(tab_protect, text="ENCRIPTAR PDF", fg_color="#e76f51", height=40, font=("Arial", 14, "bold"), command=self.run_pdf_protect).pack(pady=20)

    # --- LÓGICA INTERNA PDF ---
    def select_file_for_entry(self, entry_widget):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, path)

    def select_pdfs_to_merge(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.files_to_merge.extend(files)
            self.update_merge_listbox()

    def clear_merge_list(self):
        self.files_to_merge = []
        self.update_merge_listbox()

    def update_merge_listbox(self):
        self.list_merge_files.configure(state="normal")
        self.list_merge_files.delete("1.0", "end")
        for f in self.files_to_merge:
            self.list_merge_files.insert("end", f"{os.path.basename(f)}\n")
        self.list_merge_files.configure(state="disabled")

    def run_pdf_merge(self):
        if len(self.files_to_merge) < 2:
            messagebox.showwarning("Faltan archivos", "Selecciona al menos 2 PDFs para unir.")
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if save_path:
            try:
                pdf_tools.merge_pdfs(self.files_to_merge, save_path)
                messagebox.showinfo("Éxito", "PDFs unidos correctamente.")
                self.clear_merge_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def run_pdf_extract(self):
        src = self.entry_pdf_extract_src.get()
        start = self.entry_page_start.get()
        end = self.entry_page_end.get()
        
        if not src or not start.isdigit() or not end.isdigit():
            messagebox.showwarning("Datos inválidos", "Revisa el archivo y los números de página.")
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if save_path:
            try:
                pdf_tools.extract_pages(src, save_path, int(start), int(end))
                messagebox.showinfo("Éxito", "Páginas extraídas correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def run_pdf_protect(self):
        src = self.entry_pdf_protect_src.get()
        pwd = self.entry_pdf_pwd.get()
        
        if not src or not pwd:
            messagebox.showwarning("Faltan datos", "Selecciona archivo y escribe una contraseña.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if save_path:
            try:
                pdf_tools.protect_pdf(src, save_path, pwd)
                messagebox.showinfo("Éxito", "PDF protegido correctamente.")
                self.entry_pdf_pwd.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", str(e))