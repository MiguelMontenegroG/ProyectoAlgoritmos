#!/usr/bin/env python3
"""
Script de prueba para verificar que las funciones del proyecto funcionan correctamente
"""

import os
import sys
import io
import contextlib

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("Probando importaciones...")

try:
    from procesamiento.Requerimiento2.requerimiento2Ejecutable import mainRequerimiento2
    print("✓ Requerimiento2 importado")
except Exception as e:
    print(f"❌ Error importando Requerimiento2: {e}")

try:
    from procesamiento.Requerimiento3.FrecuenciaPalabra import mainEjecutableRequerimiento3
    print("✓ Requerimiento3 importado")
except Exception as e:
    print(f"❌ Error importando Requerimiento3: {e}")

def test_function(func, name):
    """Prueba una función capturando su salida"""
    print(f"\n{'='*50}")
    print(f"Probando {name}")
    print(f"{'='*50}")

    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
            func()

        output = output_buffer.getvalue()
        print("Salida capturada:")
        print("-" * 30)
        print(output[:500] + "..." if len(output) > 500 else output)
        print("-" * 30)
        print(f"Longitud total: {len(output)} caracteres")

        if output.strip():
            print("✅ Función ejecutada exitosamente")
        else:
            print("⚠️ Función ejecutada pero sin salida")

    except Exception as e:
        print(f"❌ Error ejecutando {name}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nIniciando pruebas de funciones...")

    # Solo probar algunas funciones que deberían ser rápidas
    try:
        test_function(mainRequerimiento2, "Requerimiento 2")
    except:
        pass

    try:
        test_function(mainEjecutableRequerimiento3, "Requerimiento 3")
    except:
        pass

    print("\nPruebas completadas.")