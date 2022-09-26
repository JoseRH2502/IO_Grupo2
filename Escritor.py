from os import path

    
def escribir (nombreArchivo, respuesta):
        """
        Descripción: Esta función se encarga de generar un txt con todas las iteraciones del método simplex/dos fases
        Entrandas:
            nombreArchivo: Es el nombre que tendra el archivo generado con las respuestas
            respuesta: Es un string con todas las respuestas del método simplx 
        Salida: N/A
        Restricciones: N/A
        """
        nuevoArchivo = nombreArchivo+".txt"
      
        #revisa si el archivo existe, si existe se agrega un "n" al nombre, donde "n" es un cantidad de achivos con el mismo nombre 
        i = 1
        flag = True
        while(flag):
            if not path.exists(nombreArchivo+".txt"):
                flag = False

            elif not (path.exists(nombreArchivo+"("+str(i)+").txt")):
                flag = False
                nuevoArchivo = nombreArchivo+"("+str(i)+").txt"
            
            else:
                i += 1
        archv = open(nuevoArchivo, "a")
        archv.write(respuesta)
        archv.close()
