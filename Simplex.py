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

def mostrarMatrix(matriz):
    for i in matriz:
        print(i)

