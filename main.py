import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk

# --- OTROS IMPORTS ---
import file_handler
import comparison_logic
import utils
import export_handler

# --- SOLUCIÓN: Intentar importar pyi_splash, pero no fallar si no existe ---
try:
    import pyi_splash
except ModuleNotFoundError:
    # Esto nos permite ejecutar el script directamente sin el error
    pass

# (El resto de la clase ChecklistDialog no cambia)
class ChecklistDialog(tk.Toplevel):
    # ... (pega aquí la clase ChecklistDialog de la respuesta anterior, no ha cambiado)
    def __init__(self, parent, title, choices, selected_choices=[]):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.transient(parent)
        self.grab_set()
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        search_frame = ttk.Frame(self, padding=(10, 10, 10, 5))
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_choices)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")
        list_frame = ttk.Frame(self)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.vars = {}
        self.checkboxes = {}
        for choice in choices:
            var = tk.StringVar(value=choice if choice in selected_choices else "")
            self.vars[choice] = var
            cb = ttk.Checkbutton(self.scrollable_frame, text=choice, variable=var, onvalue=choice, offvalue="")
            cb.pack(anchor="w", padx=10, pady=2, fill="x")
            self.checkboxes[choice] = cb
        button_frame = ttk.Frame(self, padding=(10, 5, 10, 10))
        button_frame.grid(row=2, column=0, sticky="e")
        ok_button = ttk.Button(button_frame, text="Aceptar", command=self._on_ok, style="Accent.TButton")
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        ok_button.pack(side="left", padx=5)
        cancel_button.pack(side="left")
        self.update_idletasks()
        win_width, win_height = 400, 500
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        pos_x, pos_y = (screen_width // 2) - (win_width // 2), (screen_height // 2) - (win_height // 2)
        self.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")
        self.minsize(300, 400)
        search_entry.focus_set()

    def _on_canvas_configure(self, event): self.canvas.itemconfig(self.frame_id, width=event.width)
    def _on_frame_configure(self, event): self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def _filter_choices(self, *args):
        search_term = self.search_var.get().lower()
        for choice, checkbox in self.checkboxes.items():
            if search_term in choice.lower(): checkbox.pack(anchor="w", padx=10, pady=2, fill="x")
            else: checkbox.pack_forget()
    def _on_ok(self):
        self.result = [var.get() for var in self.vars.values() if var.get()]
        self.destroy()

# (El resto de la clase App no cambia)
class App(ThemedTk):
    # ... (pega aquí la clase App de la respuesta anterior, no ha cambiado)
    def __init__(self):
        super().__init__()
        
        self.set_theme("arc")
        self.title("Comparador de Ficheros Pro")
        self.geometry("1200x800")

        self.df1, self.df2 = None, None
        self.keys1, self.keys2 = [], []
        self.missing_in_2_df, self.missing_in_1_df, self.value_mismatches_df = None, None, None
        
        self._create_widgets()

    def _create_widgets(self):
        style = ttk.Style()
        style.configure("TLabelFrame.Label", font=("Helvetica", 11, "bold"))

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        files_frame = ttk.LabelFrame(main_frame, text="1. Carga y Selección")
        files_frame.pack(fill=tk.X, padx=5, pady=5)
        files_frame.columnconfigure(1, weight=1)
        files_frame.columnconfigure(3, weight=1)

        # --- Fichero 1 ---
        ttk.Button(files_frame, text="Cargar Fichero 1", command=lambda: self.load_file(1)).grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.path1_label = ttk.Label(files_frame, text="No se ha cargado ningún fichero", wraplength=400, justify=tk.LEFT)
        self.path1_label.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        ttk.Label(files_frame, text="Clave(s) Fichero 1:").grid(row=1, column=0, padx=10, pady=5, sticky="ne")
        self.keys1_label = ttk.Label(files_frame, text="Ninguna seleccionada", foreground="blue", wraplength=350)
        self.keys1_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        key_buttons_frame1 = ttk.Frame(files_frame)
        key_buttons_frame1.grid(row=1, column=0, padx=5, pady=5, sticky="se")
        ttk.Button(key_buttons_frame1, text="Seleccionar...", command=lambda: self._open_key_selector(1)).pack(side=tk.LEFT)
        ttk.Button(key_buttons_frame1, text="Limpiar", command=lambda: self._clear_selection(1)).pack(side=tk.LEFT, padx=5)

        ttk.Label(files_frame, text="Comparar valor de:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.val_col1_combo = ttk.Combobox(files_frame, state="readonly")
        self.val_col1_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # --- Fichero 2 ---
        ttk.Button(files_frame, text="Cargar Fichero 2", command=lambda: self.load_file(2)).grid(row=0, column=2, padx=10, pady=10, sticky="nw")
        self.path2_label = ttk.Label(files_frame, text="No se ha cargado ningún fichero", wraplength=400, justify=tk.LEFT)
        self.path2_label.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        ttk.Label(files_frame, text="Clave(s) Fichero 2:").grid(row=1, column=2, padx=10, pady=5, sticky="ne")
        self.keys2_label = ttk.Label(files_frame, text="Ninguna seleccionada", foreground="blue", wraplength=350)
        self.keys2_label.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        key_buttons_frame2 = ttk.Frame(files_frame)
        key_buttons_frame2.grid(row=1, column=2, padx=5, pady=5, sticky="se")
        ttk.Button(key_buttons_frame2, text="Seleccionar...", command=lambda: self._open_key_selector(2)).pack(side=tk.LEFT)
        ttk.Button(key_buttons_frame2, text="Limpiar", command=lambda: self._clear_selection(2)).pack(side=tk.LEFT, padx=5)

        ttk.Label(files_frame, text="Comparar valor de:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.val_col2_combo = ttk.Combobox(files_frame, state="readonly")
        self.val_col2_combo.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # --- Botón de Comparación ---
        compare_frame = ttk.Frame(main_frame)
        compare_frame.pack(pady=20)
        ttk.Label(compare_frame, text="2.", font=("Helvetica", 11, "bold")).pack(side=tk.LEFT, padx=(0,5))
        compare_button = ttk.Button(compare_frame, text="Realizar Comparación", command=self.compare_files, style="Accent.TButton")
        compare_button.pack(side=tk.LEFT)
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))
        
        # --- Resultados ---
        results_frame = ttk.LabelFrame(main_frame, text="3. Resultados")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        tab1 = ttk.Frame(notebook); notebook.add(tab1, text="Faltan en Fichero 2")
        export_frame1 = ttk.Frame(tab1); export_frame1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame1, text="Exportar a Excel/CSV", command=lambda: export_handler.export_to_file(self.missing_in_2_df)).pack(side=tk.LEFT)
        self.tree1 = self._create_treeview_with_scrollbars(tab1)

        tab2 = ttk.Frame(notebook); notebook.add(tab2, text="Faltan en Fichero 1")
        export_frame2 = ttk.Frame(tab2); export_frame2.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame2, text="Exportar a Excel/CSV", command=lambda: export_handler.export_to_file(self.missing_in_1_df)).pack(side=tk.LEFT)
        self.tree2 = self._create_treeview_with_scrollbars(tab2)

        tab3 = ttk.Frame(notebook); notebook.add(tab3, text="Diferencias de Valor")
        export_frame3 = ttk.Frame(tab3); export_frame3.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame3, text="Exportar a Excel/CSV", command=lambda: export_handler.export_to_file(self.value_mismatches_df)).pack(side=tk.LEFT)
        self.tree3 = self._create_treeview_with_scrollbars(tab3)

    def load_file(self, file_num):
        file_path = filedialog.askopenfilename(title=f"Selecciona el Fichero {file_num}", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if not file_path: return
        
        df = file_handler.load_data(file_path)
        if df is None: messagebox.showerror("Error", f"No se pudo cargar el fichero: {file_path}"); return
        
        cols_with_none = ["-- No Comparar --"] + df.columns.tolist()
        if file_num == 1:
            self.df1 = df
            self.path1_label.config(text=file_path)
            self._clear_selection(1)
            self.val_col1_combo['values'] = cols_with_none
            self.val_col1_combo.current(0)
        else:
            self.df2 = df
            self.path2_label.config(text=file_path)
            self._clear_selection(2)
            self.val_col2_combo['values'] = cols_with_none
            self.val_col2_combo.current(0)

    def compare_files(self):
        if self.df1 is None or self.df2 is None: messagebox.showwarning("Aviso", "Debes cargar ambos ficheros."); return
        if not self.keys1 or not self.keys2: messagebox.showwarning("Aviso", "Debes seleccionar al menos una clave en cada fichero."); return
        
        val_col1, val_col2 = self.val_col1_combo.get(), self.val_col2_combo.get()
        val_col1 = None if val_col1 == "-- No Comparar --" else val_col1
        val_col2 = None if val_col2 == "-- No Comparar --" else val_col2
        
        if bool(val_col1) != bool(val_col2): messagebox.showwarning("Aviso", "Para comparar valores, debe seleccionar una columna en ambos ficheros o en ninguno."); return

        try:
            missing_in_2, missing_in_1, value_mismatches = comparison_logic.compare_dataframes(
                self.df1, self.df2, self.keys1, self.keys2, val_col1, val_col2
            )
            self.missing_in_2_df, self.missing_in_1_df, self.value_mismatches_df = missing_in_2, missing_in_1, value_mismatches
            
            utils.display_df_in_treeview(self.tree1, self.missing_in_2_df)
            utils.display_df_in_treeview(self.tree2, self.missing_in_1_df)
            utils.display_df_in_treeview(self.tree3, self.value_mismatches_df)
            
            messagebox.showinfo("Completado", "La comparación ha finalizado.")
        except Exception as e:
            messagebox.showerror("Error en la comparación", str(e))

    def _open_key_selector(self, file_num):
        df, keys, title = (self.df1, self.keys1, "Fichero 1") if file_num == 1 else (self.df2, self.keys2, "Fichero 2")
        if df is None: messagebox.showinfo("Aviso", f"Primero debe cargar el {title}."); return
        
        dialog = ChecklistDialog(self, f"Seleccionar Claves para {title}", df.columns.tolist(), keys)
        self.wait_window(dialog)

        if dialog.result is not None:
            if file_num == 1: self.keys1 = dialog.result; self._update_keys_label(self.keys1_label, self.keys1)
            else: self.keys2 = dialog.result; self._update_keys_label(self.keys2_label, self.keys2)

    def _clear_selection(self, file_num):
        if file_num == 1: self.keys1 = []; self._update_keys_label(self.keys1_label, self.keys1)
        else: self.keys2 = []; self._update_keys_label(self.keys2_label, self.keys2)

    def _update_keys_label(self, label, keys):
        label.config(text="Ninguna seleccionada" if not keys else ", ".join(keys))

    def _create_treeview_with_scrollbars(self, parent):
        tree_frame = ttk.Frame(parent); tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview); vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview); hsb.pack(side='bottom', fill='x')
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree


if __name__ == "__main__":
    app = App()
    
    # --- SOLUCIÓN: Intentar cerrar el splash, pero no fallar si no existe ---
    try:
        pyi_splash.close()
    except NameError:
        # pyi_splash no está definido porque el import falló, lo cual es correcto
        pass
        
    app.mainloop()

##### C:\Py\WPy64-31110\python-3.11.1.amd64\Scripts\pyinstaller.exe --onefile --windowed --name="ComparadorPro" --splash="splash.png" main.py