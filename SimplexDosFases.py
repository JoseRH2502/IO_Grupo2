import math
"""
Definición de las Varibles globales que se utilizaran desde las funciones
"""
datos = []                 # Datos originales del txt
max_min = 0                # 0 = Maximización / 1 = Minimización
realVariables = []         # Número de Variables Reales
holguraVariable = []       # Número de Variables de Holgura
artificialVariables = []   # Número de Variables Artificales
ordenRestriccion  = []     # Orden del simbolo de restricciones
matrix = []                # Donde se guardará la matriz a trabajar
respuesta = ""             # Respuesta a imprimir y escribir
pivote = 0                 # pivotee para calculos de Etapas/Iteraciones
elegidoCol = 0             # Columna seleccionada para Etapa/Iteración
elegidoRow = 0             # Fila seleccionada para Etapa/Iteración
mismoLD = -1               # Variable auxiliar para detectar Degeneradas
degenerada = False         # Variable de degenerada
noAcotada = False          # Variable de No Acotada
noFactible = False         # Variable de No Factible
solMultiple = False        # Variable de Soluciones Multiples

def cargarDatos():
        """
        Descripción:Esta función utiliza los valores del txt que se encuentra en  datos y actuliza todo los valores de la clase. 
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """   
        global datos           
        global max_min              
        global realVariables         
        global holguraVariable        
        global artificialVariables    
        global ordenRestriccion        
       
        # Se revisa si la operación es Max o Min
        if datos[1] == "max":
            max_min = 1
            
        # Se actualiza la cantidad de variables reales
        aux = 1
        while aux <= datos[2]:
            realVariables.append(aux)
            aux+=1
        # Dependiendo de los simbolos, se suma cada tipo de restriccióna la variable correspondiente
        for variables in datos:
            if variables == "<=":
                ordenRestriccion .append("<=")
                holguraVariable.append(aux)

                aux += 1

            elif variables == "=":
                ordenRestriccion .append("=")
                artificialVariables.append(aux)
                aux += 1
                
            elif variables == ">=":
                ordenRestriccion .append(">=")
                holguraVariable.append(aux)
                aux += 1
                artificialVariables.append(aux)
                aux += 1

