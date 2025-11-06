import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def crear_pdf_con_imagenes(imagenes, ruta_salida):
    """
    Crea un PDF con cada imagen en una página separada y lo abre automáticamente.

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
    print(f"✅ PDF creado exitosamente: {ruta_salida}")

    # 🔹 Abrir el PDF automáticamente (solo en Windows)
    try:
        os.startfile(ruta_salida)
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")

def mainExportarPDF():
    # Lista de imágenes
    imagenes = [
        r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\lineaTemporal.png",
        r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\mapa_calor.png",
        r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\mapa_calorGeopsy.png",
        r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\imagenes\nubePalabras.png"
    ]

    # PDF de salida
    pdf_file = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\output\requerimiento5.pdf"

    # Llamada a la función
    crear_pdf_con_imagenes(imagenes, pdf_file)

if __name__ == "__main__":
    mainExportarPDF()

