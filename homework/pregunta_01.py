"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


import pandas as pd
import re
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Conservamos solo las líneas de datos (saltamos las primeras 4 líneas de encabezado)
    data_lines = lines[4:]

    rows = []
    current_cluster = None
    current_quantity = None
    current_percentage = None
    current_keywords = []

    for line in data_lines:
        # Si la línea está vacía o es una línea divisoria, la saltamos
        if not line.strip() or line.strip().startswith("---"):
            continue

        # Buscamos si la línea comienza con el número de un clúster
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,.]+)\s*%\s*(.*)", line)

        if match:
            # Si ya veníamos acumulando un clúster anterior, lo procesamos y guardamos
            if current_cluster is not None:
                # Unimos las líneas con un espacio, luego colapsamos múltiples espacios a uno solo
                keywords_str = " ".join(current_keywords).strip()
                keywords_str = re.sub(r"\s+", " ", keywords_str)
                
                if keywords_str.endswith("."):
                    keywords_str = keywords_str[:-1]
                
                rows.append([current_cluster, current_quantity, current_percentage, keywords_str])

            # Inicializamos los datos del nuevo clúster
            current_cluster = int(match.group(1))
            current_quantity = int(match.group(2))
            current_percentage = float(match.group(3).replace(",", "."))
            current_keywords = [match.group(4).strip()]
        else:
            # Si la línea no empieza con número, es continuación de las palabras clave
            if current_cluster is not None:
                current_keywords.append(line.strip())

    # Guardar el último clúster procesado al salir del ciclo
    if current_cluster is not None:
        keywords_str = " ".join(current_keywords).strip()
        keywords_str = re.sub(r"\s+", " ", keywords_str)
        if keywords_str.endswith("."):
            keywords_str = keywords_str[:-1]
        rows.append([current_cluster, current_quantity, current_percentage, keywords_str])

    # 2. Definimos los nombres de las columnas ajustando la última según el test
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    # 3. Creamos el DataFrame
    df = pd.DataFrame(rows, columns=columns)

    return df