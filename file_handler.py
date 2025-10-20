import pandas as pd

def load_data(file_path):
    """
    Carga un fichero Excel o CSV y lo devuelve como un DataFrame de Pandas.
    Detecta automáticamente el separador (coma o punto y coma) para ficheros CSV.
    """
    try:
        if file_path.endswith('.csv'):
            # --- LÓGICA DE IMPORTACIÓN CORRECTA ---
            try:
                # Usamos sep=None y engine='python' para que Pandas infiera el separador.
                # Esto funciona tanto para comas como para punto y coma.
                # 'utf-8-sig' es robusto contra problemas de codificación (BOM de Excel).
                df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8-sig')
            except Exception:
                # Si lo anterior falla (normalmente por codificación), probamos con 'latin1'.
                df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin1')
            
            # Comprobación de seguridad: Si después de la autodetección seguimos con una 
            # sola columna, es posible que el fichero tenga un formato muy extraño.
            # Este aviso puede ayudar a depurar si surge un problema.
            if df.shape[1] == 1:
                print(f"Advertencia: El fichero CSV '{file_path}' se ha cargado con una sola columna. "
                      f"Asegúrese de que el separador sea estándar (coma o punto y coma).")

        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            print(f"Formato de fichero no soportado: {file_path}")
            return None
        return df
    except Exception as e:
        print(f"Error crítico al cargar el fichero {file_path}: {e}")
        return None