import tkinter as tk
from tkinter import ttk
from ui.tooltip import ToolTip

#Esto es un respaldo de la interfaz en Tkinter, al pasarse a su extensión Custom Tkinter

def build_ui(self):
        def only_integers(text):
            return text.isdigit() or text == ""
        

        # ───────────────────────────
    # Contenedor principal
        # ───────────────────────────
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Layout en tres columnas
        main_frame.columnconfigure(0, weight=0)  # panel izquierdo
        main_frame.columnconfigure(1, weight=1)  # área central
        main_frame.columnconfigure(2, weight=0)  # panel derecho (simétrico con izquierdo)

        # ───────────────────────────
        # Panel lateral 1 (botones)
        # ───────────────────────────
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 15))

        # ========= SESIÓN =========
        session_frame = ttk.LabelFrame(left_panel, text="Sesión", padding=10)
        session_frame.pack(fill="x", pady=5)


        # ========= ARCHIVOS =========
        files_frame = ttk.LabelFrame(left_panel, text="Archivos de Notas", padding=10)
        files_frame.pack(fill="x", pady=5)

        btn_attach = ttk.Button(
        files_frame,
        text="Adjuntar archivo(s) CSV",
        command=self.attach_csv_files
        )
        btn_attach.pack(fill="x")


        # ⬇️ BOTÓN NUEVO ⬇️
        btn_reload = ttk.Button(
        files_frame,
        text="Recargar archivos",
        command=self.reload_files
        )
        btn_reload.pack(fill="x", pady=(5, 0))

        self.lbl_files_status = ttk.Label(
        files_frame,
        textvariable=self.files_status_var,
        font=("Segoe UI", 9),
        foreground="gray"
        )
        self.lbl_files_status.pack(pady=(5, 0))
        ToolTip(
        btn_reload,
        "Recarga los archivos CSV si fueron modificados\n"
        "sin necesidad de volverlos a seleccionar."
        )


        # ========= DATOS =========
        data_frame = ttk.LabelFrame(left_panel, text="Datos", padding=10)
        data_frame.pack(fill="x", pady=5)

        lbl_students = ttk.Label(
            data_frame,
            text="Cantidad de estudiantes:"
        )
        lbl_students.pack(anchor="w")

        vcmd = (self.root.register(only_integers), "%P")

        self.students_var = tk.StringVar(value="0")
        entry_students = ttk.Entry(
        data_frame,
        width=4,              # suficiente para 2 dígitos
        validate="key",
        validatecommand=vcmd,
        textvariable=self.students_var
        )
        entry_students.pack(anchor="w", pady=(0, 2))



        ToolTip(
        entry_students,
        "Ingresar un número entero.\n"
        "Si los índices van de 0 a n,\n"
        "la cantidad real es n+1.\n"
        "Ej.: 0,1,2,3 → 4 estudiantes."
        )

        # ========= NOTAS =========

        grades_frame = ttk.LabelFrame(left_panel, text="Notas", padding=10)
        grades_frame.pack(fill="x", pady=5)

