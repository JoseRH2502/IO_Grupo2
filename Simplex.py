import sys
from Lector import *
from SimplexTabular import *
from SimplexDosFases import*
from Escritor import *


def main():

    archivo = sys.argv[1] # recibe archivo al ejecutar en terminal " python3 Simplex.py -h **.txt " 
    nArgumentos = len(sys.argv) - 1 
    if nArgumentos == 1:
        if (archivo != "-h"):
            problema = leerTxt("Problemas/" + archivo)
            if (problema[0][0] == 1):# valida si el problema requiere ser resuelto por el metodo simplexTabular
                simplexTabular(problema)
            elif(problema[0][0] == 2):# valida si el problema requiere ser resuelto por el metodo simplexDosFases
                escribir("Solución",  dosFases(problema))
        else:
            print("Modo ayuda ")
            print("La intrucción de ejecución debe tener la siguinte estructura: \n")
            print("python Simplex.py nombreArchivo.txt \n")
            print("Donde: \n")
            print("python Simplex.py: Esta es la instrucción que ejecuta el programa")
            print("nombreArchivo: Es el nombre del archivo txt del problema que desea resolver\n")
            print("Nota: Es el importante que el archivo txt se almacene en la carpeta Problemas")
       
    if nArgumentos == 2:
        if ( archivo[0]+archivo[1] != "-h"):
            print("La intrucción de ejecución debe tener la siguiente estructura: \n")
            print("python Simplex.py nombreArchivo.txt \n")
        else:
            print("Modo ayuda ")
            print("La intrucción de ejecución debe tener la siguinte estructura: \n")
            print("python Simplex.py nombreArchivo.txt \n")
            print("Donde: \n")
            print("python Simplex.py: Esta es la instrucción que ejecuta el programa")
            print("nombreArchivo: Es el nombre del archivo txt del problema que desea resolver\n")
            print("Nota: Es el importante que el archivo txt se almacene en la carpeta Problemas")
        
        
   

     
   
main()

