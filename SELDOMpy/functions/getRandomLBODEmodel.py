import random as rdm
# The "random" package is imported for the calculation of the uniform number for roulette


def getRandomLBODEmodel(adjMat, maxInput):
    if maxInput == len(adjMat):  # If "maxInput" coincides with the number of inputs it is already known that "adjMat" will be 1s
        for i in range(len(adjMat)):
            adjMat[i] = [1]*maxInput
        return adjMat
    # Function to perform roulette simulation
    sumcol = 0
    # Now the step is made of adding all the elements of each column of adjMat and dividing each of them by the sum total
    for i in range(len(adjMat[0])):  # The columns are traversed
        for j in range(len(adjMat)):  # Rows of each column are traversed
            sumcol += adjMat[j][i]
        for j in range(len(adjMat)):
            adjMat[j][i] = round(adjMat[j][i] / sumcol, 8)
        sumcol = 0

    temp = []  # Each inner matrix is a column and the numbers inside each matrix are the rows with 1s in that column
    for i in range(len(adjMat[0])):
        temp.append([])
    k = 0  # Variable for traversing columns
    while k < len(adjMat[0]):  # I scroll through columns
        nrandom = rdm.uniform(0, 1)  # The uniform number is generated for comparisons
        colacum = adjMat[0][k]  # When you start comparing the cumulative number is the first item in the column
        h = 0  # Variable for traversing rows
        while h < len(adjMat):  # Rows of each column are traversed
            if colacum <= nrandom:
                # If the element of the cumulative column of adding is less than the continuous uniform number
                colacum += adjMat[h + 1][k]  # The item in the following row is added for the following comparison
                h += 1  # Next row
                continue  # Returns to the start of the while loop for the next row
            if (colacum > nrandom) and (h not in temp[k]):
                # If the accumulated element is greater than the uniform and that row is not yet in temp[column]
                temp[k].append(h)  # Added row to temp[column]
                if len(temp[k]) == maxInput:  # If you already have nmaxbins rows in temp[column]
                    k += 1  # Next column
                    break  # Goes to the start of the large while loop for the next column
                if len(temp[k]) < maxInput:  # If you don't already have nmaxbins rows in temp[column]
                    break  # Goes to the beginning of the large while loop for the same column, but with another uniform number
            if (colacum > nrandom) and (h in temp[k]):
                break

    # Once the temp list is calculated, the adjMat is already expressed with 1s in the elements collected in temp and the rest 0s
    for i in range(len(adjMat)):  # Rows are traversed
        for j in range(len(adjMat[i])):  # Columns of each row are traversed
            adjMat[j][i] = 0  # First the whole matrix is set to 0

    for i in range(len(temp)):  # Columns are traversed
        for j in temp[i]:  # Rows of each column are traversed
            adjMat[j][i] = 1

    return adjMat