# --    - Rango ---
        range_frame_grades = ttk.Frame(grades_frame)
        range_frame_grades.pack(fill="x", pady=5)

        ttk.Label(range_frame_grades, text="Desde:").grid(row=0, column=0, sticky="w")
        ttk.Label(range_frame_grades, text="Hasta:").grid(row=0, column=1, sticky="w")
        grade_options = []
        for i in range(1, 9):
                grade_options.extend([f"NE{i}", f"E{i}R1", f"E{i}R2"])

        self.combo_grades_from = ttk.Combobox(
            range_frame_grades, values=grade_options, state="readonly", width=8
        )
        self.combo_grades_from.grid(row=1, column=0, padx=(0, 5))

        self.combo_grades_to = ttk.Combobox(
            range_frame_grades, values=grade_options, state="readonly", width=8
        )
        self.combo_grades_to.grid(row=1, column=1)

        # --- Botones ---
        btn_upload_grades = ttk.Button(grades_frame, text="Subir notas", command=self.iniciar_subida_notas)
        btn_upload_grades.pack(fill="x", pady=(5, 2))

        ToolTip(
            btn_upload_grades,
            "Permite subir notas en un rango específico.\n"
            "Columnas: NE1, R1E1, R2E1 … NE8, R1E8, R2E8."
        )

        btn_delete_grades = ttk.Button(grades_frame, text="Borrar notas")
        btn_delete_grades.pack(fill="x")

        
        #------REPORTES----------------

        eval_options = []
        for i in range(1, 9):
            eval_options.extend([f"EVAL {i}", f"R1E{i}", f"R2E{i}"])

        
              

        reportes_frame = ttk.LabelFrame(left_panel, text="Reportes", padding=10)
        reportes_frame.pack(fill="x", pady=5)

        self.combo_eval_desaprobados = ttk.Combobox(
        reportes_frame,
        values=eval_options,
        state="readonly",
        width=10
        )
        self.combo_eval_desaprobados.pack(fill="x", pady=(0, 5))


        btn_desaprobados = ttk.Button(
        reportes_frame,
        text="Generar lista de (des)aprobados",
        command=self.crear_lista_desaprobados_y_aprobados
        )
        btn_desaprobados.pack(fill="x")
        
        









        # ───────────────────────────
        # Área central (output text)
        # ───────────────────────────
        content_frame = ttk.Frame(main_frame, relief="groove")
        content_frame.grid(row=0, column=1, sticky="nsew")

        # Text principal
        self.output_text = tk.Text(
            content_frame,
            wrap="word",
            height=25
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        ##0f0c29, #302b63, #24243e
        self.output_text.configure(
        background="#24243e",     # fondo oscuro suave
        foreground="#eaeaeb",     # texto claro
        insertbackground="#d6d9e0",
        selectbackground="#3a3f5c",
        relief="sunken",
        borderwidth=0
)

        # Frame inferior para el botón
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        copy_btn = ttk.Button(
            bottom_frame,
            text="Copiar",
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side="right")

        save_btn = ttk.Button(
        bottom_frame,
        text="Guardar .txt",
        command=self.save_to_file
        )
        save_btn.pack(side="right", padx=(0, 5))

        # Panel lateral derecho (simétrico al izquierdo)
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=2, sticky="ns", padx=(15, 0))

        # ───────────────────────────
        # Panel lateral 2 (botones)
        # ───────────────────────────
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=2, sticky="ns", padx=(0, 15))

        


        # ========= ARCHIVOS =========
        files_frame = ttk.LabelFrame(right_panel, text="Archivos de IEFs", padding=10)
        files_frame.pack(fill="x", pady=5)

        btn_attach = ttk.Button(
        files_frame,
        text="Adjuntar archivo(s) CSV",
        command=self.attach_csv_files_iefs
        )
        btn_attach.pack(fill="x")


        # ⬇️ BOTÓN NUEVO ⬇️
        btn_reload_ief = ttk.Button(
        files_frame,
        text="Recargar archivos",
        command=self.reload_files_iefs
        )
        btn_reload_ief.pack(fill="x", pady=(5, 0))

        self.lbl_files_status_ief = ttk.Label(
        files_frame,
        textvariable=self.files_status_var_iefs,
        font=("Segoe UI", 9),
        foreground="gray"
        )
        self.lbl_files_status_ief.pack(pady=(5, 0))
        ToolTip(
        btn_reload,
        "Recarga los archivos CSV si fueron modificados\n"
        "sin necesidad de volverlos a seleccionar."
        )


        # ========= DATOS =========
        data_frame = ttk.LabelFrame(right_panel, text="Datos", padding=10)
        data_frame.pack(fill="x", pady=5)

        
        #========= IEFs =========

        iefs_frame = ttk.LabelFrame(right_panel, text="IEFs", padding=10)
        iefs_frame.pack(fill="x", pady=5)

        # --- Rango ---
        range_frame_iefs = ttk.Frame(iefs_frame)
        range_frame_iefs.pack(fill="x", pady=5)

        ttk.Label(range_frame_iefs, text="Desde:").grid(row=0, column=0, sticky="w")
        ttk.Label(range_frame_iefs, text="Hasta:").grid(row=0, column=1, sticky="w")

        ief_options = [f"Aprendizaje {chr(c)}" for c in range(ord("A"), ord("N") + 1)]

        self.combo_iefs_from = ttk.Combobox(
            range_frame_iefs, values=ief_options, state="readonly", width=14
        )
        self.combo_iefs_from.grid(row=1, column=0, padx=(0, 5))

        self.combo_iefs_to = ttk.Combobox(
            range_frame_iefs, values=ief_options, state="readonly", width=14
        )
        self.combo_iefs_to.grid(row=1, column=1)

        # --- Botones ---
        btn_upload_iefs = ttk.Button(iefs_frame, text="Cargar IEFs", command=self.iniciar_subida_iefs)
        btn_upload_iefs.pack(fill="x", pady=(5, 2))

        ToolTip(
            btn_upload_iefs,
            "Carga aprendizajes en un rango especificado.\n"
            "Columnas: Aprendizaje A hasta Aprendizaje N."
        )

        btn_finalizar_etapa = ttk.Button(iefs_frame, text="Finalizar Etapa", command=self.lanzador_finalizar_etapas)
        btn_finalizar_etapa.pack(fill="x", pady=(5, 2))

        ToolTip(
            btn_finalizar_etapa,
            "Finaliza etapa en cada estudiante.\n"
            "No ingresar texto en Síntesis Final IEF \n"
            "porque se borra automáticamente."
        )

        btn_close_iefs = ttk.Button(iefs_frame, text="Cerrar IEFs", command=self.lanzador_cerrar_iefs)
        btn_close_iefs.pack(fill="x", pady=(5, 2))

        ToolTip(
            btn_close_iefs,
            "Cierra cada IEF, siempre y cuando,\n"
            " se haya cargado la Síntesis Final IEF \n"
            "y todos los aprendizajes tengan su estado"
        )
        





        btn_delete_iefs = ttk.Button(
            iefs_frame, text="Borrar estado de aprendizajes"
        )
        btn_delete_iefs.pack(fill="x")

        ToolTip(
            btn_delete_iefs,
            "Elimina estados cargados para permitir una nueva carga."
        )

        #------REPORTES----------------

        eval_options = []
        for i in range(1, 9):
            eval_options.extend([f"EVAL {i}", f"R1E{i}", f"R2E{i}"])

        reportes_frame = ttk.LabelFrame(right_panel, text="Reportes", padding=10)
        reportes_frame.pack(fill="x", pady=5)

        self.combo_estados = ttk.Combobox(
        reportes_frame,
        values=eval_options,
        state="readonly",
        width=10
        )
        self.combo_estados.pack(fill="x", pady=(0, 5))


        btn_estados = ttk.Button(
        reportes_frame,
        text="Generar lista de estados",
        command=self.crear_lista_estados
        )
        btn_estados.pack(fill="x")
        
        ToolTip(btn_estados, "Genera, a partir de las notas de una columna, \n"
        "una lista de los estados posibles de aprendizajes:\n" 
        "Logrado, EnProceso o Pendiente.")
