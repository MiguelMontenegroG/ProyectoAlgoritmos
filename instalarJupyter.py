import subprocess
import sys
import time
import webbrowser
import os
import shlex

def instalar_jupyter():
    """Instala Jupyter Notebook si no está instalado."""
    print("=" * 60)
    print("📦 VERIFICANDO/INSTALANDO JUPYTER NOTEBOOK")
    print("=" * 60)

    try:
        import notebook
        print("✅ Jupyter Notebook ya está instalado.\n")
    except ImportError:
        print("⚙️ Instalando Jupyter Notebook...\n")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-U", "notebook"]
            )
            print("✅ Instalación completada correctamente.\n")
        except Exception as e:
            print("❌ Error al instalar Jupyter Notebook:")
            print(e)
            sys.exit(1)


def ejecutar_jupyter():
    """Ejecuta Jupyter Notebook en la ruta del proyecto."""
    print("=" * 60)
    print("🚀 INICIANDO JUPYTER NOTEBOOK EN LA RUTA DEL PROYECTO")
    print("=" * 60)

    # 📍 Ruta del proyecto (directorio actual)
    project_root = "."

    # Validar que exista
    if not os.path.exists(project_root):
        print(f"❌ La ruta especificada no existe:\n{project_root}")
        sys.exit(1)

    print(f"📁 Directorio del proyecto: {project_root}\n")

    try:
        # Comando completo (entre comillas por los espacios)
        cmd = f'"{sys.executable}" -m notebook --notebook-dir="{project_root}"'

        # Ejecutar sin bloquear la consola
        subprocess.Popen(
            shlex.split(cmd),
            cwd=project_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True  # necesario en Windows para rutas con espacios
        )

        time.sleep(3)
        webbrowser.open("http://localhost:8888/tree")

        print("✅ Jupyter Notebook iniciado correctamente.")
        print("🌐 Abre tu navegador en: http://localhost:8888/tree\n")
        print(f"📂 Mostrando archivos desde: {project_root}\n")

    except Exception as e:
        print("❌ Error al ejecutar Jupyter Notebook:")
        print(e)


def mainJupyter():
    instalar_jupyter()
    ejecutar_jupyter()


if __name__ == "__main__":
    mainJupyter()
