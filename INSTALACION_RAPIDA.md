# ⚡ Instalación Rápida

## 🚀 3 pasos para empezar

### Paso 1: Instalar dependencias
```bash
python install_dependencies.py
```

O manualmente:
```bash
pip install pandas scikit-learn nltk bibtexparser jupyter matplotlib seaborn
```

### Paso 2: Descargar modelos de IA (OPCIONAL, pero recomendado)
```bash
pip install transformers torch sentence-transformers
```

> ⚠️ Nota: Esto descarga ~2GB. Si no tienes espacio, omite este paso. El notebook funcionará sin los modelos de IA.

### Paso 3: Ejecutar Jupyter
```bash
jupyter notebook Text_Similarity_Analysis.ipynb
```

---

## ✅ Verificar instalación

En Python/Jupyter:
```python
import pandas, scikit-learn, nltk, bibtexparser
print("✓ Básicos OK")

try:
    import matplotlib, seaborn
    print("✓ Visualización OK")
except:
    print("⚠️  Visualización no disponible")

try:
    import transformers, torch, sentence_transformers
    print("✓ Modelos IA OK")
except:
    print("⚠️  Modelos IA no disponibles")
```

---

## 🎯 Alternativa: Usar Google Colab (GRATIS)

Si tienes problemas de instalación local:

1. Sube `Text_Similarity_Analysis.ipynb` a Google Colab
2. Ejecuta la primera celda (instala en la nube)
3. El resto funciona igual

Google Colab tiene todo preinstalado + GPU gratis 🚀

---

## 📋 Requisitos Mínimos

| Componente | Obligatorio? | Función |
|-----------|------------|---------|
| Python 3.8+ | ✅ Sí | Runtime |
| pandas | ✅ Sí | Manejo de datos |
| scikit-learn | ✅ Sí | TF-IDF, Coseno |
| nltk | ✅ Sí | Tokenización |
| bibtexparser | ✅ Sí | Lectura BibTeX |
| matplotlib | ❌ No | Gráficas |
| seaborn | ❌ No | Gráficas estadísticas |
| transformers | ❌ No | Modelo BERT |
| torch | ❌ No | Aceleración IA |
| sentence-transformers | ❌ No | Sentence-BERT |

---

## 💡 Recomendaciones

**Para máxima experiencia:**
```bash
pip install pandas scikit-learn nltk bibtexparser jupyter matplotlib seaborn transformers torch sentence-transformers
```

**Minimalista (solo algoritmos clásicos):**
```bash
pip install pandas scikit-learn nltk bibtexparser jupyter
```

**Sin visualización:**
```bash
pip install pandas scikit-learn nltk bibtexparser transformers torch sentence-transformers
```
