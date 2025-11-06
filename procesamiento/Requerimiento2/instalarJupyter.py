import subprocess
import sys
import time
import webbrowser

def instalar_jupyter():
    """Instala Jupyter Notebook si no está instalado."""
    print("=" * 60)
    print("📦 VERIFICANDO/INSTALANDO JUPYTER NOTEBOOK")
    print("=" * 60)

    try:
        # Intentar importar para ver si ya está instalado
        import notebook
        print("✅ Jupyter Notebook ya está instalado.\n")
    except ImportError:
        print("⚙️ Instalando Jupyter Notebook...\n")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-U", "notebook"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Instalación completada correctamente.\n")
        except Exception as e:
            print("❌ Error al instalar Jupyter Notebook:")
            print(e)
            sys.exit(1)


def ejecutar_jupyter():
    """Ejecuta Jupyter Notebook y abre el navegador."""
    print("=" * 60)
    print("🚀 INICIANDO JUPYTER NOTEBOOK")
    print("=" * 60)

    try:
        subprocess.Popen(
            [sys.executable, "-m", "notebook"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Esperar unos segundos para que el servidor inicie
        time.sleep(3)
        webbrowser.open("http://localhost:8888/tree")

        print("✅ Jupyter Notebook iniciado correctamente.")
        print("🌐 Abre tu navegador en: http://localhost:8888/tree\n")

    except Exception as e:
        print("❌ Error al ejecutar Jupyter Notebook:")
        print(e)

def mainJupyter():
    instalar_jupyter()
    ejecutar_jupyter()

if __name__ == "__main__":
    mainJupyter()
