import sys
from Lector import *
from SimplexTabular import *


def main():

    archivo = sys.argv[1] # recibe archivo al ejecutar en terminal " python3 Simplex.py -h **.txt " 
    problema = leerTxt("Problemas/" + archivo)

    if (problema[0][0] == 1):# valida si el problema requiere ser resuelto por el metodo simplexTabular
      simplexTabular(problema)
    
    elif(problema[0][0] == 2):# valida si el problema requiere ser resuelto por el metodo simplexDosFases
        print("metodo dos fases aun no esta implementado")
    
   
main()