def matrizInicialFase1():
        """
        Descripción:Este función se encarga de preparar la tabla inicial de Fase 1. 
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """ 
        global datos           
        global realVariables          
        global holguraVariable         
        global artificialVariables    
        global ordenRestriccion        
        global matrix 
        global respuesta               
        
        colNumber = 1 + len(realVariables) + len(holguraVariable) + len(artificialVariables) + 1         # colNumber - Cantidad de columnas a realizar en la matriz
        rowNumber = 2 + datos[3]            # rowNumber - Cantidad de filas a realizar en la matriz

        indexReal = 0   # indexReal - Indice que indica la variable real que se trabaja
        indexHolgura = 0          # indexHolgura - Indice que indica la variable de holgura que se trabaja
        indexArtifitial = 0         # indexArtifitial - Indice que indica la variable artificial que se trabaja

        indexHolguraTable = 0   # indexHolguraTable - Indice para colocar el Xn en el VB
        indexArtifitialTable = 0         # indexArtifitialTable - Indice para colocar el X'n en el VB

        # Se generan las filas dentro de la matriz
        for i in range(rowNumber):
            tempRow = []
            matrix.append(tempRow)

        aux = 3 + len(realVariables) + 1 #index de los datos + cantidad de variables reales + 1 para empezar en el primero de restriccion (1)
        row = 0

        # Por cada fila dentro de la matriz, se va rellenando cada columna (exceptuando U) con los datos correspondientes
        for fila in matrix:
            col = 0
            for columna in range(colNumber):

                # Si la fila es 0, es la fila de las variables, por lo que se colocan sus nombres
                if row == 0:
                    if col == 0:
                        fila.append("VB")

                    elif col == colNumber-1:
                        fila.append("LD")
                    
                    else:
                        if indexReal < len(realVariables) and realVariables[indexReal] == col:
                            fila.append("X"+str(indexReal+indexHolgura+indexArtifitial+1))
                            indexReal += 1

                        elif indexHolgura < len(holguraVariable) and holguraVariable[indexHolgura] == col:
                            fila.append("X"+str(indexReal+indexHolgura+indexArtifitial+1))
                            indexHolgura += 1
                        
                        else:
                            fila.append("X'"+str(indexReal+indexHolgura+indexArtifitial+1))
                            indexArtifitial += 1
                else:
                    # Si la fila no es 0, se intenta ingresar cada uno de sus valores
                    if col == 0:
                        if row == 1:
                            fila.append("U")
                        else:
                            # Si la restricción posee un <= entonces se ingresa una variable de holgura
                            if ordenRestriccion [row-2] == "<=":
                                fila.append("X"+str(holguraVariable[indexHolgura]))
                                indexHolgura += 1

                            # Si la restricción posee un = entonces se ingresa una variable artificial
                            elif ordenRestriccion [row-2] == "=":
                                fila.append("X'"+str(artificialVariables[indexArtifitial]))
                                indexArtifitial += 1
                            
                            # Si la restricción posee un = entonces se ingresa una variable artificial
                            else:
                                fila.append("X'"+str(artificialVariables[indexArtifitial]))
                                indexArtifitial += 1
                                indexHolgura += 1
                    else:
                        # Cuando la columna no es 0 y la fila es mayor a 1, se empieza a llenar los valores
                        if row != 1:
                            # Si es dato es de la columna VB o LP entonces inserta el dato directamente
                            if col <= len(realVariables):
                                fila.append(datos[aux])
                                aux += 1
                            
                            elif col == colNumber-1:
                                fila.append(datos[aux])
                                aux += 1

                            else:
                                # Si es una variable se inserta dentro de la matriz dependiendo del simbolo que pertenezca
                                if datos[aux] == "<=":
                                    if indexHolguraTable < len(holguraVariable) and col == holguraVariable[indexHolguraTable]:
                                        fila.append(1)
                                        indexHolguraTable += 1
                                        aux += 1

                                    else:
                                        fila.append(0)

                                elif datos[aux] == "=":
                                    if indexArtifitialTable < len(artificialVariables) and col == artificialVariables[indexArtifitialTable]:
                                        fila.append(1)
                                        indexArtifitialTable += 1
                                        aux += 1

                                    else:
                                        fila.append(0)

                                elif datos[aux] == ">=":
                                    if indexHolguraTable < len(holguraVariable) and col == holguraVariable[indexHolguraTable]:
                                        fila.append(-1)
                                        indexHolguraTable += 1
                                    
                                    elif indexArtifitialTable < len(artificialVariables) and col == artificialVariables[indexArtifitialTable]:
                                        fila.append(1)
                                        indexArtifitialTable += 1
                                        aux += 1

                                    else:
                                        fila.append(0)

                                else:
                                    fila.append(0)
                        else:
                            if col in artificialVariables:
                                fila.append(1)

                            else:
                                fila.append(0)

                col += 1
            if row == 0:
                indexReal = 0
                indexHolgura = 0
                indexArtifitial = 0
            row += 1

        # Se transforma la linea de 1 en su forma Fase 1 
        for i in range(colNumber):
            if i != 0:
                temp = matrix[1][i]
                aux = 0

                for j in ordenRestriccion :
                    if j != "<=":
                        temp += -1*matrix[aux+2][i]

                    aux += 1
                
                
                matrix [1][i] = temp

        # Matriz se pasa a self y se coloca la respuesta correspondiente
        respuesta += "Fase 1\nEstado 0:\n"

        for i in matrix:
            for j in i:
                auxValue = ""
                if type(j) == str:
                    respuesta += str(j)
                    auxValue = str(j)
                else:
                    respuesta += str(round(j, 4))
                    auxValue = str(round(j, 4))
                if len(auxValue) > 3:
                    respuesta += "\t"
                else:
                    respuesta += "\t\t"
            respuesta += "\n"
        respuesta += "\n"
        obtenerSolucion()

        # Si la matriz no está lista, se selecciona un pivotee
        if not obtenerEstadoFase1():
            obtenerPivote()

