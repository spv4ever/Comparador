import tkinter as tk
from tkinter import ttk


class ChecklistDialog(tk.Toplevel):
    def __init__(self, parent, title, choices, selected_choices=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.transient(parent)
        self.grab_set()

        if selected_choices is None:
            selected_choices = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Buscador ---
        search_frame = ttk.Frame(self, padding=(10, 10, 10, 5))
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_choices)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")

        # --- Lista de checks con scroll ---
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
            cb = ttk.Checkbutton(self.scrollable_frame, text=choice, variable=var,
                                 onvalue=choice, offvalue="")
            cb.pack(anchor="w", padx=10, pady=2, fill="x")
            self.checkboxes[choice] = cb

        # --- Botonera ---
        button_frame = ttk.Frame(self, padding=(10, 5, 10, 10))
        button_frame.grid(row=2, column=0, sticky="e")

        ok_button = ttk.Button(button_frame, text="Aceptar", command=self._on_ok, style="Accent.TButton")
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        ok_button.pack(side="left", padx=5)
        cancel_button.pack(side="left")

        # --- Tamaño/posición: centrado sobre el padre ---
        self.update_idletasks()

        # Dimensiones del diálogo (si aún no tiene tamaño, fija uno base)
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 400, 500
            self.geometry(f"{w}x{h}")

        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()

        # Posición y tamaño del padre
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        if pw <= 1 or ph <= 1:
            parent.update_idletasks()
            pw = parent.winfo_width()
            ph = parent.winfo_height()

        # Centro relativo al padre
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2

        self.geometry(f"{w}x{h}+{x}+{y}")
        self.minsize(300, 400)
        search_entry.focus_set()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _filter_choices(self, *args):
        search_term = self.search_var.get().lower()
        for choice, checkbox in self.checkboxes.items():
            if search_term in choice.lower():
                checkbox.pack(anchor="w", padx=10, pady=2, fill="x")
            else:
                checkbox.pack_forget()

    def _on_ok(self):
        self.result = [var.get() for var in self.vars.values() if var.get()]
        self.destroy()
