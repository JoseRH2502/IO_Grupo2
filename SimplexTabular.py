#Metodo principal donde se ejecuta el simplex
def simplexTabular(requerimientos):
    nRestricciones = requerimientos[0][-1]
    nFunObjetivoVal = requerimientos[0][-2]
    return solution(
        llenarMatriz(generarMatriz(nRestricciones + 2, (nFunObjetivoVal + nRestricciones) + 2), requerimientos[1:]),requerimientos[1])

# aqui se genera la matriz con el tamaño que se requiera
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

#En estas dos funciones que continuan se pretende llenar la matriz con las restricciones y la funcion objetivo
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


#Esta funcion valida el caso especial de rompimiento de empates
def rompimientoEmpate(funObj):
    for i in range(len(funObj)):
        for j in range(len(funObj)):
            if (funObj[i] == funObj[j] and j > i):
                return True
    return False

# Esta funcion valida el caso especial de una solucion degenerada
def degenerada(col, matriz):
    degenerada = []
    for i in range(2, len(matriz)):
        #Aqui se controlan las diviciones entre 0
        try:
            if (matriz[i][-1] / matriz[i][col] >= 0):
                degenerada.append(round(matriz[i][-1] / matriz[i][col], 3))
        except ZeroDivisionError:
            print('Divicion entre cero')
    for j in range(len(degenerada)):
        for k in range(len(degenerada)):
            if(degenerada[j] == degenerada[k] and k > j):

                return True
    return False

#Esta funcion valida el caso especial de que el problema sea no Acotado
def noAcotada(col, matriz):
    for i in range(2, len(matriz)):
        try: #Aqui se controlan las diviciones entre 0
            if (matriz[i][-1] / matriz[i][col] >= 0):
                return False
        except ZeroDivisionError:
            print('Divicion entre cero')
    return True

# funcion para validar si hay mas de una solucion
def multiSolucion(matriz):
    numVar =   (len(matriz[0])-2 ) - (len(matriz)-2) # aqui se calcula el numero de variables
    x = "x"
    for i in range(numVar):
        temporal = True
        for j in range(2, len(matriz)):
            if(x+str(i+1) == matriz[j][0]):   # Se busca que la variable real no se encuentre en las variables basicas
                temporal = False
        if (temporal):
            if (matriz[1][i+1]) == 0:    # se busaca que la misma varible este en 0 en la funcion objetivo
                print('Este Problema tiene soluciones multiples')
                salida = 'Este Problema tiene soluciones multiples'
                return salida
    return ""


#Esta es la funcion principal donde se ejecuta todas las operaciones con la matriz
def solution(matriz,funcionObjetivo):
    filapivote = 0
    columnapivote = 0
    numpivote = 0
    entrante = ''
    saliente = ''
    estado = 1
    registro = str(imprimeMatriz(matriz)) + str("\n")
    contador = 0
    esdegenerada = ''
    mostrarProblema(matriz)
    print("\n")
    # En este ciclo vamos a relaizar todas las iteraciones de nuestro simplex
    while (esSolucion(matriz)):

        columnapivote = columnaPivote(matriz)   # se calcula la columna pivot
        if(degenerada(columnapivote, matriz)): # se valida si es degenerada
            esdegenerada = "\n" + "Es una solucion degenerada"
        if(noAcotada(columnapivote, matriz)):    # se valida no esta acotada y termina el simples
            registro += "\n" + " Es un caso no acotado"
            print("Problema no acotado Favor revisar el archivo de salida")
            break
        filapivote = filaPivote(columnapivote, matriz)    # calcula la fila pivot
        numpivote = matriz[filapivote][columnapivote]     # se calcula el numero pivot
        entrante = matriz[0][columnapivote]       # se saca la variable que entra
        saliente = matriz[filapivote][0]     # se saca la variable que sale
        matriz = operacion(matriz, columnapivote, filapivote, numpivote, entrante)   # se reliazan las operaciones en la matriz
        # se comienza a construir la salida
        registro += 'VB entrante: ' + str(entrante) + "\t"+', ' + 'VB saliente: ' + str(
            saliente) +  ", "+'Número Pivot: ' + str(round(numpivote, 4)) + "\n"
        registro += 'Estado: ' + str(estado) + "\n"
        registro += 'Respuesta Parcial: U = ' + str(matriz[1][-1]) + ', ' + solucionObjetivo(matriz)
        registro += "\n"
        registro += imprimeMatriz(matriz)
        registro += "\n"
        contador += 1
        if (not esSolucion(matriz)): # se valida que sea la solucion final para imprimir en consola la ultima tabla
            print('VB entrante: ' + str(entrante) + "\t" + 'VB saliente: ' + str(
            ) + "\t" + 'Número Pivot: ' + str(numpivote) )
            print('Respuesta Parcial: U ' + str(matriz[1][-1]) + ', ' + solucionObjetivo(matriz))
            print('Estado: ' +"Final")
            print(imprimeMatriz(matriz))
            print(esdegenerada)
    if(rompimientoEmpate(funcionObjetivo)):  # valida si es rompe empate
        registro += "\n" + "Rompimiento de empates"
    salida = multiSolucion(matriz)   # antes se terminar valida si tiene multiples soluciones
    return registro + esdegenerada + salida

