"""
Script rápido para análisis de prueba del sistema.
Procesa solo los primeros N documentos para validación rápida.
Tiempo esperado: 30 segundos a 2 minutos
"""

import sys
import os
from pathlib import Path
import time

# Agregar rutas al path
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent

# Detectar si estamos ejecutando desde un archivo temporal (web app)
is_temp_file = str(script_dir).startswith('/tmp') or str(script_dir).startswith('\\tmp') or 'temp' in str(script_dir).lower()

if is_temp_file:
    # Si es un archivo temporal, usar rutas absolutas
    sys.path.insert(0, str(project_root))
    try:
        from procesamiento.Seguimiento2.punto2.cooccurrence_graph import build_cooccurrence_graph_from_abstracts
        from procesamiento.Seguimiento2.punto2.graph_analyzer import GraphAnalyzer
        from procesamiento.Seguimiento2.punto2.graph_visualizer import GraphVisualizer
    except ImportError as e:
        print(f"❌ Error importando módulos desde archivo temporal: {e}")
        sys.exit(1)
else:
    # Si es el archivo original, usar imports relativos
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(script_dir))

    try:
        from cooccurrence_graph import build_cooccurrence_graph_from_abstracts
        from graph_analyzer import GraphAnalyzer
        from graph_visualizer import GraphVisualizer
    except ImportError as e:
        print(f"❌ Error importando módulos locales: {e}")
        print("Intentando importaciones absolutas...")
        try:
            from procesamiento.Seguimiento2.punto2.cooccurrence_graph import build_cooccurrence_graph_from_abstracts
            from procesamiento.Seguimiento2.punto2.graph_analyzer import GraphAnalyzer
            from procesamiento.Seguimiento2.punto2.graph_visualizer import GraphVisualizer
        except ImportError as e2:
            print(f"❌ Error en importaciones absolutas: {e2}")
            sys.exit(1)
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import json
from datetime import datetime


# ⚙️ CONFIGURACIÓN - MODIFICA AQUÍ PARA DIFERENTES ANÁLISIS
MAX_DOCUMENTS = 100  # Número de documentos a procesar (análisis rápido estándar)
MIN_COOCCURRENCE = 1  # Mínimo de coocurrencias (aumenta para menos ruido)
# ════════════════════════════════════════════════════════════


def load_abstracts_from_bibtex(file_path, max_docs=None):
    """Carga abstracts desde BibTeX, limitando a max_docs si se especifica."""
    try:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            entries = bibtexparser.load(bibtex_file, parser=parser).entries
        
        abstracts = []
        count = 0
        for entry in entries:
            if count >= max_docs:
                break
            if 'abstract' in entry and entry['abstract'].strip():
                abstracts.append(entry['abstract'])
                count += 1
        
        print(f"✓ Cargados {len(abstracts)} abstracts (de {len(entries)} totales)")
        return abstracts
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return []


