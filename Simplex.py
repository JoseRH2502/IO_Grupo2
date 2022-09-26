import sys
from Lector import *
from SimplexTabular import *
from SimplexDosFases import*
from Escritor import *


def main():

    archivo = sys.argv[1] # recibe archivo al ejecutar en terminal " python3 Simplex.py -h **.txt " 
    #archivo = "p_min_2.txt"
    problema = leerTxt("Problemas/" + archivo)

    if (problema[0][0] == 1):# valida si el problema requiere ser resuelto por el metodo simplexTabular
        simplexTabular(problema)
    
    elif(problema[0][0] == 2):# valida si el problema requiere ser resuelto por el metodo simplexDosFases
        escribir("Solución",  dosFases(problema))

     
   
main()

