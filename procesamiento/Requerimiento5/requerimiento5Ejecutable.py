from procesamiento.Requerimiento5.lineaTemporal import mainLineaTemporal
from procesamiento.Requerimiento5.mapaCalorGeopsy import mainCalorGeopsy
from procesamiento.Requerimiento5.mapaCalorNormal import mainCalorNormal
from procesamiento.Requerimiento5.nubePalabras import mainNubePalabras
from procesamiento.Requerimiento5.exportarPDF import mainExportarPDF

def mainRequerimiento5():
    mainLineaTemporal()
    mainCalorNormal()
    mainCalorGeopsy()
    mainNubePalabras()
    mainExportarPDF()

if __name__ == "__main__":
    mainRequerimiento5()

