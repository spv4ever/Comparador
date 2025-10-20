import os
from pathlib import Path
import configparser


APP_NAME = "Comparador"
CFG_FILE = "ajustes.ini"


class SettingsManager:
    """
    Persistencia simple en un INI:
      [window]
      geometry=1200x800+X+Y
      maximized=0/1

      [theme]
      mode=light|dark
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = self._resolve_path()

    # -----------------------------
    #   Path de configuración
    # -----------------------------
    def _resolve_path(self) -> Path:
        # Windows: %APPDATA%\Comparador\ajustes.ini
        base = os.getenv("APPDATA")
        if not base:
            base = str(Path.home())
        cfg_dir = Path(base) / APP_NAME
        cfg_dir.mkdir(parents=True, exist_ok=True)
        return cfg_dir / CFG_FILE

    # -----------------------------
    #   API pública
    # -----------------------------
    def load(self):
        if self.path.exists():
            try:
                self.config.read(self.path, encoding="utf-8")
            except Exception:
                self.config = configparser.ConfigParser()

    def save(self):
        try:
            with self.path.open("w", encoding="utf-8") as f:
                self.config.write(f)
        except Exception:
            pass

    # --- Geometry ---
    def get_geometry(self):
        geom = None
        maximized = False
        if self.config.has_section("window"):
            geom = self.config.get("window", "geometry", fallback=None)
            maximized = self.config.getboolean("window", "maximized", fallback=False)
        return geom, maximized

    def set_geometry(self, geometry: str, maximized: bool):
        if not self.config.has_section("window"):
            self.config.add_section("window")
        self.config.set("window", "geometry", str(geometry))
        self.config.set("window", "maximized", "1" if maximized else "0")

    # --- Theme ---
    def get_theme(self):
        if self.config.has_section("theme"):
            return self.config.get("theme", "mode", fallback=None)
        return None

    def set_theme(self, mode: str):
        mode = (mode or "light").lower()
        if not self.config.has_section("theme"):
            self.config.add_section("theme")
        self.config.set("theme", "mode", "dark" if mode == "dark" else "light")
