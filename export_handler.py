import pandas as pd
from tkinter import filedialog, messagebox

def export_to_file(dataframe):
    """
    Exporta un DataFrame a un fichero Excel o CSV elegido por el usuario.
    """
    if dataframe is None or dataframe.empty:
        messagebox.showwarning("Aviso", "No hay datos para exportar.")
        return

    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Fichero Excel", "*.xlsx"),
                ("Fichero CSV", "*.csv"),
                ("Todos los ficheros", "*.*")
            ],
            title="Guardar resultados como..."
        )

        if not file_path:
            # El usuario canceló el diálogo
            return

        if file_path.endswith('.xlsx'):
            # El index=False evita que se guarde una columna extra con los índices del DataFrame
            dataframe.to_excel(file_path, index=False)
        elif file_path.endswith('.csv'):
            # sep=';' y encoding='utf-8-sig' son mejores para compatibilidad con Excel en español
            dataframe.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')
        else:
            messagebox.showerror("Error", "Formato de fichero no soportado. Por favor, elija .xlsx o .csv.")
            return

        messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error de Exportación", f"Ocurrió un error al guardar el fichero:\n{e}")