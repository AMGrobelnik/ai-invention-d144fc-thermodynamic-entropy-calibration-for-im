#!/usr/bin/env python3
"""Pre-download models needed for the experiment."""
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import warnings
warnings.filterwarnings('ignore')

models = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "bert-base-uncased",
    "roberta-large-mnli",
]

for model_name in models:
    print(f"Downloading {model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
        print(f"  Downloaded {model_name}")
    except Exception as e:
        print(f"  Error: {e}")
        
print("All models downloaded!")
