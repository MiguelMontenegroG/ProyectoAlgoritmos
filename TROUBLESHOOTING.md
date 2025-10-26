# 🔧 Troubleshooting - Errores Comunes

## ❌ Error: `CalledProcessError: Command pip install returned non-zero exit status`

### Causa
El comando pip falla durante la instalación de paquetes. Generalmente es por:
- Problemas de permisos
- Versión de Python incompatible
- Conexión a Internet deficiente
- Conflictos de dependencias

### Solución

**Opción 1: Usar el script de instalación (RECOMENDADO)**
```bash
python install_dependencies.py
```

**Opción 2: Instalar manualmente paquetes obligatorios**
```bash
python -m pip install --upgrade pip
python -m pip install pandas scikit-learn nltk bibtexparser
```

**Opción 3: Instalar paquetes opcionales por separado**
```bash
# Visualización
python -m pip install matplotlib seaborn

# Modelos de IA (más pesados, pueden tardar)
python -m pip install transformers torch
python -m pip install sentence-transformers
```

---

## ❌ Error: `ModuleNotFoundError: No module named 'matplotlib'`

### Causa
Matplotlib no está instalado.

### Solución
```bash
python -m pip install matplotlib seaborn
```

El Jupyter notebook ahora tolera su ausencia - funcionará sin gráficas.

---

## ❌ Error: `ModuleNotFoundError: No module named 'torch'`

### Causa
PyTorch no está instalado (necesario para BERT y Sentence-BERT).

### Solución

**Para CPU (más pequeño, más lento):**
```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Para GPU (NVIDIA CUDA):**
```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Luego instala los modelos:
```bash
python -m pip install transformers sentence-transformers
```

---

## ⚠️ Jupyter Notebook: Celdas se quedan "ejecutando"

### Causa
Los modelos de IA tardan mucho en descargarse/procesarse la primera vez.

### Solución
- **Primera ejecución**: Paciencia. Los modelos BERT/Sentence-BERT se descargan ~1GB.
- **Siguientes ejecuciones**: Serán más rápidas (datos cacheados).
- **Puedes detener**: Presiona el botón de "stop" en Jupyter si tarda demasiado.

---

## ❌ Error: `ImportError: cannot import name 'BibTexParser'`

### Causa
Versión antigua de `bibtexparser`.

### Solución
```bash
python -m pip install --upgrade bibtexparser
```

---

## ❌ Error: `FileNotFoundError: output/unified_cleaned.bib`

### Causa
El archivo BibTeX no existe en la ruta esperada.

### Solución
1. Verifica que ejecutas el notebook desde el directorio raíz del proyecto
2. Asegúrate de que `output/unified_cleaned.bib` existe
3. O genera el archivo ejecutando primero los scripts de procesamiento

---

## ✅ Todo instalado pero Jupyter no funciona

### Solución 1: Reinicia Jupyter
```bash
# Cierra Jupyter (Ctrl+C en la terminal)
# Luego reinicia
jupyter notebook
```

### Solución 2: Kernel no válido
```bash
# Asegúrate de usar el kernel correcto (Python 3.9+)
python -m ipykernel install --user --name python3
```

### Solución 3: Limpia caché
```bash
# En Windows
rmdir /s %TEMP%\.jupyter
# En Linux/Mac
rm -rf ~/.cache/jupyter
```

---

## 📊 Instalar solo lo básico (sin IA)

Si solo quieres usar los algoritmos clásicos sin BERT/Sentence-BERT:

```bash
python -m pip install pandas scikit-learn nltk bibtexparser matplotlib seaborn
```

Esto evita descargar ~3GB de PyTorch.

---

## 🆘 Si nada funciona

Crea un **ambiente virtual limpio**:

```bash
# Crear ambiente
python -m venv venv_algebra

# Activar
# En Windows:
venv_algebra\Scripts\activate
# En Linux/Mac:
source venv_algebra/bin/activate

# Instalar
pip install pandas scikit-learn nltk bibtexparser jupyter matplotlib seaborn

# Luego opcional:
pip install transformers torch sentence-transformers
```

---

## 📞 Verificar instalación

Ejecuta este script para diagnosticar:

```python
import sys
packages = {
    'pandas': '✓', 'scikit-learn': '✓', 'nltk': '✓', 'bibtexparser': '✓',
    'matplotlib': '◐', 'seaborn': '◐',
    'transformers': '◐', 'torch': '◐', 'sentence_transformers': '◐'
}

for pkg, req in packages.items():
    try:
        __import__(pkg.replace('_', '-'))
        status = '✓ OK'
    except ImportError:
        status = '❌ NO INSTALADO'
    req_type = "[OBLIGATORIO]" if req == "✓" else "[OPCIONAL]"
    print(f"{pkg:<25} {status:<15} {req_type}")
```
