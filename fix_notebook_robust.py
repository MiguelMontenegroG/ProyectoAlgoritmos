#!/usr/bin/env python3
"""
Script para arreglar el problema de NameError en el notebook de análisis de similitud textual.
Crea una solución ROBUSTA que carga todas las dependencias automáticamente.
"""

import json
import re

def fix_notebook_robust():
    """Agrega lógica de recuperación robusta a todas las celdas que usan detailed_results"""
    
    notebook_path = r"C:\Users\NICOLAS PEÑA RINCON\Documents\GitHub\ProyectoAlgoritmos\Text_Similarity_Analysis.ipynb"
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Código de verificación ROBUSTA que se inyectará al inicio de las celdas problemáticas
    robust_verification = '''# ✅ VERIFICACIÓN ROBUSTA: Asegurar que todas las dependencias existen

# 1. Verificar si detailed_results existe y está completo
detailed_results_exists = 'detailed_results' in locals() and isinstance(detailed_results, dict)
has_all_algorithms = detailed_results_exists and all(
    key in detailed_results for key in ['edit_distance', 'jaccard', 'jaro_winkler', 'bert', 'sentence_bert']
)

if not has_all_algorithms:
    # 2. Intentar obtener de analyzer si existe
    try:
        if 'analyzer' in locals() and hasattr(analyzer, 'get_detailed_analysis'):
            detailed_results = analyzer.get_detailed_analysis('all')
            print("✓ detailed_results regenerado desde analyzer")
    except Exception as e:
        # 3. Intentar recrear analyzer desde abstracts
        try:
            if 'abstracts' in locals() and 'index1' in locals() and 'index2' in locals():
                if len(abstracts) > max(index1, index2):
                    # Importar TextSimilarityAnalyzer
                    import sys
                    sys.path.insert(0, r'C:\\Users\\NICOLAS PEÑA RINCON\\Documents\\GitHub\\ProyectoAlgoritmos')
                    from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer
                    
                    analyzer = TextSimilarityAnalyzer(
                        abstracts[index1]['abstract'],
                        abstracts[index2]['abstract']
                    )
                    detailed_results = analyzer.get_detailed_analysis('all')
                    print("✓ analyzer y detailed_results recreados desde abstracts")
                else:
                    raise ValueError("Índices fuera de rango")
            else:
                raise NameError("abstracts, index1 o index2 no definidos")
        except Exception as e2:
            # 4. Último recurso: cargar todo desde cero
            try:
                # Cargar bibtex
                import sys
                import bibtexparser
                from bibtexparser.bparser import BibTexParser
                from bibtexparser.customization import convert_to_unicode
                
                sys.path.insert(0, r'C:\\Users\\NICOLAS PEÑA RINCON\\Documents\\GitHub\\ProyectoAlgoritmos')
                from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer
                
                bibtex_path = r'C:\\Users\\NICOLAS PEÑA RINCON\\Documents\\GitHub\\ProyectoAlgoritmos\\output\\unified_cleaned.bib'
                
                parser = BibTexParser()
                parser.customization = convert_to_unicode
                
                with open(bibtex_path, 'r', encoding='utf-8', errors='ignore') as f:
                    bibtex_db = bibtexparser.load(f, parser=parser)
                
                abstracts = []
                for entry in bibtex_db.entries:
                    if 'abstract' in entry and entry['abstract'].strip():
                        abstracts.append({
                            'id': entry.get('ID', 'Unknown'),
                            'title': entry.get('title', 'No title'),
                            'abstract': entry['abstract'],
                            'year': entry.get('year', 'N/A')
                        })
                
                index1 = 0
                index2 = 1
                
                if len(abstracts) > max(index1, index2):
                    analyzer = TextSimilarityAnalyzer(
                        abstracts[index1]['abstract'],
                        abstracts[index2]['abstract']
                    )
                    detailed_results = analyzer.get_detailed_analysis('all')
                    print("✓ Todas las dependencias cargadas y recreadas desde cero")
                else:
                    raise ValueError("No hay suficientes abstracts")
            except Exception as e3:
                print(f"\\n❌ No se pudo recrear las dependencias. Errores:")
                print(f"   Tier 1 (analyzer.get_detailed_analysis): {str(e)[:100]}")
                print(f"   Tier 2 (recrear analyzer): {str(e2)[:100]}")
                print(f"   Tier 3 (cargar desde cero): {str(e3)[:100]}")
                print(f"\\n📋 INSTRUCCIONES:")
                print(f"   1. Ejecuta la celda 'Instalaciones requeridas' (Celda 1)")
                print(f"   2. Ejecuta la celda de 'Importaciones' (Celda 2)")
                print(f"   3. Ejecuta la celda que carga abstracts desde BibTeX (Celda 3)")
                print(f"   4. Ejecuta la celda que selecciona índices (Celda 5)")
                print(f"   5. Ejecuta la celda que crea el analyzer (Celda 6)")
                print(f"   6. Ahora ejecuta esta celda de nuevo")
                detailed_results = {}
'''

    fixed_count = 0
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        
        # Obtener el código como string
        if isinstance(cell['source'], list):
            source = ''.join(cell['source'])
        else:
            source = cell['source']
        
        # Patrones que indican que la celda usa detailed_results
        uses_detailed_results = (
            "'sentence_bert' in detailed_results" in source or
            "'jaccard' in detailed_results" in source or
            "'jaro_winkler' in detailed_results" in source or
            "'bert' in detailed_results" in source
        )
        
        if uses_detailed_results:
            # Verificar si ya tiene la verificación robusta antigua
            if "VERIFICACIÓN ROBUSTA" in source and "Tier 1" not in source:
                print(f"Celda {i}: Ya tiene verificación. Reemplazando...")
                
                # Encontrar el inicio del bloque try
                try_match = re.search(r'try:\s*if .*?in detailed_results', source)
                if try_match:
                    # Encontrar el final del bloque try-except-except completo
                    rest_of_source = source[try_match.start():]
                    
                    # Contar bloques try-except-except para encontrar dónde termina
                    lines = rest_of_source.split('\n')
                    indent_level = len(lines[0]) - len(lines[0].lstrip())
                    
                    # Buscar la siguiente línea al mismo nivel de indentación que no sea parte del try-except
                    end_line = 0
                    in_except = 0
                    for j, line in enumerate(lines[1:], 1):
                        if line.strip().startswith('except'):
                            in_except += 1
                        elif line and not line[0].isspace() and line.strip():
                            # Línea sin indentación - fin de la estructura try-except
                            end_line = j
                            break
                        elif line.strip() and (len(line) - len(line.lstrip())) <= indent_level:
                            if not line.strip().startswith('except'):
                                end_line = j
                                break
                    
                    if end_line == 0:
                        end_line = len(lines)
                    
                    # Reconstruir el código
                    before = source[:try_match.start()]
                    after = '\n'.join(lines[end_line:]) if end_line < len(lines) else ''
                    
                    new_source = before + robust_verification + '\n\n' + after
                    
                    # Asignar el código actualizado
                    if isinstance(cell['source'], list):
                        cell['source'] = new_source.split('\n')
                        # Agregar saltos de línea al final de cada línea excepto la última
                        cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                    else:
                        cell['source'] = new_source
                    
                    fixed_count += 1
                    print(f"  ✓ Celda {i} actualizada con verificación robusta (Tier 1-3)")
    
    # Guardar el notebook actualizado
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"\n✅ Proceso completado: {fixed_count} celdas actualizadas con lógica robusta.")
    print(f"📁 Notebook guardado en: {notebook_path}")

if __name__ == '__main__':
    fix_notebook_robust()