def obtenerEstadoFase1():

        """
        Descripción:Esta función se encarga de ver si Fase 1 ha terminado o no. 
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global matrix    
         
        negativa = False      # negativa - Variable auxiliar para forzar una no Factible
        colLen = len(matrix[1])     # colLen - Largo de las columnas

        # Se revisa si es un problema no Factible
        for i in range(colLen):
            # Si el LP es diferente a 0 al terminar la Fase 1, fuerza el estado a terminado
            # luego se trata marca la no Factibilidad más adelante
            if i == colLen-1 and not negativa and round(matrix[1][i], 4) != 0:
                return True
            
            # Se revisa si alguna de las variables es negativa, o sea, no se ha terminado Fase 1
            if i > 0 and i < colLen-1:
                if round(matrix[1][i], 4) < 0:
                    negativa = True
        
        for i in artificialVariables:
            if abs(math.ceil(matrix[1][i])) != 1 and abs(1-matrix[1][i]) > 0.0000001: #Si en el renglon 0 (U) no todas las artificiales son 1, aún no se termina Fase 1
                return False
        
        return True            

def obtenerSolucion():
        """
        Descripción:Esta función se encarga de devolver la solución de la Tabla actual en el respuesta
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global max_min              
        global matrix                
        global respuesta              
        global degenerada         

        colLen = len(matrix[0])  # colLen - Largo de las columnas de la matriz
        rowLen = len(matrix)      # rowLen - Largo de las filas de la matriz
        uValue = matrix[1][colLen-1]        # uValue - Varlor de LP de renglon 0 (U)

        if uValue < 0 or not max_min:
            uValue = uValue*-1

        respuesta += "Respuesta de la Tabla Anterior: U = "+str(round(uValue, 4))+", ("

        # Se saca el valor de cada variable respecto a la tabla
        for i in range(colLen):
            if i > 0 and i < colLen-1:
                value = 0
                for j in range(rowLen):
                    if matrix[0][i] == matrix[j][0]:
                        value = matrix[j][colLen-1]
                
                respuesta += matrix[0][i]+" = "+str(round(value, 4))
                if i < colLen-2:
                    respuesta += ", "
                else:
                    respuesta += ")\n"
        
        # Si degenerada está activada, indica que la función es degenerada
        if degenerada:
            respuesta += "La solución es degenerada, existen restricciones redundantes\n"

