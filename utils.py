import tkinter as tk
from tkinter import ttk, font

def display_df_in_treeview(treeview, dataframe):
    """
    Limpia y llena un widget Treeview de Tkinter con los datos de un DataFrame,
    ajustando automáticamente el ancho de las columnas.
    """
    # Limpiar el Treeview actual
    treeview.delete(*treeview.get_children())
    
    if dataframe is None or dataframe.empty:
        treeview["columns"] = []
        return
        
    # Configurar columnas
    treeview["column"] = list(dataframe.columns)
    treeview["show"] = "headings"
    
    df_rows = dataframe.to_numpy().tolist()
    for col_name in dataframe.columns:
        treeview.heading(col_name, text=col_name)
        
        # --- Lógica de auto-ajuste de ancho CORREGIDA ---
        try:
            # INTENTAMOS usar la fuente real para una medición precisa
            font_obj = font.Font(font=treeview.cget("font"))
            header_width = font_obj.measure(col_name)
            
            max_content_width = 0
            sample_data = dataframe[col_name].head(100).astype(str)
            for item in sample_data:
                max_content_width = max(max_content_width, font_obj.measure(item))

        except tk.TclError:
            # FALLBACK si lo anterior falla: usamos una estimación basada en la longitud del texto
            header_width = len(col_name) * 10  # Estimación simple
            
            max_content_width = 0
            sample_data = dataframe[col_name].head(100).astype(str)
            for item in sample_data:
                # Usamos la misma estimación para el contenido
                max_content_width = max(max_content_width, len(item) * 10)

        # Ahora, tanto header_width como max_content_width tienen un valor garantizado
        col_width = max(header_width, max_content_width) + 20 
        final_width = max(50, min(col_width, 400))
        
        treeview.column(col_name, width=final_width, minwidth=50, stretch=tk.NO)

    # Añadir datos al Treeview
    for row in df_rows:
        treeview.insert("", "end", values=row)