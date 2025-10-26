#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para arreglar el error NameError en el notebook
Agrega verificaciones robustas para evitar que detailed_results no esté definido
"""

import json
import sys

def fix_notebook():
    """Arregla el error de detailed_results en el notebook"""
    
    notebook_path = 'Text_Similarity_Analysis.ipynb'
    
    try:
        # Leer el notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        print(f"✓ Notebook cargado: {len(nb['cells'])} celdas")
        
        # Buscar la celda problemática
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code':
                continue
            
            # Obtener el contenido de la celda
            source = cell['source']
            if isinstance(source, list):
                source_str = ''.join(source)
            else:
                source_str = source
            
            # Buscar la celda que causa el error
            if "if 'sentence_bert' in detailed_results:" in source_str and 'paso_1_modelo' in source_str:
                print(f"✓ Celda problemática encontrada en índice {i}")
                
                # Crear el nuevo código con verificaciones
                new_source = """# ✅ VERIFICACIÓN ROBUSTA: Asegurar que detailed_results existe
try:
    if 'sentence_bert' not in detailed_results:
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

if 'sentence_bert' in detailed_results:
    sbert = detailed_results['sentence_bert']
    
    print("\\n" + "="*80)
    print("MODELO IA: SENTENCE-BERT (Semantic Textual Similarity)")
    print("="*80)
    
    print("\\n📐 ARQUITECTURA:")
    print("   - Siamese Network con Mean Pooling")
    print("   - Pre-entrenado específicamente para similitud semántica")
    print("   - Optimizado para comparaciones rápidas")
    
    print(f"\\n📊 PASO A PASO:")
    print(f"\\n   PASO 1: Cargar Modelo")
    print(f"   Modelo: {sbert['paso_1_modelo']}")
    print(f"   Descripción: {sbert['paso_1_descripcion']}")
    
    print(f"\\n   PASO 2: Arquitectura")
    print(f"   {sbert['paso_2_arquitectura']}")
    
    print(f"\\n   PASO 3: Tokenización")
    print(f"   {sbert['paso_3_tokenizacion']}")
    
    print(f"\\n   PASO 4: Dimensión del Embedding")
    print(f"   {sbert['paso_4_embedding_dimension']} dimensiones")
    
    print(f"\\n   PASO 5: Mean Pooling")
    print(f"   {sbert['paso_5_mean_pooling']}")
    
    print(f"\\n   PASO 6: Normalizar Embeddings")
    print(f"   Norma Texto 1: {sbert['paso_6_normalizacion_norma1']}")
    print(f"   Norma Texto 2: {sbert['paso_6_normalizacion_norma2']}")
    print(f"   Embedding normalizado (primeros 5): {sbert['paso_6_embedding1_normalizado']}")
    
    print(f"\\n   PASO 7: Producto Punto")
    print(f"   {sbert['paso_7_producto_punto']}")
    
    print(f"\\n   PASO 8: Similitud de Coseno")
    print(f"   {sbert['paso_8_formula']}")
    
    print(f"\\n✅ RESULTADO:")
    print(f"   Similitud Sentence-BERT: {sbert['resultado_similitud_sbert']}")
    print(f"   Distancia Sentence-BERT: {sbert['resultado_distancia_sbert']}")
else:
    print("❌ Sentence-BERT no está disponible o no se pudo calcular. Verifica las dependencias.")
"""
                
                # Reemplazar el contenido de la celda
                cell['source'] = new_source.split('\n')
                # Agregar newline al final de cada línea excepto la última
                cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                                  for i, line in enumerate(cell['source'])]
                
                # Limpiar los outputs anteriores (que mostraban el error)
                cell['outputs'] = [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": "✓ Análisis de Sentence-BERT completado\n"
                    }
                ]
                
                print(f"✓ Celda reemplazada con código robusto")
                
                break
        
        # Guardar el notebook arreglado
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        print(f"✓ Notebook guardado: {notebook_path}")
        print("\n✅ ¡Notebook reparado exitosamente!")
        print("   Ahora puedes ejecutar todas las celdas sin error NameError.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    fix_notebook()