def obtenerPivote():
        """
        Descripción:Esta función se encarga de escoger el pivotee para la siguiente iteración
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global realVariables        
        global holguraVariable        
        global matrix               
        global respuesta           
        global pivote          
        global elegidoCol          
        global elegidoRow           
        global mismoLD               
        global degenerada         
        global noAcotada         

        noListaDegenerada = False   # noListaDegenerada - variable auxiliar para saber si la etapa anterior y la actual pueden ser una degenerada
        elegidoCol = round(matrix[2][1], 4)      # elegidoCol - variable para comparar el valor menor de las columnas
        aux = 1        # aux - Variable auxiliar para saber cual columna se escoge

        # Si mismoLD ya está activo, entonces la fase anterior pudo ser degenerada, se prende noListaDegenerada
        if mismoLD != -1:
            noListaDegenerada = True

        # realSlackVariable - Lista de variables reales y de holgura
        realSlackVariable = realVariables + holguraVariable
        
        # Se busca la columna a seleccionar, si es menor que la actual se selecciona
        for i in realSlackVariable:
            if round(matrix[1][i], 4) < round(elegidoCol, 4):
                elegidoCol = matrix[1][i]
                aux = i
        elegidoCol = aux

        # Se busca la fila a seleccionar
        elegidoRow = -1 # Se inicia en -1 para que cualquier primer caso valido lo reemplace
        aux = 2
        rowLen = len(matrix)
        colLen = len(matrix[0])

        # Se recorre cada fila y se busca cuál division de LD con la columna seleccionada es menor sin ser n/0 o < 0

        # firstTime - Variable para saber si el valor obtenido valido pasa de una o no
        firstTime = True
        for i in range(rowLen):
            if i != 0 and i != 1:
                if matrix[i][elegidoCol] != 0:
                    division = matrix[i][colLen-1] / matrix[i][elegidoCol]
                    # Si ya se detectó una posible degenerada y su nuevo resultado LP da 0, entonces se marca como degenerada
                    if mismoLD == i and matrix[i][colLen-1] == 0:
                        degenerada = True

                    # Si se encuentra otra LP que dividida da lo mismo, se marca para revisar si es degenerada
                    if elegidoRow == division:
                        mismoLD = i

                    # Si la respuesta de la division es válida y es menor a la actual o es la primera evaluada, se selecciona 
                    if (division < elegidoRow or firstTime) and (division >= 0 and matrix[i][elegidoCol] > 0):
                       firstTime = False
                       elegidoRow = division
                       aux = i
        
        # Se desactiva el mismoLD despues de evaluar si esta fase y la anterior son degeneradas
        if noListaDegenerada == True:
            mismoLD = -1

        # Si ninguna fila es válida para escogerse es una No Acotada
        if elegidoRow == -1:
            noAcotada = True
            respuesta += "La solución no está acotada. La variable "+matrix[0][elegidoCol]+" puede entrar pero ninguna puede salir\n"

        else:
            # Si se escogió una columna, se pasa al self al igual que el pivotee y se actualiza la respuesta
            elegidoRow = aux

            pivote = matrix[elegidoRow][elegidoCol]

            respuesta += "VB entrante: " + str(matrix[0][elegidoCol])+\
                        ", VB saliente: " + str(matrix[elegidoRow][0])+\
                        ", Número pivote: " + str(round(pivote, 4))+ "\n"

            matrix[elegidoRow][0] = matrix[0][elegidoCol]

def simplexFase1():
        """
        Descripción:Esta función se encarga de hacer la Fase 1 de las 2 Fases
        Entrandas:
        Salida: N/A
        Restricciones: N/A
        """
        global matrix             
        global respuesta           
        global pivote             
        global elegidoCol            
        global elegidoRow          
        global noAcotada          
        global noFactible         
    
        estado = 1   # estado - Iteración actual del 2 Fases: Fase 1
        colNumber = len(matrix[0])   # colNumber - Largo de las columnas de la matriz
        rowNumber = len(matrix)   # rowNumber - Largo de las filas de la matriz

        # Mientras que no se haya terminado y el problema no sea no Acotada o no Factible, sigue iterando
        while not obtenerEstadoFase1() and not noAcotada and not noFactible:

            #Se crea la nueva fila seleccionada
            for i in range(colNumber):
                if i != 0:
                    matrix[elegidoRow][i] = matrix[elegidoRow][i] / pivote

            #Se crean las nuevas filas en base a la nueva fila pivotee
            for i in range(rowNumber):
                if i != 0 and i != elegidoRow:
                    colpivote = matrix[i][elegidoCol]
                    for j in range(colNumber):
                        if j != 0:
                            matrix[i][j] = matrix[i][j] - colpivote * matrix[elegidoRow][j]

                  
            #Se agrega la nueva tabla a la respuesta
            respuesta += "\nEstado "+str(estado)+"\n"

            for i in matrix:
                for j in i:
                    auxValue = ""
                    if type(j) == str:
                        respuesta += str(j)
                        auxValue = str(j)
                    else:
                        respuesta += str(round(j, 4))
                        auxValue = str(round(j, 4))
                    if len(auxValue) > 3:
                        respuesta += "\t"
                    else:
                        respuesta += "\t\t"
                respuesta += "\n"

            respuesta += "\n"
            obtenerSolucion()

            # Si no se ha terminado Fase 1, se escoge un pivotee
            if not obtenerEstadoFase1():
                obtenerPivote()

            estado += 1
       
       # Si el LP del renglón 0 (U) no es 0, entonces es no Factible
        if round(matrix[1][colNumber-1], 4) != 0:
            noFactible = True
            respuesta += "El problema es infactible ya que el valor de la función objetivo es distinta a 0 al terminar Fase 1\n"

        # Si el problema no es no Acotada ni no Factible, entonces sigue con Fase 2
        if not noAcotada and not noFactible:
            respuesta += "Final de la Fase 1\n\nFase 2"
     
def matrizInicialFase2():
        """
        Descripción:Esta función se encarga de inicializar la tabla de la fase 2
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global holguraVariable        
        global artificialVariables
        global matrix               
        global respuesta             
        global pivote                
        
        # rowLen - Largo de las filas de la matriz
        rowLen = len(matrix)

        # Se ordena la lista de artificales de mayor a menor
        artificialVariables.sort(reverse=True)

        # Se eliminan las variables artificiales
        for i in range(rowLen):
            for j in artificialVariables:
                del matrix[i][j]

        # Se ajustan variables de holgura en holguraVariable
        holguraVariable.clear()

        for i in range(len(matrix[1])):
            if i > 0 and i < len(matrix[1])-1:
                if i not in realVariables:
                    holguraVariable.append(i)

        aux = 4 # aux indice para señalar los valores reales, el valor 4 porque es la posición dentro de la matriz de datos de X1
        min = 1  # min - variable para definir el valor positivo/negativo del renglón 0 (U) 

        # Si la operación es maximizar entonces se multiplica por -1, sino no
        if max_min == 1:
            min = -1

        for i in range(len(matrix[1])-1):
            if i+1 in realVariables:
                matrix[1][i+1] = min*datos[aux]
            
            else:
                matrix[1][i+1] = 0
            aux += 1

        colLen = len(matrix[0])
        #Se restablece la forma apropiada de U (Elim. Gaussiana)
        for rv in realVariables:
            choosenRow = -1
            for i in range(rowLen):
                if i >= 2 and matrix[i][rv] == 1:
                    choosenRow = i
            
            pivote = matrix[1][rv]
            if choosenRow != -1:
                for i in range(colLen):
                    if i != 0:
                        matrix[1][i] = matrix[1][i] - pivote * matrix[choosenRow][i]

        respuesta += "\nEstado 0\n"

        for i in matrix:
            for j in i:
                auxValue = ""
                if type(j) == str:
                    respuesta += str(j)
                    auxValue = str(j)
                else:
                    respuesta += str(round(j, 4))
                    auxValue = str(round(j, 4))
                if len(auxValue) > 3:
                    respuesta += "\t"
                else:
                    respuesta += "\t\t"
            respuesta += "\n"

        respuesta += "\n"
        obtenerSolucion()

        if not obtenerEstadoFase2():
            obtenerPivote()

