from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def crear_pdf_con_imagenes(imagenes, ruta_salida):
    """
    Crea un PDF con cada imagen en una página separada.

    :param imagenes: Lista de rutas a imágenes PNG.
    :param ruta_salida: Ruta completa del PDF de salida.
    """
    c = canvas.Canvas(ruta_salida, pagesize=A4)
    ancho, alto = A4  # Dimensiones de la página

    for img in imagenes:
        # Dibujar la imagen ocupando toda la página
        c.drawImage(img, 0, 0, width=ancho, height=alto)
        c.showPage()  # Nueva página para la siguiente imagen

    c.save()
    print(f"PDF creado exitosamente: {ruta_salida}")

def mainExportarPDF():
    # Lista de imágenes
    imagenes = [
        os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'imagenes', 'lineaTemporal.png'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'imagenes', 'mapa_calor.png'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'imagenes', 'mapa_calorGeopsy.png'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'imagenes', 'nubePalabras.png')
    ]

    # PDF de salida
    pdf_file = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'requerimiento5.pdf')

    # Llamada a la función
    crear_pdf_con_imagenes(imagenes, pdf_file)

if __name__ == "__main__":
    mainExportarPDF()

