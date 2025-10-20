import pandas as pd
import numpy as np

def create_composite_key(df, key_columns):
    """Crea una columna de clave única concatenando las columnas especificadas."""
    if not key_columns:
        raise ValueError("Se debe seleccionar al menos una columna para la clave.")
    return df[key_columns].astype(str).agg('-'.join, axis=1)

def compare_dataframes(df1, df2, keys1, keys2, val_col1=None, val_col2=None):
    """
    Compara dos DataFrames. Devuelve tres resultados:
    1. Filas de df1 que no están en df2.
    2. Filas de df2 que no están en df1.
    3. Filas que existen en ambos pero con valores diferentes en las columnas especificadas.
    """
    df1_copy = df1.copy()
    df2_copy = df2.copy()
    
    # Guardamos el índice original para una selección precisa después del merge
    df1_copy.reset_index(inplace=True)
    df2_copy.reset_index(inplace=True)

    # Creamos la clave de comparación en ambas tablas
    df1_copy['__temp_key__'] = create_composite_key(df1_copy, keys1)
    df2_copy['__temp_key__'] = create_composite_key(df2_copy, keys2)
    
    # Realizamos el merge exterior para capturar todas las filas
    merged_df = pd.merge(
        df1_copy, 
        df2_copy, 
        on='__temp_key__', 
        how='outer', 
        indicator=True,
        suffixes=('_f1', '_f2')
    )
    
    # --- 1. Filas Faltantes ---
    # Filas que solo están en el fichero 1
    missing_in_df2_merged = merged_df[merged_df['_merge'] == 'left_only']
    # Filas que solo están en el fichero 2
    missing_in_df1_merged = merged_df[merged_df['_merge'] == 'right_only']
    
    # Obtenemos los índices originales para seleccionar las filas correctas
    original_indices_missing_in_2 = missing_in_df2_merged['index_f1']
    original_indices_missing_in_1 = missing_in_df1_merged['index_f2']

    result_missing_in_2 = df1.loc[original_indices_missing_in_2]
    result_missing_in_1 = df2.loc[original_indices_missing_in_1]
    
    # --- 2. Comparación de Valores ---
    value_mismatches_df = pd.DataFrame() # Creamos un DF vacío por si no se compara nada

    # Solo procedemos si el usuario ha seleccionado columnas para comparar valores
    if val_col1 and val_col2:
        # Filtramos las filas que existen en ambos ficheros
        common_rows = merged_df[merged_df['_merge'] == 'both'].copy()
        
        # Construimos los nombres de las columnas de valor después del merge
        val_col1_merged = val_col1 + '_f1'
        val_col2_merged = val_col2 + '_f2'
        
        # Rellenamos valores nulos (NaN, None) para poder compararlos de forma segura
        common_rows[val_col1_merged] = common_rows[val_col1_merged].fillna('[VACÍO]')
        common_rows[val_col2_merged] = common_rows[val_col2_merged].fillna('[VACÍO]')

        # La condición de diferencia: los valores no son iguales (tras convertirlos a string)
        mismatch_condition = common_rows[val_col1_merged].astype(str) != common_rows[val_col2_merged].astype(str)
        
        mismatched_rows = common_rows[mismatch_condition]
        
        if not mismatched_rows.empty:
            # Creamos el DataFrame de salida con el formato solicitado
            value_mismatches_df = mismatched_rows[['__temp_key__', val_col1_merged, val_col2_merged]].copy()
            value_mismatches_df.rename(columns={
                '__temp_key__': 'ID de Comparación',
                val_col1_merged: f'Valor Fichero 1 ({val_col1})',
                val_col2_merged: f'Valor Fichero 2 ({val_col2})'
            }, inplace=True)

    return result_missing_in_2, result_missing_in_1, value_mismatches_df