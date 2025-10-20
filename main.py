from app import App

# Intentar cerrar splash (si PyInstaller lo usa)
try:
    import pyi_splash
except ModuleNotFoundError:
    pyi_splash = None


def main():
    app = App()
    if pyi_splash is not None:
        try:
            pyi_splash.close()
        except Exception:
            pass
    app.mainloop()


if __name__ == "__main__":
    main()


# Ejemplo de build (opcional):
# C:\Py\WPy64-31110\python-3.11.1.amd64\Scripts\pyinstaller.exe --onefile --windowed --name="ComparadorPro" --splash="splash.png" main.py
