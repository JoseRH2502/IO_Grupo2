import sys
def esNegativo(elemento):
    temp = elemento.split('-')
    if(len(temp) == 2):
        return True
    return False

def limpiarTexto(list):
    temp = list[-1].split('\n')
    list[-1] = temp[0]
    for i in range(len(list)):

        if(isinstance(list[i], str) and "." in list[i]):
            list[i] = float(list[i])
        elif (list[i].isdigit() or esNegativo(list[i])):
            list[i] = int(list[i])
    return list

def leerTxt(directorio):
    if(isinstance(directorio, str)):
        lineas = open(directorio,"r")
        problema = []
        for linea in lineas:
            problema.append(limpiarTexto(linea.split(',')))
        return problema

    else:
        print("La ruta no es correcta")
        

def generarMatriz(nFilas, nColumnas):
    matriz = []
    for i in range(nFilas):
        fila = []
        for j in range(nColumnas):
            if (i == 0):
                if (j == 0):
                    fila.append("VB")
                elif (j == nColumnas - 1):
                    fila.append("LD")
                else:
                    fila.append("x" + str(j))
            elif (i == 1 and j == 0):
                fila.append("U")
            elif (i > 0 and j == 0):
                fila.append("x" + str(((nColumnas - 2) - (nFilas - 1) + i)))
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

def llenarMatriz(matriz, restricciones):
    for i in range(len(restricciones)):
        matriz = llenarMatrizAux(i, matriz, restricciones[i], restricciones)
    return matriz

def llenarMatrizAux(pos, matriz, restriccion, restriccion2):
    for j in range(1, len(matriz[pos + 1])):

        if (pos + 1 == 1):
            if (j - 1 > len(restriccion) - 1):
                matriz[pos + 1][j] = 0
            else:
                matriz[pos + 1][j] = restriccion[j - 1] * -1
        else:
            if (len(matriz[pos + 1]) - 1 == j):
                matriz[pos + 1][j] = restriccion[-1]
            elif (len(restriccion2[0]) + pos == j):
                matriz[pos + 1][j] = 1
            elif (j - 1 < len(restriccion) - 1):
                if (type(restriccion[j - 1]) == int):
                    matriz[pos + 1][j] = restriccion[j - 1]
            else:
                matriz[pos + 1][j] = 0

    return matriz

def mostrarMatriz(matriz):
    for i in matriz:
        for j in i:
            print(j)

def mostrarProblema(matriz):
    for i in matriz:
        print(i)


def esColumnaPivote(matriz):
    columnaPivote = 1
    for i in range(1, len(matriz[1])):
        if (matriz[1][i] <= matriz[1][columnaPivote]):
            columnaPivote = i

    return columnaPivote

def noAcotada(col, matriz):
    for i in range(2, len(matriz)):
        try:
            if (matriz[i][-1] / matriz[i][col] >= 0):
                return False
        except ZeroDivisionError:
            print('Division entre cero')
    return True

def main():
    columnaPivote = 0
    archivo = sys.argv[2] # al ejecutar en terminal " python3 Simplex.py -h Problema1.txt " 
    problema = leerTxt(archivo)
    matriz = generarMatriz(problema[0][2], problema[0][3])
    numRestrictions =  problema[0][-1]
    numFunObjetiveVal =  problema[0][-2]
    full = llenarMatriz( generarMatriz(numRestrictions + 2, (numFunObjetiveVal + numRestrictions) + 2), problema[1:]) 
    print("Matriz generada:")
    mostrarProblema(full)
    print(" ")

    columnaPivote = esColumnaPivote(matriz)   # se calcula la columna pivote
    if(noAcotada(columnaPivote, matriz)):    # se valida no esta acotada y termina el simplex
            print("Problema no acotado, favor revisar el archivo de salida")

 
    

main()
