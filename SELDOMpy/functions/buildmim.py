import numpy as np
# Se importa la librería numpy necesaria para los histogramas de la información mutua
from sklearn.metrics import mutual_info_score
# Importo la función mutual_info_score para calcular la información mutua entre 2 variables, pero el problema es que
# me da valores mayores que 1 y en el ejemplo del paper está calculada entre 0 y 1, por lo que normalizaré
from math import sqrt, ceil
# Importo la función sqrt que me permite hacer raíces cuadradas del módulo math
# Importo la función ceil que me permite hacer redondeos hacia arriba del módulo math


def calc_mi(x, y, nbins):  # Función para calcular la información mutua entre 2 nodos a partir de 2 listas de medidas
    if nbins == 0:
        bins = ceil(sqrt(len(x)*2))  # Calculo el numero de divisiones óptimo para discretizar los valores de medida
    else:
        bins = nbins
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi


def buildmim(conc_data, nbins=0):  # Función para calcular la matriz de adyacencia a partir de conc_data
    # adjMat estará formada por 4 listas que representan las 4 filas de la matriz del programa de R
    # Se puede especificar el numero de divisiones para la discretizacion de las medidas
    adjMat = []
    dataArray = []  # Matriz auxiliar porque a la funcion que calcula la informacion mutua hay que pasarle listas
    for i in range(len(conc_data[0])):
        adjMat.append([])
        dataArray.append([])

    for i in range(len(conc_data[0])):  # Recorro columnas
        for j in range(len(conc_data)):  # Recorro filas de cada columna
            dataArray[i].append(conc_data[j][i])

    for i in range(len(dataArray)):
        for j in range(len(dataArray)):
            mi = calc_mi(dataArray[i], dataArray[j], nbins)
            adjMat[i].append(mi)
    maxvalue = 0

    for i in range(len(adjMat)):
        for j in range(len(adjMat[i])):
            if adjMat[i][j] > maxvalue:
                maxvalue = adjMat[i][j]

    for i in range(len(adjMat)):
        for j in range(len(adjMat[i])):
            if i == j:
                adjMat[i][j] = 0
            else:
                adjMat[i][j] = round(adjMat[i][j]/maxvalue, 8)

    return adjMat