def obtenerEstadoFase2():
        """
        Descripción:Esta función se encarga encarga de regresar si ya se terminó Fase 2 o no
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global matrix          
     
        # colLen - Largo de las columnas de la matriz
        colLen = len(matrix[0])

        for i in range(colLen):
            if i > 0 and i < colLen-1:
                if matrix[1][i] < 0:    #Si en el renglon 0 (U) no todas las variables son menores a 0, aún no se termina Fase 2
                    return False
        
        return True                        
      
def simplexFase2():
        """
        Descripción:Este método se encarga de hacer la Fase 2 de las 2 Fases
        Entrandas:
            self = Acceso a los datos generales de la clase
        Salida: N/A
        Restricciones: N/A
        """
   
        global matrix              
        global respuesta           
        global pivote              
        global elegidoCol          
        global elegidoRow          
   
        estado = 1    # estado - Iteración actual del 2 Fases: Fase 2
        colNumber = len(matrix[0])       # colNumber - Largo de las columnas de la matriz
        rowNumber = len(matrix)         # rowNumber - Largo de las filas de la matriz

        # Mientras que no se haya terminado y el problema no sea no Acotada, sigue iterando
        while not obtenerEstadoFase2() and not noAcotada:

            #Se crea la nueva fila seleccionada
            for i in range(colNumber):
                if i != 0:
                    matrix[elegidoRow][i] = matrix[elegidoRow][i] / pivote

            #Se crean las nuevas filas en base a la nueva fila pivotee
            for i in range(rowNumber):
                if i != 0 and i != elegidoRow:
                    colpivote = matrix[i][elegidoCol]
                    for j in range(colNumber):
                        if j != 0:
                            matrix[i][j] = matrix[i][j] - colpivote * matrix[elegidoRow][j]

                  
            #Se agrega la nueva tabla a la respuesta
            respuesta += "\nEstado "+str(estado)+"\n"

            for i in matrix:
                for j in i:
                    auxValue = ""
                    if type(j) == str:
                        respuesta += str(j)
                        auxValue = str(j)
                    else:
                        respuesta += str(round(j, 4))
                        auxValue = str(round(j, 4))
                    if len(auxValue) > 3:
                        respuesta += "\t"
                    else:
                        respuesta += "\t\t"
                respuesta += "\n"
            
            respuesta += "\n"
            obtenerSolucion()

            if not obtenerEstadoFase2():
                obtenerPivote()
            estado += 1

def revisarMultiples():
        """
        Descripción:Esta función se encarga de revisar si existen soluciones múltiples óptimas
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global matrix               
        global respuesta              
        global pivote                
        global elegidoCol            
        global elegidoRow            
        global solMultiple        
       
        colNumber = len(matrix[0])  # colNumber - Largo de las columnas de la matriz
        rowNumber = len(matrix)     # rowNumber - Largo de las filas de la matriz
        colToCheck = -1  # colToCheck - Posible index de la columna a revisar que tiene 0 en ranglon 0 (U)
        localMatrix = matrix         # localMatrix - Copia la matrix global en local de matrix
        localrespuesta = respuesta +"\n\nSe ha detectado una respuesta múltiple óptima\n"  # localrespuesta - Copia local de respuesta

        for i in range(colNumber):
            vnb = True  # vnb - Booleano usado para saber si la variable no está en VB
            if i != 0 and i != colNumber-1:
                for j in range(rowNumber):

                    # Si la variable está en VB se entonces se cambia vnb a False
                    if j != 0 and localMatrix[0][i] == localMatrix[j][0]:
                        vnb = False
                
                # Si la variable no está en VB y es 0, es candidato para iteración extra
                if vnb and abs(round(localMatrix[1][i], 4)) == 0:
                    colToCheck = i
        
        if colToCheck != -1:
            # Se busca la fila a seleccionar
            elegidoCol = colToCheck
            elegidoRow = -1 # Se inicia en -1 para que cualquier primer caso valido lo reemplace
            aux = 2

            # Se recorre cada fila y se busca cuál division de LD con la columna seleccionada es menor sin ser n/0 o < 0

            firstTime = True   # firstTime - Variable para saber si el valor obtenido valido pasa de una o no
            for i in range(rowNumber):
                if i != 0 and i != 1:
                    if localMatrix[i][elegidoCol] != 0:
                        division = localMatrix[i][colNumber-1] / localMatrix[i][elegidoCol]

                        # Si la respuesta de la division es válida y es menor a la actual o es la primera evaluada, se selecciona 
                        if (division < elegidoRow or firstTime) and (division >= 0 and localMatrix[i][elegidoCol] > 0):
                            firstTime = False
                            elegidoRow = division
                            aux = i

            # Si ninguna fila es válida para escogerse es una No Acotada
            if elegidoRow != -1:
                # Si se escogió una fila, se pasa al self al igual que el pivotee y se actualiza la respuesta
                elegidoRow = aux

                pivote = localMatrix[elegidoRow][elegidoCol]

                localrespuesta += "VB entrante: " + str(localMatrix[0][elegidoCol])+\
                            ", VB saliente: " + str(localMatrix[elegidoRow][0])+\
                            ", Número pivote: " + str(round(pivote, 4))+ "\n"

                localMatrix[elegidoRow][0] = localMatrix[0][elegidoCol]


                #Se crea la nueva fila seleccionada
                for i in range(colNumber):
                    if i != 0:
                        localMatrix[elegidoRow][i] = localMatrix[elegidoRow][i] / pivote

                #Se crean las nuevas filas en base a la nueva fila pivotee
                for i in range(rowNumber):
                    if i != 0 and i != elegidoRow:
                        colpivote = localMatrix[i][elegidoCol]
                        for j in range(colNumber):
                            if j != 0:
                                localMatrix[i][j] = localMatrix[i][j] - colpivote * localMatrix[elegidoRow][j]

                    
                #Se agrega la nueva tabla Extra a la respuesta
                localrespuesta += "\nEstado Extra\n"

                for i in localMatrix:
                    for j in i:
                        auxValue = ""
                        if type(j) == str:
                            respuesta += str(j)
                            auxValue = str(j)
                        else:
                            respuesta += str(round(j, 4))
                            auxValue = str(round(j, 4))
                        if len(auxValue) > 3:
                            respuesta += "\t"
                        else:
                            respuesta += "\t\t"
                    respuesta += "\n"
                
                optima = True

                for i in range(colNumber):
                    if i > 0 and i < colNumber-1:
                        if localMatrix[1][i] < 0:         #Si en el renglon 0 (U) no todas las variables son menores a 0, no es óptima
                            optima = False
                
                if optima:
                    solMultiple = True
                    matrix = localMatrix
                    respuesta = localrespuesta
                    respuesta += "\n"
                    obtenerSolucion()
                    respuesta += "\nEste es un ejemplo de otra solución Óptima\n"

