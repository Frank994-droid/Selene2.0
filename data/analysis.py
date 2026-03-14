import pandas as pd
def generar_lista_desaprobados_y_aprobados(df, columna, n_estudiantes):
    """
    Devuelve dos listas:
    - desaprobados
    - aprobados
    Solo considera notas numéricas válidas.
    """

    desaprobados = []
    aprobados = []

    for i in range(n_estudiantes):
        nota = df[columna].iloc[i]

        # Ignorar celdas vacías o no numéricas
        if pd.isna(nota):
            continue

        nombre = (
            f"{df['Apellido'].iloc[i]}, "
            f"{str(df['Nombres'].iloc[i]).title()}"
        )

        if 1 <= nota < 7:
            desaprobados.append(nombre)
        elif nota >= 7:
            aprobados.append(nombre)

        # cualquier otro valor queda ignorado

    return desaprobados, aprobados




    
def nota_valida(val):
    try:
        n = int(val)
        return 1 <= n <= 10
    except Exception:
        return False




