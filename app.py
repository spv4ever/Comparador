import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import file_handler
import comparison_logic
import utils
import export_handler

from dialogs import ChecklistDialog
from theme import ThemeManager
from menus import create_menubar
from settings import SettingsManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Settings (persistencia)
        self.settings = SettingsManager()
        self.settings.load()

        # --- Tema y estilos (lee el modo guardado)
        self.theme = ThemeManager(self, self.settings)
        self.theme.init_theme()

        # --- Ventana principal
        self.title("Comparador de Ficheros Pro")
        # Si prefieres que el tamaño venga por contenido, comenta la línea siguiente:
        self.geometry("1200x800")

        # --- Estado
        self.df1, self.df2 = None, None
        self.keys1, self.keys2 = [], []
        self.missing_in_2_df, self.missing_in_1_df, self.value_mismatches_df = None, None, None

        # --- UI
        self._create_widgets()
        create_menubar(self)

        # --- Aplicar geometría guardada o centrar
        self.after(0, self._apply_saved_or_center)

        # --- Guardar posición/tamaño y tema al salir
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # -----------------------------
    #   Construcción de la UI
    # -----------------------------
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        files_frame = ttk.LabelFrame(main_frame, text="1. Carga y Selección")
        files_frame.pack(fill=tk.X, padx=5, pady=5)
        files_frame.columnconfigure(1, weight=1)
        files_frame.columnconfigure(3, weight=1)

        # --- Fichero 1 ---
        ttk.Button(files_frame, text="Cargar Fichero 1",
                   command=lambda: self.load_file(1)).grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.path1_label = ttk.Label(files_frame, text="No se ha cargado ningún fichero",
                                     wraplength=400, justify=tk.LEFT)
        self.path1_label.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(files_frame, text="Clave(s) Fichero 1:").grid(row=1, column=0, padx=10, pady=5, sticky="ne")
        self.keys1_label = ttk.Label(files_frame, text="Ninguna seleccionada",
                                     foreground="blue", wraplength=350)
        self.keys1_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        key_buttons_frame1 = ttk.Frame(files_frame)
        key_buttons_frame1.grid(row=1, column=0, padx=5, pady=5, sticky="se")
        ttk.Button(key_buttons_frame1, text="Seleccionar...",
                   command=lambda: self._open_key_selector(1)).pack(side=tk.LEFT)
        ttk.Button(key_buttons_frame1, text="Limpiar",
                   command=lambda: self._clear_selection(1)).pack(side=tk.LEFT, padx=5)

        ttk.Label(files_frame, text="Comparar valor de:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.val_col1_combo = ttk.Combobox(files_frame, state="readonly")
        self.val_col1_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # --- Fichero 2 ---
        ttk.Button(files_frame, text="Cargar Fichero 2",
                   command=lambda: self.load_file(2)).grid(row=0, column=2, padx=10, pady=10, sticky="nw")
        self.path2_label = ttk.Label(files_frame, text="No se ha cargado ningún fichero",
                                     wraplength=400, justify=tk.LEFT)
        self.path2_label.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        ttk.Label(files_frame, text="Clave(s) Fichero 2:").grid(row=1, column=2, padx=10, pady=5, sticky="ne")
        self.keys2_label = ttk.Label(files_frame, text="Ninguna seleccionada",
                                     foreground="blue", wraplength=350)
        self.keys2_label.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        key_buttons_frame2 = ttk.Frame(files_frame)
        key_buttons_frame2.grid(row=1, column=2, padx=5, pady=5, sticky="se")
        ttk.Button(key_buttons_frame2, text="Seleccionar...",
                   command=lambda: self._open_key_selector(2)).pack(side=tk.LEFT)
        ttk.Button(key_buttons_frame2, text="Limpiar",
                   command=lambda: self._clear_selection(2)).pack(side=tk.LEFT, padx=5)

        ttk.Label(files_frame, text="Comparar valor de:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.val_col2_combo = ttk.Combobox(files_frame, state="readonly")
        self.val_col2_combo.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # --- Botón de Comparación ---
        compare_frame = ttk.Frame(main_frame)
        compare_frame.pack(pady=20)
        ttk.Label(compare_frame, text="2.", font=("Helvetica", 11, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        compare_button = ttk.Button(compare_frame, text="Realizar Comparación",
                                    command=self.compare_files, style="Accent.TButton")
        compare_button.pack(side=tk.LEFT)

        # --- Resultados ---
        results_frame = ttk.LabelFrame(main_frame, text="3. Resultados")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Faltan en Fichero 2")
        export_frame1 = ttk.Frame(tab1); export_frame1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame1, text="Exportar a Excel/CSV",
                   command=lambda: export_handler.export_to_file(self.missing_in_2_df)).pack(side=tk.LEFT)
        self.tree1 = self._create_treeview_with_scrollbars(tab1)

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Faltan en Fichero 1")
        export_frame2 = ttk.Frame(tab2); export_frame2.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame2, text="Exportar a Excel/CSV",
                   command=lambda: export_handler.export_to_file(self.missing_in_1_df)).pack(side=tk.LEFT)
        self.tree2 = self._create_treeview_with_scrollbars(tab2)

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Diferencias de Valor")
        export_frame3 = ttk.Frame(tab3); export_frame3.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame3, text="Exportar a Excel/CSV",
                   command=lambda: export_handler.export_to_file(self.value_mismatches_df)).pack(side=tk.LEFT)
        self.tree3 = self._create_treeview_with_scrollbars(tab3)

    def _create_treeview_with_scrollbars(self, parent):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    # -----------------------------
    #   Lógica de acciones
    # -----------------------------
    def load_file(self, file_num: int):
        file_path = filedialog.askopenfilename(
            title=f"Selecciona el Fichero {file_num}",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        df = file_handler.load_data(file_path)
        if df is None:
            messagebox.showerror("Error", f"No se pudo cargar el fichero: {file_path}")
            return

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
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Aviso", "Debes cargar ambos ficheros.")
            return
        if not self.keys1 or not self.keys2:
            messagebox.showwarning("Aviso", "Debes seleccionar al menos una clave en cada fichero.")
            return

        val_col1, val_col2 = self.val_col1_combo.get(), self.val_col2_combo.get()
        val_col1 = None if val_col1 == "-- No Comparar --" else val_col1
        val_col2 = None if val_col2 == "-- No Comparar --" else val_col2

        if bool(val_col1) != bool(val_col2):
            messagebox.showwarning("Aviso",
                                   "Para comparar valores, seleccione columna en ambos ficheros o en ninguno.")
            return

        try:
            missing_in_2, missing_in_1, value_mismatches = comparison_logic.compare_dataframes(
                self.df1, self.df2, self.keys1, self.keys2, val_col1, val_col2
            )
            self.missing_in_2_df, self.missing_in_1_df, self.value_mismatches_df = (
                missing_in_2, missing_in_1, value_mismatches
            )

            utils.display_df_in_treeview(self.tree1, self.missing_in_2_df)
            utils.display_df_in_treeview(self.tree2, self.missing_in_1_df)
            utils.display_df_in_treeview(self.tree3, self.value_mismatches_df)

            messagebox.showinfo("Completado", "La comparación ha finalizado.")
        except Exception as e:
            messagebox.showerror("Error en la comparación", str(e))

    def _open_key_selector(self, file_num: int):
        df, keys, title = (self.df1, self.keys1, "Fichero 1") if file_num == 1 else (self.df2, self.keys2, "Fichero 2")
        if df is None:
            messagebox.showinfo("Aviso", f"Primero debe cargar el {title}.")
            return

        dialog = ChecklistDialog(self, f"Seleccionar Claves para {title}", df.columns.tolist(), keys)
        self.wait_window(dialog)

        if dialog.result is not None:
            if file_num == 1:
                self.keys1 = dialog.result
                self._update_keys_label(self.keys1_label, self.keys1)
            else:
                self.keys2 = dialog.result
                self._update_keys_label(self.keys2_label, self.keys2)

    def _clear_selection(self, file_num: int):
        if file_num == 1:
            self.keys1 = []
            self._update_keys_label(self.keys1_label, self.keys1)
        else:
            self.keys2 = []
            self._update_keys_label(self.keys2_label, self.keys2)

    def _update_keys_label(self, label, keys):
        label.config(text="Ninguna seleccionada" if not keys else ", ".join(keys))

    # -----------------------------
    #   Geometría / centrado / persistencia
    # -----------------------------
    def _apply_saved_or_center(self):
        geom, maximized = self.settings.get_geometry()
        if geom:
            try:
                self.geometry(geom)
                self.update_idletasks()
                if maximized:
                    # En Windows: estado 'zoomed' es maximizado
                    self.state('zoomed')
            except Exception:
                # Si la geometría guardada no es válida, centramos
                self._center_on_screen()
        else:
            self._center_on_screen()

    def _center_on_screen(self, width=None, height=None):
        """Centra la ventana principal en la pantalla actual."""
        self.update_idletasks()
        w = width or self.winfo_width()
        h = height or self.winfo_height()
        if w <= 1:
            w = self.winfo_reqwidth()
        if h <= 1:
            h = self.winfo_reqheight()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.update_idletasks()

    def _on_close(self):
        """Guarda geometría y tema, y cierra."""
        try:
            maximized = (self.state() == 'zoomed')
            geom = self.geometry()
            self.settings.set_geometry(geom, maximized)
            # El tema ya se guarda al cambiar; aquí no hace falta, pero no molesta:
            self.settings.set_theme(self.theme.current_mode())
            self.settings.save()
        except Exception:
            pass
        self.destroy()