#Este metodo valida si queda alguna iteracion mas
def esSolucion(matriz):
    for i in range(1, len(matriz)):
        if (matriz[1][i] < 0):
            return True
    return False

# Esta funcion busca la fila con la que vamos a operar
def filaPivote(col, matriz):
    filaPivote = 2
    for i in range(2, len(matriz)):
        try: # controla la diviion entre 0
            if (matriz[i][-1] / matriz[i][col] >= 0 and matriz[i][-1] / matriz[i][col] < matriz[filaPivote][-1] /
                    matriz[filaPivote][col]):  # se busca la fila optima para pivot
                filaPivote = i
        except ZeroDivisionError:
            if (filaPivote == 2 and i == 2):
                filaPivote = 3
            print('Divicion entre cero')
    return filaPivote

#Esta funcion busca la columna con la que vamos a operar
def columnaPivote(matriz):
    columnaPivote = 1
    for i in range(1, len(matriz[1])):
        if (matriz[1][i] <= matriz[1][columnaPivote]):
            columnaPivote = i

    return columnaPivote

#Esta funcion realiza las operacion con la fila y columna pivote y el numero pivote
def operacion(matriz, columnapivote, filapivote, numpivote, entrante):
    for i in range(1, len(matriz[filapivote])):    # se realiza la operacion inicial en la fila pivot con el numero pivot
        matriz[filapivote][i] = matriz[filapivote][i] / numpivote

    for j in range(1, len(matriz)):   # se reliazan todas las operaciones con el resto de la matriz
        contador = 0
        numSim = 0
        for k in range(1, len(matriz[j])):
            if (contador == 0):
                numSim = (matriz[j][columnapivote] * -1)
            if (j != filapivote):
                matriz[j][k] = matriz[j][k] + (numSim * matriz[filapivote][k])
            contador += 1

    matriz[filapivote][0] = entrante
    return matriz

#esta funcion realiza la salida donde estan las soluciones
def solucionObjetivo(matriz):
    x = "x"
    salida = '( '
    for i in range(1, len(matriz[0]) - 1):
        temporal = False
        resultado = 0
        for j in range(2, len(matriz)):
            if (matriz[j][0] == x + str(i)):
                temporal = True
                resultado = matriz[j][-1]
        if (temporal):
            if (i == len(matriz[0]) - 2):
                salida += str(round(resultado, 4))
            else:
                salida += str(round(resultado, 4)) + ", "
        else:
            if (i == len(matriz[0]) - 2):
                salida += "0"
            else:
                salida += "0" + ", "
    salida += " )"
    return salida

#Aqui se forma la matriz en string para poder imprimir la salida
def imprimeMatriz(lista):
    tabla = ""
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            if (isinstance(lista[i][j], str)):
                tabla += lista[i][j] +"\t\t"
            else:
                tabla += str(round(lista[i][j], 4)) + "\t\t"
        tabla += "\n"
    return tabla

def mostrarProblema(matriz):
    for i in matriz:
        print(i)