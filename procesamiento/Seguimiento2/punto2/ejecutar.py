#!/usr/bin/env python
"""
Menú interactivo para elegir qué análisis ejecutar.
Uso: python ejecutar.py
"""

import os
import sys
from pathlib import Path


def clear_screen():
    """Limpia la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Imprime el banner principal."""
    print("\n" + "="*70)
    print("   🎯 SISTEMA DE ANÁLISIS DE GRAFO DE COOCURRENCIA")
    print("   Análisis de Términos en Publicaciones Científicas")
    print("="*70)


def print_menu():
    """Imprime el menú de opciones."""
    print("\n¿Qué deseas hacer?\n")
    print("  1️⃣  PRUEBA RÁPIDA (2 minutos)")
    print("      └─ Procesa 100 documentos")
    print("      └─ Generas 3 visualizaciones")
    print("      └─ ⭐ RECOMENDADO PARA EMPEZAR\n")
    
    print("  2️⃣  ANÁLISIS COMPLETO CON PROGRESO (10-15 minutos)")
    print("      └─ Procesa ~4000 documentos")
    print("      └─ Generas 5 visualizaciones")
    print("      └─ BARRAS DE PROGRESO EN TIEMPO REAL")
    print("      └─ 🏆 LO MEJOR\n")
    
    print("  3️⃣  VALIDACIÓN RÁPIDA (30 segundos)")
    print("      └─ Solo valida que funcione")
    print("      └─ Procesa 3 documentos de ejemplo\n")
    
    print("  4️⃣  ANÁLISIS PERSONALIZADO")
    print("      └─ Tu eliges cuántos documentos procesar\n")
    
    print("  0️⃣  SALIR\n")


def get_choice():
    """Obtiene la elección del usuario."""
    while True:
        try:
            choice = input("Elige una opción (0-4): ").strip()
            if choice in ['0', '1', '2', '3', '4']:
                return choice
            print("❌ Opción inválida. Intenta de nuevo.\n")
        except KeyboardInterrupt:
            print("\n\n👋 Hasta luego!")
            sys.exit(0)


def run_script(script_name):
    """Ejecuta un script Python."""
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print(f"❌ Error: No se encuentra {script_name}")
        return False
    
    print(f"\n🚀 Ejecutando {script_name}...\n")
    os.system(f"{sys.executable} \"{script_path}\"")
    return True


def get_custom_docs():
    """Pide al usuario cuántos documentos procesar."""
    while True:
        try:
            num = int(input("\n¿Cuántos documentos deseas procesar? (1-5000): ").strip())
            if 1 <= num <= 5000:
                return num
            print(f"❌ Elige un número entre 1 y 5000")
        except ValueError:
            print(f"❌ Debes ingresar un número")
        except KeyboardInterrupt:
            print("\n👋 Cancelado")
            return None


def modify_max_documents(num_docs):
    """Modifica MAX_DOCUMENTS en main_fast.py."""
    main_fast_path = Path(__file__).parent / "main_fast.py"
    
    try:
        with open(main_fast_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar y reemplazar MAX_DOCUMENTS
        import re
        pattern = r'MAX_DOCUMENTS = \d+'
        replacement = f'MAX_DOCUMENTS = {num_docs}'
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(main_fast_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Configurado para procesar {num_docs} documentos")
        return True
    except Exception as e:
        print(f"❌ Error al modificar configuración: {e}")
        return False


def main():
    """Función principal."""
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = get_choice()
        
        if choice == '0':
            print("\n👋 Hasta luego!\n")
            break
        
        elif choice == '1':
            print("\n" + "="*70)
            print("⚡ INICIANDO ANÁLISIS RÁPIDO")
            print("="*70)
            print("📊 Documentos: 100")
            print("⏱️  Tiempo estimado: 1-2 minutos")
            print("✨ Generará visualizaciones y reporte\n")
            input("Presiona ENTER para comenzar...")
            run_script("main_fast.py")
        
        elif choice == '2':
            print("\n" + "="*70)
            print("🔍 INICIANDO ANÁLISIS COMPLETO")
            print("="*70)
            print("📊 Documentos: ~4000")
            print("⏱️  Tiempo estimado: 10-15 minutos")
            print("📈 Verás barras de progreso en tiempo real")
            print("✨ Análisis exhaustivo con visualizaciones detalladas\n")
            input("Presiona ENTER para comenzar...")
            run_script("main_with_progress.py")
        
        elif choice == '3':
            print("\n" + "="*70)
            print("✅ VALIDACIÓN DEL SISTEMA")
            print("="*70)
            print("📊 Documentos: 3 (ejemplo)")
            print("⏱️  Tiempo estimado: 30 segundos")
            print("✨ Solo valida que todo funcione\n")
            input("Presiona ENTER para comenzar...")
            run_script("test_simple.py")
        
        elif choice == '4':
            print("\n" + "="*70)
            print("⚙️ ANÁLISIS PERSONALIZADO")
            print("="*70)
            
            num_docs = get_custom_docs()
            if num_docs is None:
                continue
            
            print(f"\n🔧 Configurando para {num_docs} documentos...")
            if not modify_max_documents(num_docs):
                continue
            
            print("⏱️  Tiempo estimado: variable según cantidad")
            input("\nPresiona ENTER para comenzar...")
            run_script("main_fast.py")
        
        # Menú post-ejecución
        print("\n" + "="*70)
        choice_after = input("\n¿Qué deseas hacer ahora?\n\n"
                            "1. Ejecutar otro análisis\n"
                            "2. Ver archivos generados\n"
                            "3. Salir\n\n"
                            "Elige una opción (1-3): ").strip()
        
        if choice_after == '2':
            output_dir = Path(__file__).parent / "output"
            os.system(f'explorer "{output_dir}"')
        elif choice_after == '3':
            print("\n👋 Hasta luego!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()