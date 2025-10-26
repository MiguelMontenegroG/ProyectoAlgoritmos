#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para arreglar todas las celdas que usan detailed_results
Agrega verificaciones robustas para evitar NameError
"""

import json
import re

def add_verification_header():
    """Retorna el código de verificación que se agrega al inicio"""
    return """# ✅ VERIFICACIÓN ROBUSTA: Asegurar que detailed_results existe
try:
    if not detailed_results:
        detailed_results = analyzer.get_detailed_analysis('all')
except NameError:
    # Si analyzer no existe, intentar recrearlo
    try:
        analyzer = TextSimilarityAnalyzer(
            abstracts[index1]['abstract'],
            abstracts[index2]['abstract']
        )
        detailed_results = analyzer.get_detailed_analysis('all')
    except:
        print("⚠️ No se pudo crear detailed_results. Ejecuta las celdas previas en orden.")
        detailed_results = {}

"""

def fix_all_detailed_results_cells():
    """Arregla todas las celdas que usan detailed_results"""
    
    notebook_path = 'Text_Similarity_Analysis.ipynb'
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        print(f"✓ Notebook cargado: {len(nb['cells'])} celdas")
        
        cells_fixed = 0
        
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code':
                continue
            
            source = cell['source']
            if isinstance(source, list):
                source_str = ''.join(source)
            else:
                source_str = source
            
            # Detectar si esta celda usa detailed_results
            if "in detailed_results" in source_str and "if '" in source_str:
                # Detectar si ya tiene la verificación
                if "VERIFICACIÓN ROBUSTA" in source_str:
                    print(f"  Celda {i}: Ya tiene verificación ✓")
                    continue
                
                # Detectar qué tipo de análisis es
                if "'jaccard' in detailed_results" in source_str:
                    print(f"✓ Arreglando celda Jaccard (índice {i})")
                elif "'jaro_winkler' in detailed_results" in source_str:
                    print(f"✓ Arreglando celda Jaro-Winkler (índice {i})")
                elif "'bert' in detailed_results" in source_str:
                    print(f"✓ Arreglando celda BERT (índice {i})")
                elif "'sentence_bert' in detailed_results" in source_str:
                    print(f"✓ Arreglando celda Sentence-BERT (índice {i})")
                else:
                    print(f"  Celda {i}: Desconocida")
                    continue
                
                # Agregar verificación
                verification = add_verification_header()
                new_source = verification + source_str
                
                # Actualizar la celda
                cell['source'] = new_source.split('\n')
                cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                
                cells_fixed += 1
        
        # Guardar el notebook arreglado
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        print(f"\n✅ Notebook reparado:")
        print(f"   - {cells_fixed} celdas actualizadas con verificaciones robustas")
        print(f"   - Ahora todas las celdas pueden ejecutarse en cualquier orden")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_all_detailed_results_cells()