def print_section(title):
    """Imprime encabezado de sección."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def main():
    """Análisis rápido."""
    
    print("\n" + "="*70)
    print("  ⚡ ANÁLISIS RÁPIDO - PRUEBA DE FUNCIONAMIENTO")
    print("="*70)
    print(f"📊 Documentos a procesar: {MAX_DOCUMENTS}")
    print(f"⏱️  Tiempo estimado: 30-120 segundos\n")
    
    start_time = time.time()
    
    # Rutas - buscar archivo BibTeX automáticamente
    if is_temp_file:
        # Si es archivo temporal, usar la ruta del proyecto que ya tenemos
        output_dir = project_root / 'output'
    else:
        output_dir = Path(__file__).parent.parent.parent.parent / 'output'

    possible_bib_files = [
        output_dir / 'unified_cleaned.bib',
        output_dir / 'unifed_reducido.bib',
        output_dir / 'unified_with_metadata.bib',
        Path(r'C:\Users\ANGEL\Documents\GitHub\ProyectoAlgoritmos\output\unified_cleaned.bib')  # fallback
    ]

    bibtex_file = None
    for bib_path in possible_bib_files:
        if bib_path.exists():
            bibtex_file = str(bib_path)
            break

    if bibtex_file is None:
        print("❌ No se encontró archivo BibTeX. Ejecute primero 'Descargar y Unificar Datos'")
        return

    # Asegurar que el directorio output existe
    output_dir.mkdir(exist_ok=True)
    
    # 1. Cargar abstracts
    print_section("1️⃣  CARGA DE DATOS")
    print(f"📖 Cargando primeros {MAX_DOCUMENTS} documentos...")
    abstracts = load_abstracts_from_bibtex(bibtex_file, max_docs=MAX_DOCUMENTS)
    
    if not abstracts:
        print("✗ No se cargaron abstracts. Abortando...")
        return
    
    # 2. Construir grafo
    print_section("2️⃣  CONSTRUCCIÓN DEL GRAFO")
    print(f"🔗 Construyendo grafo de coocurrencia...")
    
    start_graph = time.time()
    cg = build_cooccurrence_graph_from_abstracts(abstracts, min_cooccurrence=MIN_COOCCURRENCE)
    stats = cg.get_statistics()
    graph_time = time.time() - start_graph
    
    print(f"✓ Grafo construido:")
    print(f"  • Nodos: {stats['total_nodes']}")
    print(f"  • Aristas: {stats['total_edges']}")
    print(f"  • Densidad: {stats['density']:.6f}")
    print(f"  • Grado promedio: {stats['average_degree']:.2f}")
    print(f"  • Tiempo: {graph_time:.2f}s\n")
    
    # 3. Análisis
    print_section("3️⃣  ANÁLISIS DEL GRAFO")
    print("📈 Calculando propiedades...")
    
    analyzer = GraphAnalyzer(cg.get_graph())
    
    # Grados
    degrees = analyzer.calculate_node_degrees()
    top_nodes = analyzer.get_top_nodes_by_degree(10)
    
    print("\n📊 TOP 10 TÉRMINOS POR GRADO:")
    for i, (node, degree) in enumerate(top_nodes, 1):
        print(f"  {i:2d}. {node:35s} - Grado: {degree:3d}")
    
    # Componentes
    components = analyzer.get_connected_components_with_stats()
    print(f"\n🔍 Componentes conexas detectadas: {len(components)}")
    for i, comp in enumerate(components[:5], 1):
        print(f"  Componente {i}: {comp['size']} nodos, densidad: {comp['density']:.4f}")
    
    # Clustering
    avg_clustering = analyzer.get_average_clustering_coefficient()
    print(f"\n🎯 Coeficiente de clustering promedio: {avg_clustering:.4f}")
    
    # 4. Visualizaciones rápidas
    print_section("4️⃣  GENERANDO VISUALIZACIONES")
    
    visualizer = GraphVisualizer(cg.get_graph(), figsize=(14, 10))
    
    print("  🎨 Grafo principal...", end=" ", flush=True)
    visualizer.plot_graph(layout_type='spring', figsize=(14, 10),
                         save_path=str(output_dir / 'cooccurrence_graph_fast.png'))
    print("✓")
    
    print("  📊 Distribución de grados...", end=" ", flush=True)
    visualizer.plot_degree_distribution(analyzer,
                                       save_path=str(output_dir / 'degree_distribution_fast.png'))
    print("✓")
    
    print("  🏆 Nodos principales...", end=" ", flush=True)
    visualizer.plot_top_nodes(analyzer, k=10,
                             save_path=str(output_dir / 'top_nodes_fast.png'))
    print("✓")
    
    # 5. Reporte
    print_section("5️⃣  GENERANDO REPORTE")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'sample_size': len(abstracts),
        'max_documents_config': MAX_DOCUMENTS,
        'min_cooccurrence_config': MIN_COOCCURRENCE,
        'graph_stats': {
            'nodes': stats['total_nodes'],
            'edges': stats['total_edges'],
            'density': stats['density'],
            'average_degree': stats['average_degree']
        },
        'top_nodes': top_nodes,
        'num_components': len(components),
        'clustering_coefficient': float(avg_clustering)
    }
    
    report_path = output_dir / 'analysis_report_fast.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Reporte guardado: {report_path.name}\n")
    
    # Resumen
    print_section("🏁 RESUMEN")
    
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    print(f"✅ Análisis completado en {minutes}m {seconds}s\n")
    print(f"📁 Archivos generados en: output/")
    for file in sorted(output_dir.glob('*fast*')):
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            print(f"   • {file.name} ({size_kb:.1f} KB)")
    
    print("\n💡 Próximos pasos:")
    print("   ✓ Ver imágenes PNG en output/")
    print("   ✓ Ver datos en analysis_report_fast.json")
    print("   ✓ Si funciona bien, ejecutar main_with_progress.py para análisis completo")
    print("   ✓ Para cambiar número de documentos, edita MAX_DOCUMENTS en este archivo\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()