def printRespuesta():
        """
        Descripción:Esta función se encarga de imprime la respuesta de la última tabla generada
        Entrandas: N/A
        Salida: N/A
        Restricciones: N/A
        """
        global max_min                
        global matrix           
        localrespuesta = "\nSimplex 2 Fases: Resultado\n"

        for i in matrix:
            for j in i:
                if type(j) == str:
                    localrespuesta += str(j)
                else:
                    localrespuesta += str(round(j, 4))
                localrespuesta += "\t"
            localrespuesta += "\n"
        localrespuesta += "\n"
        # Se calculan las respuestas
        
        colLen = len(matrix[0])   # colLen - Largo de las columnas de la matriz
        rowLen = len(matrix)   # rowLen - Largo de las filas de la matriz
        uValue = matrix[1][colLen-1] # uValue - Varlor de LP de renglon 0 (U)

        if uValue < 0 or not max_min:
            uValue = uValue*-1

        localrespuesta += "Respuesta de la Tabla: U = "+str(round(uValue, 4))+", ("

        # Se saca el valor de cada variable respecto a la tabla
        for i in range(colLen):
            if i > 0 and i < colLen-1:
                value = 0
                for j in range(rowLen):
                    if matrix[0][i] == matrix[j][0]:
                        value = matrix[j][colLen-1]
                
                localrespuesta += matrix[0][i]+" = "+str(round(value, 4))
                if i < colLen-2:
                    localrespuesta += ", "
                else:
                    localrespuesta += ")\n"
        
        return localrespuesta

