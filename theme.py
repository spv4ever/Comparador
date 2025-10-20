from tkinter import ttk


class ThemeManager:
    """
    Gestiona el tema ttk y (si está disponible) sv-ttk.
    Guarda/restaura el modo (claro/oscuro) usando SettingsManager.
    """
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self._has_svttk = False
        self._dark_mode = False
        self._sv_ttk = None

    def init_theme(self):
        style = ttk.Style(self.root)

        # Tema ttk “seguro” (Windows/macOS/Linux)
        preferred = ["vista", "xpnative", "clam"]
        for t in preferred:
            if t in style.theme_names():
                style.theme_use(t)
                break

        # Estilos globales
        style.configure("TLabelFrame.Label", font=("Helvetica", 11, "bold"))
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))
        style.map("Accent.TButton",
                  relief=[("pressed", "sunken"), ("active", "raised")])

        # sv-ttk opcional
        try:
            import sv_ttk
            self._sv_ttk = sv_ttk
            self._has_svttk = True
        except Exception:
            self._sv_ttk = None
            self._has_svttk = False

        # Aplica el modo guardado
        mode = (self.settings.get_theme() or "light").lower()
        if mode == "dark":
            self.set_dark_theme(save=False)
        else:
            self.set_light_theme(save=False)

        # Atajo Ctrl+T para alternar tema
        self.root.bind("<Control-t>", self.toggle_theme)

    def set_light_theme(self, save=True):
        if self._has_svttk:
            self._sv_ttk.use_light_theme()
        self._dark_mode = False
        if save:
            self.settings.set_theme("light")
            self.settings.save()

    def set_dark_theme(self, save=True):
        if self._has_svttk:
            self._sv_ttk.use_dark_theme()
        self._dark_mode = True
        if save:
            self.settings.set_theme("dark")
            self.settings.save()

    def toggle_theme(self, *_):
        if self._dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()

    def current_mode(self):
        return "dark" if self._dark_mode else "light"
