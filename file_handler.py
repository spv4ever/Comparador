import pandas as pd

def load_data(file_path):
    """
    Carga un fichero Excel o CSV y lo devuelve como un DataFrame de Pandas.
    Devuelve None si ocurre un error.
    """
    try:
        if file_path.endswith('.csv'):
            # Para CSV, intentamos detectar el separador, aunque punto y coma es común en español.
            try:
                df = pd.read_csv(file_path, sep=';', encoding='utf-8')
            except Exception:
                 df = pd.read_csv(file_path, sep=',', encoding='latin1')
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            # Si no es un formato soportado, devolvemos None
            return None
        return df
    except Exception as e:
        print(f"Error al cargar el fichero {file_path}: {e}")
        return None