def dosFases(problema):
        """
        Descripción:Esta es la funcion principal y se encarga de ejecutar el proceso de Simplex 2 Fases
        Entrandas: problema que es los datos orginales recuperados del txt
        Salida: N/A
        Restricciones: N/A
        """
        global datos            
        global respuesta             
        global degenerada         
        global noAcotada          
        global noFactible         
        global solMultiple        

        newMatriz = []
        # Limpia los datos del problema
        for i in  problema:
            for j in i:
                if isinstance(j, str) and "." in j:
                    newMatriz.append(float(j))
                else:
                    newMatriz.append(j)
        
        datos = newMatriz
        
        # Se prepara la data dentro de variables en la clase
        cargarDatos()

        # Siempre y cuando el problema no se no Acotado o no Factible, se sigue ejecutando
        if not noAcotada and not noFactible:
            # Se prepara la primer tabla de Fase 1
            matrizInicialFase1()

        if not noAcotada and not noFactible:
            # Se ejecuta la Fase 1
            simplexFase1()

        if not noAcotada and not noFactible:
            # Se prepara la primer tabla de Fase 2
            matrizInicialFase2()
        
        if not noAcotada and not noFactible:
            # Se ejecuta la Fase 2
            simplexFase2()

        if not noAcotada and not noFactible:
            # Si no es no Acotada ni no Factible, se menciona que es la respuesta óptima
            respuesta += "Respuesta Óptima\n"

        if not noAcotada and not noFactible:
            # Si no es no Acotada ni no Factible, se hace la revisión de tener otra respuesta óptima
            revisarMultiples()

        localrespuesta = printRespuesta()
        
        # Si degenerada está activada, indica que la función es degenerada
        if degenerada:
            localrespuesta += "La solución es degenerada, existen restricciones redundantes\n"

        # Si noAcotada está activada, indica que la función es noAcotada
        if noAcotada:
            localrespuesta += "La solución es no Acotada. Una de las variables puede entrar a VB pero ninguna puede salir\n"

        # Si noFactible está activada, indica que la función es no Factibles
        if noFactible:
            localrespuesta += "El problema es infactible ya que el valor de la función objetivo es distinta a 0 al terminar Fase 1\n"

        # Si solMultiple está activada, indica que la función tiene multiples soluciones óptimas
        if solMultiple:
            localrespuesta += "El problema tiene múltiples soluciones óptimas, esta es un ejemplo\n"

        print(localrespuesta)
