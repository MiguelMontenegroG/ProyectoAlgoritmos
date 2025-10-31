import pandas as pd
from collections import Counter
import re

CATEGORY_WORDS = [
    "generative models", "prompting", "machine learning",
    "multimodality", "fine-tuning", "training data", "algorithmic bias",
    "explainability", "transparency", "ethics", "privacy",
    "personalization", "human-ai interaction", "ai literacy", "co-creation"
]

def clean_text(text):
    return re.sub(r"[^a-zA-Z ]", "", str(text)).lower()

def count_category_words(file_path):
    df = pd.read_csv(file_path)
    abstracts = df["abstract"].dropna().apply(clean_text)

    all_text = " ".join(abstracts)
    counter = Counter(all_text.split())

    print("=== Frecuencia de palabras de la categoría ===")
    for word in CATEGORY_WORDS:
        print(f"{word}: {counter[word.lower()]}")
