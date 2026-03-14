# ui/main_window.py
import tkinter as tk
import customtkinter as ctk
from utils.window_helpers import set_window_icon
from tkinter import ttk, filedialog
from data.loader import load_csv_files
from ui.tooltip import ToolTip
import threading
import automation.login as login
from data.analysis import generar_lista_desaprobados_y_aprobados
from automation.upload import Upload
import pandas as pd
from automation.upload import UploadIEFs


class MainWindow:
    def __init__(self, driver=None):
        self.root = ctk.CTk()
        # Establecer ícono
        set_window_icon(self.root)
        self.root.title("Selene 2.0")
        self.root.geometry("1000x800")
        
        # IMPORTANTE: Asignar el driver recibido
        self.driver = driver

         # IMPORTANTE: Asegurar que el driver esté en la ventana principal
        if self.driver is not None:
            try:
                # Cambiar a la ventana principal (la primera/original)
                self.driver.switch_to.window(self.driver.window_handles[0])
                # Asegurar que no estamos en un iframe
                self.driver.switch_to.default_content()
            except Exception as e:
                print(f"Advertencia al cambiar ventana: {e}")
        
        # Ya no necesitas crear un nuevo Login aquí si ya tienes el driver
        # Si driver es None, entonces sí lo creas
        if self.driver is None:
            self.login = login.Login()
        else:
            self.login = None  # O podrías guardar la instancia si la necesitas
        
        # Para NOTAS (panel izquierdo)
        self.csv_paths = []
        self.files_status_var = ctk.StringVar(value="No hay archivos cargados.")
        self.dataframes_notas = {}

        # Para IEFs (panel derecho)
        self.csv_paths_iefs = []
        self.files_status_var_iefs = ctk.StringVar(value="No hay archivos cargados.")
        self.dataframes_iefs = {}

        self.build_ui()
        
    


    # Configuración global de CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    
    def build_ui(self):
        # Colores Synthwave
        bg_dark = "#0a0e27"
        bg_panel = "#1a1d35"
        neon_pink = "#ff006e"
        neon_purple = "#8338ec"
        neon_cyan = "#05d9e8"
        neon_blue = "#3a86ff"
        text_color = "#eaeaeb"
        
        # ───────────────────────────
        # Contenedor principal
        # ───────────────────────────
        main_frame = ctk.CTkFrame(self.root, fg_color=bg_dark, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
        # Layout en tres columnas
        main_frame.columnconfigure(0, weight=0)  # panel izquierdo
        main_frame.columnconfigure(1, weight=1)  # área central
        main_frame.columnconfigure(2, weight=0)  # panel derecho
    
        # ───────────────────────────
        # Panel lateral 1 (NOTAS)
        # ───────────────────────────
        left_panel = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=bg_panel,
            corner_radius=15,
            border_width=2,
            border_color=neon_purple,
            width=280
        )
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 10))
    
        # ========= SESIÓN =========
        session_frame = ctk.CTkFrame(left_panel, fg_color=bg_dark, corner_radius=10)
        session_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            session_frame,
            text="⚡ Sesión",
            font=("Orbitron", 16, "bold"),
            text_color=neon_cyan
        ).pack(pady=10)
    
        # ========= ARCHIVOS =========
        files_frame = ctk.CTkFrame(left_panel, fg_color=bg_dark, corner_radius=10)
        files_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            files_frame,
            text="📁 Archivos de Notas",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        btn_attach = ctk.CTkButton(
            files_frame,
            text="Adjuntar CSV",
            command=self.attach_csv_files,
            font=("Rajdhani", 13),
            fg_color=neon_blue,
            hover_color=neon_purple,
            corner_radius=8,
            height=35
        )
        btn_attach.pack(fill="x", padx=10, pady=(0, 5))
    
        btn_reload = ctk.CTkButton(
            files_frame,
            text="Recargar archivos",
            command=self.reload_files,
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color="#3d4260",
            corner_radius=8,
            height=35
        )
        btn_reload.pack(fill="x", padx=10, pady=(0, 5))
    
        self.lbl_files_status = ctk.CTkLabel(
            files_frame,
            textvariable=self.files_status_var,
            font=("Rajdhani", 11),
            text_color="#888"
        )
        self.lbl_files_status.pack(pady=(5, 10))
    
        # ========= DATOS =========
        data_frame = ctk.CTkFrame(left_panel, fg_color=bg_dark, corner_radius=10)
        data_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            data_frame,
            text="📊 Datos",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        ctk.CTkLabel(
            data_frame,
            text="Cantidad de estudiantes:",
            font=("Rajdhani", 12),
            text_color=text_color
        ).pack(anchor="w", padx=10)
    
        self.students_var = ctk.StringVar(value="0")
        entry_students = ctk.CTkEntry(
            data_frame,
            width=80,
            height=35,
            textvariable=self.students_var,
            font=("Rajdhani", 14),
            fg_color="#0d1128",
            border_color=neon_purple,
            border_width=2,
            corner_radius=8
        )
        entry_students.pack(anchor="w", padx=10, pady=(0, 10))
    
        # ========= NOTAS =========
        grades_frame = ctk.CTkFrame(left_panel, fg_color=bg_dark, corner_radius=10)
        grades_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            grades_frame,
            text="📝 Notas",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        # Rango
        range_frame_grades = ctk.CTkFrame(grades_frame, fg_color="transparent")
        range_frame_grades.pack(fill="x", pady=5, padx=10)
    
        ctk.CTkLabel(
            range_frame_grades,
            text="Desde:",
            font=("Rajdhani", 12),
            text_color=text_color
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
    
        ctk.CTkLabel(
            range_frame_grades,
            text="Hasta:",
            font=("Rajdhani", 12),
            text_color=text_color
        ).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
    
        grade_options = []
        for i in range(1, 9):
            grade_options.extend([f"NE{i}", f"E{i}R1", f"E{i}R2"])
    
        self.combo_grades_from = ctk.CTkComboBox(
            range_frame_grades,
            values=grade_options,
            width=100,
            font=("Rajdhani", 12),
            fg_color="#0d1128",
            button_color=neon_purple,
            border_color=neon_purple,
            dropdown_fg_color=bg_panel,
            dropdown_hover_color=neon_purple
        )
        self.combo_grades_from.grid(row=1, column=0, pady=(0, 5))
    
        self.combo_grades_to = ctk.CTkComboBox(
            range_frame_grades,
            values=grade_options,
            width=100,
            font=("Rajdhani", 12),
            fg_color="#0d1128",
            button_color=neon_purple,
            border_color=neon_purple,
            dropdown_fg_color=bg_panel,
            dropdown_hover_color=neon_purple
        )
        self.combo_grades_to.grid(row=1, column=1, padx=(10, 0), pady=(0, 5))
    
        # Botones principales con efecto neón
        btn_upload_grades = ctk.CTkButton(
            grades_frame,
            text="▲ SUBIR NOTAS",
            command=self.iniciar_subida_notas,
            font=("Orbitron", 14, "bold"),
            fg_color=neon_pink,
            hover_color=neon_purple,
            corner_radius=10,
            height=45,
            border_width=2,
            border_color=neon_cyan
        )
        btn_upload_grades.pack(fill="x", padx=10, pady=(5, 5))
    
        btn_delete_grades = ctk.CTkButton(
            grades_frame,
            text="Borrar notas",
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color="#3d4260",
            corner_radius=8,
            height=35
        )
        btn_delete_grades.pack(fill="x", padx=10, pady=(0, 10))
    
        # ========= REPORTES =========
        eval_options = []
        for i in range(1, 9):
            eval_options.extend([f"EVAL {i}", f"R1E{i}", f"R2E{i}"])
    
        reportes_frame = ctk.CTkFrame(left_panel, fg_color=bg_dark, corner_radius=10)
        reportes_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            reportes_frame,
            text="📋 Reportes",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        self.combo_eval_desaprobados = ctk.CTkComboBox(
            reportes_frame,
            values=eval_options,
            width=200,
            font=("Rajdhani", 12),
            fg_color="#0d1128",
            button_color=neon_purple,
            border_color=neon_purple,
            dropdown_fg_color=bg_panel,
            dropdown_hover_color=neon_purple
        )
        self.combo_eval_desaprobados.pack(fill="x", padx=10, pady=(0, 5))
    
        btn_desaprobados = ctk.CTkButton(
            reportes_frame,
            text="Lista de (des)aprobados",
            command=self.crear_lista_desaprobados_y_aprobados,
            font=("Rajdhani", 13),
            fg_color=neon_blue,
            hover_color=neon_purple,
            corner_radius=8,
            height=35
        )
        btn_desaprobados.pack(fill="x", padx=10, pady=(0, 10))
    
        # ───────────────────────────
        # Área central (output)
        # ───────────────────────────
        content_frame = ctk.CTkFrame(
            main_frame,
            fg_color=bg_panel,
            corner_radius=15,
            border_width=2,
            border_color=neon_purple
        )
        content_frame.grid(row=0, column=1, sticky="nsew", padx=10)
    
        # Título del área central
        ctk.CTkLabel(
            content_frame,
            text="⚡ CONSOLA DE SALIDA",
            font=("Orbitron", 18, "bold"),
            text_color=neon_cyan
        ).pack(pady=(15, 10))
    
        # Text widget (mantenemos el original porque CustomTkinter no tiene CTkText completo)
        import tkinter as tk
        self.output_text = tk.Text(
            content_frame,
            wrap="word",
            height=25,
            background="#24243e",
            foreground="#eaeaeb",
            insertbackground="#d6d9e0",
            selectbackground="#3a3f5c",
            relief="flat",
            borderwidth=0,
            font=("Consolas", 11)
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    
        # Frame inferior para botones
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=(0, 15))
    
        save_btn = ctk.CTkButton(
            bottom_frame,
            text="💾 Guardar .txt",
            command=self.save_to_file,
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color=neon_blue,
            corner_radius=8,
            height=35,
            width=120
        )
        save_btn.pack(side="right", padx=(5, 0))
    
        copy_btn = ctk.CTkButton(
            bottom_frame,
            text="📋 Copiar",
            command=self.copy_to_clipboard,
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color=neon_blue,
            corner_radius=8,
            height=35,
            width=120
        )
        copy_btn.pack(side="right")
    
        # ───────────────────────────
        # Panel lateral 2 (IEFs)
        # ───────────────────────────
        right_panel = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=bg_panel,
            corner_radius=15,
            border_width=2,
            border_color=neon_purple,
            width=280
        )
        right_panel.grid(row=0, column=2, sticky="ns", padx=(10, 0))
    
        # ========= ARCHIVOS IEFs =========
        files_frame_ief = ctk.CTkFrame(right_panel, fg_color=bg_dark, corner_radius=10)
        files_frame_ief.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            files_frame_ief,
            text="📁 Archivos de IEFs",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        btn_attach_ief = ctk.CTkButton(
            files_frame_ief,
            text="Adjuntar CSV",
            command=self.attach_csv_files_iefs,
            font=("Rajdhani", 13),
            fg_color=neon_blue,
            hover_color=neon_purple,
            corner_radius=8,
            height=35
        )
        btn_attach_ief.pack(fill="x", padx=10, pady=(0, 5))
    
        btn_reload_ief = ctk.CTkButton(
            files_frame_ief,
            text="Recargar archivos",
            command=self.reload_files_iefs,
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color="#3d4260",
            corner_radius=8,
            height=35
        )
        btn_reload_ief.pack(fill="x", padx=10, pady=(0, 5))
    
        self.lbl_files_status_ief = ctk.CTkLabel(
            files_frame_ief,
            textvariable=self.files_status_var_iefs,
            font=("Rajdhani", 11),
            text_color="#888"
        )
        self.lbl_files_status_ief.pack(pady=(5, 10))
    
        # ========= DATOS IEFs =========
        data_frame_ief = ctk.CTkFrame(right_panel, fg_color=bg_dark, corner_radius=10)
        data_frame_ief.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            data_frame_ief,
            text="📊 Datos",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=10)
    
        # ========= IEFs =========
        iefs_frame = ctk.CTkFrame(right_panel, fg_color=bg_dark, corner_radius=10)
        iefs_frame.pack(fill="x", pady=(0, 10), padx=10)
    
        ctk.CTkLabel(
            iefs_frame,
            text="📚 IEFs",
            font=("Rajdhani", 14, "bold"),
            text_color=neon_cyan
        ).pack(pady=(10, 5))
    
        # Rango
        range_frame_iefs = ctk.CTkFrame(iefs_frame, fg_color="transparent")
        range_frame_iefs.pack(fill="x", pady=5, padx=10)
    
        ctk.CTkLabel(
            range_frame_iefs,
            text="Desde:",
            font=("Rajdhani", 12),
            text_color=text_color
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
    
        ctk.CTkLabel(
            range_frame_iefs,
            text="Hasta:",
            font=("Rajdhani", 12),
            text_color=text_color
        ).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
    
        ief_options = [f"Aprendizaje {chr(c)}" for c in range(ord("A"), ord("N") + 1)]
    
        self.combo_iefs_from = ctk.CTkComboBox(
            range_frame_iefs,
            values=ief_options,
            width=115,
            font=("Rajdhani", 11),
            fg_color="#0d1128",
            button_color=neon_purple,
            border_color=neon_purple,
            dropdown_fg_color=bg_panel,
            dropdown_hover_color=neon_purple
        )
        self.combo_iefs_from.grid(row=1, column=0, pady=(0, 5))
    
        self.combo_iefs_to = ctk.CTkComboBox(
            range_frame_iefs,
            values=ief_options,
            width=115,
            font=("Rajdhani", 11),
            fg_color="#0d1128",
            button_color=neon_purple,
            border_color=neon_purple,
            dropdown_fg_color=bg_panel,
            dropdown_hover_color=neon_purple
        )
        self.combo_iefs_to.grid(row=1, column=1, padx=(10, 0), pady=(0, 5))
    
        # Botones principales IEFs
        btn_upload_iefs = ctk.CTkButton(
            iefs_frame,
            text="▲ CARGAR IEFS",
            command=self.iniciar_subida_iefs,
            font=("Orbitron", 14, "bold"),
            fg_color=neon_pink,
            hover_color=neon_purple,
            corner_radius=10,
            height=45,
            border_width=2,
            border_color=neon_cyan
        )
        btn_upload_iefs.pack(fill="x", padx=10, pady=(5, 5))
    
        btn_finalizar_etapa = ctk.CTkButton(
            iefs_frame,
            text="⚡ FINALIZAR ETAPA",
            command=self.lanzador_finalizar_etapas,
            font=("Orbitron", 14, "bold"),
            fg_color=neon_pink,
            hover_color=neon_purple,
            corner_radius=10,
            height=45,
            border_width=2,
            border_color=neon_cyan
        )
        btn_finalizar_etapa.pack(fill="x", padx=10, pady=(0, 5))
    
        btn_close_iefs = ctk.CTkButton(
            iefs_frame,
            text="🔒 CERRAR IEFS",
            command=self.lanzador_cerrar_iefs,
            font=("Orbitron", 14, "bold"),
            fg_color=neon_pink,
            hover_color=neon_purple,
            corner_radius=10,
            height=45,
            border_width=2,
            border_color=neon_cyan
        )
        btn_close_iefs.pack(fill="x", padx=10, pady=(0, 5))
    
        btn_delete_iefs = ctk.CTkButton(
            iefs_frame,
            text="Borrar estado de aprendizajes",
            font=("Rajdhani", 13),
            fg_color="#2d3250",
            hover_color="#3d4260",
            corner_radius=8,
            height=35
        )
        btn_delete_iefs.pack(fill="x", padx=10, pady=(0, 10))
    
        



    
    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def save_to_file(self):
        text = self.output_text.get("1.0", "end-1c")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

    def attach_csv_files(self):
        
        """Para NOTAS (panel izquierdo)"""
        paths = filedialog.askopenfilenames(
            title="Seleccionar archivos CSV - NOTAS",
            initialdir="~/Downloads",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not paths:
            return

        self.csv_paths = list(paths)
        self.dataframes_notas.clear()

        for path in self.csv_paths:
            try:
                df = pd.read_csv(path)
                self.dataframes_notas[path] = df
            except Exception as e:
                print(f"Error al leer {path}: {e}")

        self.files_status_var.set(
            f"{len(self.dataframes_notas)} archivo(s) CSV cargado(s)."
        )

    def iniciar_subida_notas(self):
        threading.Thread(
        target=self.subir_notas,
        daemon=True
        ).start()

    def iniciar_subida_iefs(self):
        threading.Thread(
        target=self.subir_iefs,
        daemon=True
        ).start()


    def subir_notas(self):

        if self.driver is None:
            print("Debe iniciar sesión primero.")
            return
    
        if not self.dataframes_notas:
            print("No hay CSV cargado.")
            return
    
        # elegís el dataframe correcto (ejemplo: el primero)
        df = list(self.dataframes_notas.values())[0]
    
        col_inicio = self.combo_grades_from.get()
        col_fin = self.combo_grades_to.get()
    
        uploader = Upload(self.driver, df)
        uploader.subir_notas(col_inicio, col_fin)
        

    
    def subir_iefs(self):

        if self.driver is None:
            print("Debe iniciar sesión primero.")
            return
    
        if not self.dataframes_iefs:
            print("No hay CSV cargado.")
            return
    
        # elegís el dataframe correcto (ejemplo: el primero)
        df = list(self.dataframes_iefs.values())[0]
    
        col_inicio = self.combo_iefs_from.get()
        col_fin = self.combo_iefs_to.get()
    
        uploader = UploadIEFs(self.driver, df)
        uploader.subir_iefs(col_inicio, col_fin)
        


    def lanzador_finalizar_etapas(self):
        threading.Thread(
            target=self._finalizar_etapas_thread,
            daemon=True
        ).start()
    
    def lanzador_cerrar_iefs(self):
        threading.Thread(
            target=self._cerrar_iefs_thread,
            daemon=True
        ).start()
    
    

    def _finalizar_etapas_thread(self):

        if self.driver is None:
            print("Debe iniciar sesión primero.")
            return

        if not self.dataframes_iefs:
            print("No hay CSV de IEFs cargado.")
            return

        df = list(self.dataframes_iefs.values())[0]
        n= int(self.students_var.get())
        uploader = UploadIEFs(self.driver, df)
        uploader.finalizar_etapas(n)

    def _cerrar_iefs_thread(self):

        if self.driver is None:
            print("Debe iniciar sesión primero.")
            return

        if not self.dataframes_iefs:
            print("No hay CSV de IEFs cargado.")
            return

        df = list(self.dataframes_iefs.values())[0]

        uploader = UploadIEFs(self.driver, df)
        uploader.cerrar_iefs()


    def attach_csv_files_iefs(self):
        
        """Para IEFs (panel derecho)"""
        paths= filedialog.askopenfilenames(
            title="Seleccionar archivos CSV - IEFs",
            initialdir="~/Downloads",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not paths:
            return

        self.csv_paths_iefs = list(paths)
        self.dataframes_iefs.clear()

        for path in self.csv_paths_iefs:
            try:
                df = pd.read_csv(path)
                self.dataframes_iefs[path] = df
            except Exception as e:
                print(f"Error al leer {path}: {e}")

        self.files_status_var_iefs.set(
            f"{len(self.dataframes_iefs)} archivo(s) CSV cargado(s)."
        )


        
    

    def crear_lista_desaprobados_y_aprobados(self):
       
        # Validar archivos
        if not self.csv_paths:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "⚠️ Primero debe cargar archivos CSV de notas.\n")
            return

        # Validar columna
        columna = self.combo_eval_desaprobados.get()
        if not columna:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "⚠️ Seleccione una evaluación.\n")
            return

        # Validar número de estudiantes
        try:
            n_estudiantes = int(self.students_var.get())
            if n_estudiantes <= 0:
                raise ValueError
        except ValueError:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "⚠️ Ingrese un número válido de estudiantes.\n")
            return

        # Cargar dataframes de NOTAS (corregido)
        if not self.dataframes_notas:
            self.dataframes_notas = load_csv_files(self.csv_paths)

        self.output_text.delete("1.0", tk.END)

        for nombre_archivo, df in self.dataframes_notas.items():

            # VALIDACIÓN: Detectar si es archivo IEF por error
            columnas_ief = [col for col in df.columns if col.startswith('Aprendizaje')]
            if columnas_ief:
                self.output_text.insert(
                    tk.END, 
                    f"⚠️ ERROR: '{nombre_archivo}' parece ser un archivo de IEFs.\n"
                    f"   Este método es solo para archivos de NOTAS.\n"
                    f"   Por favor, cargue archivos CSV de notas en el panel izquierdo.\n\n"
                )
                continue

            # Columna inexistente
            if columna not in df.columns:
                self.output_text.insert(
                    tk.END, f"⚠️ '{columna}' no existe en {nombre_archivo}\n\n"
                )
                continue

            # Detección de columna vacía o con solo ceros
            serie_notas = pd.to_numeric(df[columna], errors="coerce")
            cantidad_notas_validas = (serie_notas > 0).sum()
            estado_columna_vacia = cantidad_notas_validas == 0

            # OUTPUT siempre (encabezado)
            self.output_text.insert(tk.END, f"📋 Archivo: {nombre_archivo}\n")
            self.output_text.insert(tk.END, f"📊 Evaluación: {columna}\n")

            if estado_columna_vacia:
                self.output_text.insert(tk.END, "❌ Desaprobados: 0\n")
                self.output_text.insert(tk.END, "✅ Aprobados: 0\n")
                self.output_text.insert(tk.END, "⚠️ Columna vacía: no se pueden calcular (des)aprobados.\n")
                self.output_text.insert(tk.END, "-" * 55 + "\n\n")
            else:
                try:
                    desaprobados, aprobados = generar_lista_desaprobados_y_aprobados(
                        df, columna, n_estudiantes
                    )

                    self.output_text.insert(tk.END, f"❌ Desaprobados: {len(desaprobados)}\n")
                    self.output_text.insert(tk.END, f"✅ Aprobados: {len(aprobados)}\n")
                    self.output_text.insert(tk.END, "-" * 55 + "\n")

                    if desaprobados:
                        self.output_text.insert(tk.END, "\n❌ Desaprobados:\n")
                        for est in desaprobados:
                            self.output_text.insert(tk.END, f"  • {est}\n")

                    if aprobados:
                        self.output_text.insert(tk.END, "\n✅ Aprobados:\n")
                        for est in aprobados:
                            self.output_text.insert(tk.END, f"  • {est}\n")

                    self.output_text.insert(tk.END, "\n")

                except Exception as e:
                    self.output_text.insert(
                        tk.END, f"⚠️ Error al procesar {nombre_archivo}: {str(e)}\n\n"
                    )


    def reload_files(self):
        """Recarga archivos de NOTAS"""
        self.dataframes = {}
        if self.csv_paths:
            self.dataframes = load_csv_files(self.csv_paths)

    def reload_files_iefs(self):
        """Recarga archivos de IEFs"""
        self.dataframes_iefs = {}
        if self.csv_paths_iefs:
            self.dataframes_iefs = load_csv_files(self.csv_paths_iefs)  
    
    

    def run(self):
        self.root.mainloop()















