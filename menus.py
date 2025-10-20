import tkinter as tk


def create_menubar(app):
    """
    Construye la barra de menús.
    `app` debe exponer `theme` (ThemeManager) con set_light_theme(), set_dark_theme(), toggle_theme().
    """
    menubar = tk.Menu(app)
    app.config(menu=menubar)

    view_menu = tk.Menu(menubar, tearoff=False)
    theme_menu = tk.Menu(view_menu, tearoff=False)

    theme_menu.add_command(label="Claro", command=app.theme.set_light_theme)
    theme_menu.add_command(label="Oscuro", command=app.theme.set_dark_theme)
    view_menu.add_cascade(label="Tema", menu=theme_menu)
    view_menu.add_command(label="Alternar (Ctrl+T)", command=app.theme.toggle_theme)

    menubar.add_cascade(label="Ver", menu=view_menu)
