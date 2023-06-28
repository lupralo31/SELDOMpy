import random as rdm
# Se importa la libreria random para el calculo del numero uniforme para la ruleta


def getRandomLBODEmodel(adjMat, maxInput):
    if maxInput == len(adjMat):  # Si maxInput coindide con el nº de entradas ya sé que adjMat será 1s toda
        for i in range(len(adjMat)):
            adjMat[i] = [1]*maxInput
        return adjMat
    # Funcion para realizar la simulacion de la ruleta
    sumcol = 0
    # Ahora hago el paso de sumar todos los elementos de cada columna de adjMat y dividir cada uno
    # de ellos entre la suma total
    for i in range(len(adjMat[0])):  # Recorro columnas
        for j in range(len(adjMat)):  # Recorro filas de cada columna
            sumcol += adjMat[j][i]
        for j in range(len(adjMat)):
            adjMat[j][i] = round(adjMat[j][i] / sumcol, 8)
        sumcol = 0

    temp = []  # Cada matriz interior es una columna y los nºs dentro de cada matriz son las filas con 1s en esa columna
    for i in range(len(adjMat[0])):
        temp.append([])
    colacum = 0  # Valor acumulado al ir sumando elementos de una columna tratando de supera al nº uniforme
    k = 0  # Variable para recorrer las columnas
    while k < len(adjMat[0]):  # Recorro columnas
        nrandom = rdm.uniform(0, 1)  # Genero el número uniforme para hacer las comparaciones
        colacum = adjMat[0][k]  # Al empezar a comparar el numero acumulado es el primer elemento de la columna
        h = 0  # Variable para recorrer las filas
        while h < len(adjMat):  # Recorro filas de cada columna
            if colacum <= nrandom:
                # Si el elemento de la columna acumulado de ir sumando es menor que el nº uniforme continuo
                colacum += adjMat[h + 1][k]  # Le sumo el elemento de la siguiente fila para la siguiente comparacion
                h += 1  # Paso a la siguiente fila
                continue  # Vuelvo al inicio del bucle while para la siguiente fila
            if (colacum > nrandom) and (h not in temp[k]):
                # Si el elemento acumulado es mayor que el uniforme y esa fila no esta aun en temp[columna]
                temp[k].append(h)  # Añado la fila a temp[columna]
                if len(temp[k]) == maxInput:  # Si ya tengo nmaxbins filas en temp[columna]
                    k += 1  # Paso a la siguiente columna
                    break  # Voy al inicio del bucle while grande para la siguiente columna
                if len(temp[k]) < maxInput:  # Si aun no tengo nmaxbins filas en temp[columna]
                    break  # Voy al inicio del bucle while grande para la misma columna, pero con otro numero uniforme
            if (colacum > nrandom) and (h in temp[k]):
                break

    # Una vez calculada la lista temp expreso ya la adjMat con 1s en los elementos recogidos en temp y el resto 0s
    for i in range(len(adjMat)):  # Recorro filas
        for j in range(len(adjMat[i])):  # Recorro columnas de cada fila
            adjMat[j][i] = 0  # Primero pongo toda la matriz a 0

    for i in range(len(temp)):  # Recorro columnas
        for j in temp[i]:  # Recorro filas de cada columna
            adjMat[j][i] = 1

    return adjMat
