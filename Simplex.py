import sys
from Lector import *
from SimplexTabular import *


def main():

    archivo = sys.argv[1] # al ejecutar en terminal " python3 Simplex.py -h **.txt " 
    problema = leerTxt("Problemas/" + archivo)
    simplexTabular(problema)
   
main()

