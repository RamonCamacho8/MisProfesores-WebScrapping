import pandas as pd
import numpy as np
import re

def eliminar_puntuaciones(texto):
        # Utiliza una expresión regular para eliminar caracteres de puntuación
        return re.sub(r'[^\w\s]', '', texto)

def limpiarCorpus(df : pd.DataFrame):
    df.head()
    df = df.rename(columns={'Comment':'comentario_esp',
                        'Clase':'materia',
                        'Tag':'mp_tag',
                        'Facilidad':'facilidad',
                        'Calidad':'calidad',
                        'Calificación':'calif_Obtenida',
                        'Fecha':'fecha'})
    print('Tamaño del Corpus Inicial: ', len(df), ' filas.')
    for column in df.columns:
        #Remplazamos los comentarios vacios, en espera o bloqueados por valores NaN
        df[column].replace('', np.nan, inplace=True)
        df[column].replace('[Comentario esperando revisión]', np.nan, inplace=True)
        df[column].replace('[Comentario bloqueado]', np.nan, inplace=True)
    
    #Eliminamos todas las filas con NaN
    df = df.dropna()
    #Reiniciamos el index
    df = df.reset_index(drop = True )
    # Función para eliminar puntuaciones
    
    df['comentario_esp'] = df['comentario_esp'].apply(eliminar_puntuaciones)
    df = df[~df['comentario_esp'].apply(lambda x: isinstance(x, float))]
    df = df[~(df['comentario_esp'].str.len() < 5)]

    print('Tamaño del Corpus Final: ', len(df), ' filas.')
    return df