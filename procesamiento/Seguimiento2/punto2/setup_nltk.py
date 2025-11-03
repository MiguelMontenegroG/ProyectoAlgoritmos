#!/usr/bin/env python
"""Script para configurar recursos NLTK necesarios."""

import nltk
import sys

print("Descargando recursos NLTK necesarios...")
print("-" * 50)

resources = {
    'punkt_tab': 'Punkt Tab Tokenizer',
    'stopwords': 'Stopwords',
    'wordnet': 'WordNet Lemmatizer',
    'averaged_perceptron_tagger': 'POS Tagger'
}

for resource, name in resources.items():
    try:
        print(f"Descargando {name}...", end=" ")
        nltk.download(resource, quiet=True)
        print("✓")
    except Exception as e:
        print(f"✗ ({e})")

print("-" * 50)
print("✓ Recursos NLTK configurados")