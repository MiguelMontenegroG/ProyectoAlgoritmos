# Algoritmos de Similitud Textual para Abstracts Científicos

Este documento describe los **6 algoritmos de similitud textual** implementados (4 clásicos + 2 con IA) para análisis de abstracts científicos.

## 📋 Tabla de Contenidos

1. [Algoritmos Clásicos](#algoritmos-clásicos)
   - [Distancia de Levenshtein](#1-distancia-de-levenshtein)
   - [Similitud Jaccard](#2-similitud-jaccard)
   - [Jaro-Winkler](#3-jaro-winkler)
   - [TF-IDF + Coseno](#4-tfidf--coseno)
2. [Modelos de IA](#modelos-de-ia)
   - [BERT](#5-bert)
   - [Sentence-BERT](#6-sentence-bert)
3. [Comparación](#comparación)
4. [Uso](#uso)

---

## Algoritmos Clásicos

### 1. Distancia de Levenshtein

**Tipo:** Clásico basado en caracteres

#### Explicación Matemática

La distancia de Levenshtein mide el número mínimo de ediciones (inserción, eliminación, sustitución) necesarias para transformar una cadena en otra.

**Fórmula recursiva:**
```
lev(a, b) = max(|a|, |b|)                    si min(|a|,|b|) = 0
lev(a, b) = lev(a[1:], b[1:])                si a[0] = b[0]
lev(a, b) = 1 + min(
    lev(a[1:], b),      # eliminación
    lev(a, b[1:]),      # inserción
    lev(a[1:], b[1:])   # sustitución
)                                             en otro caso
```

**Matriz de Programación Dinámica:**
```
    ""  c  a  t
""   0  1  2  3
d    1  1  2  3
o    2  2  2  3
g    3  3  3  3
```

#### Algoritmo Paso a Paso

1. **Inicializar matriz** de tamaño (m+1) × (n+1)
2. **Llenar primera fila y columna** con índices 0..m, 0..n
3. **Iterar** para cada posición (i,j):
   - Si caracteres coinciden: `dp[i][j] = dp[i-1][j-1]`
   - Si no coinciden: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
4. **Resultado:** `dp[m][n]` contiene la distancia

**Similitud normalizada:** `1 - (distancia / max_longitud)`

#### Características
- **Complejidad:** O(m × n) tiempo, O(m × n) espacio
- **Rango:** [0, max_longitud]
- **Uso ideal:** Similitud character-level, edición de textos

#### Ejemplo
```
"kitten" → "sitting"

Operaciones:
1. Sustituir 'k' por 's': "sitten"
2. Sustituir 'e' por 'i': "sittin"
3. Insertar 'g':         "sitting"

Distancia = 3
```

---

### 2. Similitud Jaccard

**Tipo:** Clásico basado en conjuntos

#### Explicación Matemática

El coeficiente de Jaccard compara la similitud entre conjuntos calculando la razón entre la intersección y la unión.

**Fórmula:**
```
J(A, B) = |A ∩ B| / |A ∪ B|

Donde:
- A ∩ B: Elementos comunes
- A ∪ B: Elementos únicos totales
```

**Rango:** [0, 1]
- 0: Conjuntos completamente disjuntos
- 1: Conjuntos idénticos

#### Algoritmo Paso a Paso

1. **Tokenizar** ambos textos en palabras
2. **Convertir a conjuntos** para obtener elementos únicos
3. **Calcular intersección:** palabras comunes en ambos textos
4. **Calcular unión:** todas las palabras únicas
5. **Aplicar fórmula:** intersección_size / union_size

#### Ejemplo

```
Texto 1: "machine learning algorithm"
Tokens 1: {machine, learning, algorithm}

Texto 2: "machine learning model"
Tokens 2: {machine, learning, model}

Intersección: {machine, learning} → tamaño = 2
Unión: {machine, learning, algorithm, model} → tamaño = 4

J = 2 / 4 = 0.5
```

#### Características
- **Complejidad:** O(n + m) siendo n y m tamaños de los conjuntos
- **Rango:** [0, 1]
- **Uso ideal:** Similitud de conjuntos, filtrado de duplicados

#### Ventajas y Desventajas
✅ Simple y rápido
✅ No sensible al orden de palabras
✅ Interpretación intuitiva

❌ No considera frecuencia de palabras
❌ Sensible a vocabulario diferente

---

### 3. Jaro-Winkler

**Tipo:** Clásico especializado en strings cortos

#### Explicación Matemática

Jaro-Winkler es una mejora del algoritmo Jaro, optimizada para detectar errores tipográficos en nombres y strings cortos.

**JARO (base):**
```
jaro = (m/|s1| + m/|s2| + (m-t)/m) / 3

Donde:
- m: número de caracteres coincidentes
- t: número de transposiciones
- |s1|, |s2|: longitudes de los strings
```

**Ventana de búsqueda (match window):**
```
match_window = max(|s1|, |s2|) / 2 - 1
```

**JARO-WINKLER (mejorado):**
```
jaro_winkler = jaro + (l × p × (1 - jaro))

Donde:
- l: longitud del prefijo común (máximo 4)
- p: factor de escala (típicamente 0.1)
```

#### Algoritmo Paso a Paso

**JARO:**
1. Determinar ventana de búsqueda
2. Marcar caracteres coincidentes en ambas cadenas
3. Contar coincidencias y transposiciones
4. Aplicar fórmula Jaro

**JARO-WINKLER:**
5. Encontrar prefijo común (máximo 4 caracteres)
6. Aplicar bonificación al prefijo
7. Calcular similitud final

#### Ejemplo

```
s1 = "john"
s2 = "juan"

Ventana = 4/2 - 1 = 1

Coincidencias encontradas:
- 'j' en posición 0: ✓
- 'o' en posición 1: en 's2' está en posición 2 (dentro ventana) ✓
- 'h' en posición 2: ✗
- 'n' en posición 3: en 's2' está en posición 3 ✓

Coincidencias: 3
Transposiciones: 0

jaro = (3/4 + 3/4 + 3/3) / 3 = 0.917

Prefijo común: "j" (longitud 1)
jaro_winkler = 0.917 + (1 × 0.1 × (1 - 0.917)) = 0.925
```

#### Características
- **Complejidad:** O(m × n) en el peor caso
- **Rango:** [0, 1]
- **Uso ideal:** Detección de errores tipográficos, matching de nombres

---

### 4. TF-IDF + Coseno

**Tipo:** Clásico estadístico

#### Explicación Matemática

**TF (Term Frequency):**
```
tf(t, d) = (frecuencia de t en d) / (total de términos en d)
```

**IDF (Inverse Document Frequency):**
```
idf(t) = log(total de documentos / documentos con t)
```

**TF-IDF:**
```
tfidf(t, d) = tf(t, d) × idf(t)
```

**Similitud de Coseno:**
```
cos(u, v) = (u · v) / (||u|| × ||v||)

donde u y v son vectores TF-IDF
```

#### Algoritmo Paso a Paso

1. **Tokenizar** cada texto
2. **Calcular TF** para cada término en cada documento
3. **Calcular IDF** basado en la colección
4. **Construir vectores TF-IDF** (matriz término-documento)
5. **Normalizar vectores** (dividir por su magnitud)
6. **Calcular producto punto** entre vectores normalizados
7. **Resultado:** similitud en [0, 1]

#### Ejemplo

```
Corpus: [Doc1: "machine learning", Doc2: "deep learning"]

TF (documento 1):
- machine: 1/2 = 0.5
- learning: 1/2 = 0.5

IDF:
- machine: log(2/1) = 0.301
- learning: log(2/2) = 0.0
- deep: log(2/1) = 0.301

TF-IDF (documento 1):
- machine: 0.5 × 0.301 = 0.151
- learning: 0.5 × 0.0 = 0.0

Vector 1: [0.151, 0.0, 0.0]
Vector 2: [0.0, 0.0, 0.151]

cos(v1, v2) = 0 (sin términos en común)
```

#### Características
- **Complejidad:** O(n × m) siendo n documentos, m términos únicos
- **Rango:** [0, 1]
- **Uso ideal:** Búsqueda de documentos, recomendaciones

#### Ventajas
✅ Captura importancia de términos
✅ Rápido y eficiente
✅ Bien documentado y ampliamente usado

---

## Modelos de IA

### 5. BERT

**Tipo:** Transformer bidireccional pre-entrenado

#### Explicación Matemática

**Arquitectura Transformer:**
```
x → Embedding → Positional Encoding → Multi-Head Attention → Feed-Forward → Output
```

**Multi-Head Attention:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k)V

Donde:
- Q: Query
- K: Key
- V: Value
- d_k: dimensión de Key
```

**Producto de atención:**
```
Similitud_atención(q, k) = QK^T / √d_k
```

#### Proceso

1. **Tokenización:** WordPiece (similar a BPE)
   - "unaffordable" → ["un", "##afford", "##able"]

2. **Embedding de tokens:** Vector de 768 dimensiones (BERT-base)

3. **Positional Encoding:** Codifica posición de cada token

4. **Capas Transformer:** 12 capas de atención multinúcleo

5. **Output:** Representación contextual de cada token

#### Algoritmo para Similitud

1. Obtener embedding del token [CLS] de ambos textos
2. Normalizar vectores: `v_norm = v / ||v||`
3. Calcular similitud de coseno: `sim = v1_norm · v2_norm`

#### Ejemplo

```
Texto 1: "El gato está en la casa"
Texto 2: "Un gato está en el hogar"

[CLS] embedding 1: vector_768d_1
[CLS] embedding 2: vector_768d_2

Similitud de coseno: 0.85
```

#### Características
- **Complejidad:** O(n²) donde n es longitud de secuencia
- **Rango:** [0, 1] (para similitud de coseno)
- **Uso ideal:** Tareas semánticas complejas, QA, NER

#### Ventajas
✅ Captura contexto bidireccional
✅ Pre-entrenado en corpus masivo
✅ Excelente para tareas semánticas

---

### 6. Sentence-BERT (SBERT)

**Tipo:** Siamese Network especializada en similitud semántica

#### Explicación Matemática

**Arquitectura Siamese:**
```
Texto 1 → BERT → u → Normalización → Similitud de Coseno
Texto 2 → BERT → v → Normalización ↗

sim = cos(u_norm, v_norm)
```

**Mean Pooling:**
```
sentence_embedding = (1/n) × Σ token_embedding_i
```

**Loss de Triplet (entrenamiento):**
```
Loss = max(0, margin + sim(a, n) - sim(a, p))

Donde:
- a: anchor (texto de referencia)
- p: positive (texto similar)
- n: negative (texto disímil)
- margin: margen de separación
```

#### Algoritmo para Similitud

1. **Tokenizar** ambos textos
2. **Pasar por BERT** para obtener embeddings de cada token
3. **Mean Pooling:** promediar todos los embeddings de tokens
4. **Normalizar:** dividir por la norma
5. **Calcular similitud de coseno**

#### Ejemplo

```
Texto A: "Machine learning es una rama de IA"
Tokens de BERT: [768d, 768d, ..., 768d]  (11 tokens)
Mean pooling: (1/11) × suma de todos = 768d vector

Texto B: "El aprendizaje automático es parte de la IA"
Tokens de BERT: [768d, 768d, ..., 768d]  (12 tokens)
Mean pooling: (1/12) × suma de todos = 768d vector

Similitud = 0.92
```

#### Modelos Disponibles

| Modelo | Dimensión | Velocidad | Precisión | Uso |
|--------|-----------|-----------|-----------|-----|
| all-MiniLM-L6-v2 | 384 | Muy rápida | Buena | Recomendado |
| all-mpnet-base-v2 | 768 | Rápida | Excelente | Máxima precisión |
| paraphrase-MiniLM-L6-v2 | 384 | Muy rápida | Buena | Parafrasis |

#### Características
- **Complejidad:** O(n) con índices FAISS
- **Rango:** [0, 1]
- **Uso ideal:** Similitud semántica, clustering, recomendaciones

#### Ventajas
✅ Optimizado específicamente para similitud
✅ Muy rápido
✅ Captura significado semántico

---

## Comparación

### Matriz de Características

```
┌─────────────────────┬─────────┬──────────┬──────────┬─────────────────┐
│ Algoritmo           │ Tipo    │ Rango    │ Contexto │ Velocidad       │
├─────────────────────┼─────────┼──────────┼──────────┼─────────────────┤
│ Levenshtein         │ Clásico │ [0, max] │ No       │ Rápida (O(n²))  │
│ Jaccard             │ Clásico │ [0, 1]   │ No       │ Muy rápida      │
│ Jaro-Winkler        │ Clásico │ [0, 1]   │ No       │ Rápida          │
│ TF-IDF + Coseno     │ Clásico │ [0, 1]   │ No       │ Rápida          │
│ BERT                │ IA      │ [0, 1]   │ Sí       │ Lenta (GPU)     │
│ Sentence-BERT       │ IA      │ [0, 1]   │ Sí       │ Moderada        │
└─────────────────────┴─────────┴──────────┴──────────┴─────────────────┘
```

### Casos de Uso Recomendados

| Caso de Uso | Algoritmo Recomendado | Razón |
|-------------|----------------------|-------|
| Errores tipográficos | Jaro-Winkler | Optimizado para ello |
| Comparación de palabras clave | Jaccard | Rápido y simple |
| Similitud semántica abstractos | Sentence-BERT | **RECOMENDADO** |
| Búsqueda rápida | TF-IDF + Coseno | Balance velocidad-precisión |
| Análisis character-level | Levenshtein | Nivel de carácter |
| NLP avanzada | BERT | Máxima precisión |

---

## Uso

### 1. Instalación

```bash
pip install transformers torch sentence-transformers scikit-learn nltk
```

### 2. Uso Básico

```python
from src.similarity.text_similarity_analyzer import TextSimilarityAnalyzer

text1 = "Machine learning is a subset of artificial intelligence"
text2 = "AI includes machine learning as a key component"

analyzer = TextSimilarityAnalyzer(text1, text2)
results = analyzer.compute_all()
comparison = analyzer.compare_all()

print(comparison['similarities'])
```

### 3. Análisis Detallado

```python
# Obtener análisis paso a paso
detailed = analyzer.get_detailed_analysis('jaccard')

print(detailed['jaccard']['paso_5_formula'])
print(detailed['jaccard']['resultado_similitud_jaccard'])
```

### 4. Con Abstracts de BibTeX

```python
from src.similarity.text_similarity_analyzer import analyze_abstracts

# Cargar abstracts del BibTeX (ver Notebook)
result = analyze_abstracts(abstract1, abstract2, detailed=True)

print(result['comparison']['similarities'])
print(result['detailed_analysis'])
```

### 5. Usar en Notebook Jupyter

```bash
jupyter notebook Text_Similarity_Analysis.ipynb
```

---

## Archivos Generados

```
src/similarity/
├── edit_distance.py              # Levenshtein
├── jaccard_similarity.py          # Jaccard
├── jaro_winkler.py               # Jaro-Winkler
├── bert_similarity.py            # BERT
├── sentence_bert_similarity.py   # Sentence-BERT
└── text_similarity_analyzer.py   # Integrador

Text_Similarity_Analysis.ipynb     # Notebook interactivo
ALGORITMOS_SIMILITUD_TEXTUAL.md   # Esta documentación
```

---

## Referencias

1. **Levenshtein (1966):** "Binary Codes Capable of Correcting Deletions, Insertions and Reversals"
2. **Jaccard (1912):** "The Distribution of the Flora in the Alpine Zone"
3. **Jaro (1989):** "Advances in Record-Linkage Methodology"
4. **Devlin et al. (2018):** "BERT: Pre-training of Deep Bidirectional Transformers"
5. **Reimers & Gurevych (2019):** "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

---

## Notas

- Para máxima precisión en similitud de abstracts científicos, **usa Sentence-BERT**
- Los modelos IA requieren GPU para mejor rendimiento
- Todos los algoritmos están optimizados para funcionar con abstracts completos
- El Notebook Jupyter incluye visualizaciones interactivas

---

*Última actualización: 2024*