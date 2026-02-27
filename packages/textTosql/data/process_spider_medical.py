import json
import os
import random

# Configuration
SPIDER_ROOT = "data/spider/evaluation_examples/examples"
OUTPUT_DIR = "data/spider_medical"

# Target Medical Databases for Testing/Validation
# We will evaluate on these, but train on EVERYTHING to get better SQL grammar
MEDICAL_DB_IDS = [
    "hospital_1", 
    "patient_record", 
    "perpetual_condition_index", 
    "medicine_enzyme_interaction",
    "medicine_request",
    "gene_disease_association",
    "allergy_1" # Added allergy_1 as it's close to medical
]

def process():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Read Spider Train Data
    train_file = os.path.join(SPIDER_ROOT, "train_spider.json")
    if not os.path.exists(train_file):
        print(f"Error: {train_file} not found. Please ensure Spider dataset is at {SPIDER_ROOT}")
        return

    with open(train_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. Filter and Split
    # Strategy: Standard 80/10/10 split on ALL available data
    # This provides more robust evaluation metrics
    
    all_data = []
    
    for item in data:
        sample = {
            "text": item["question"],
            "structured": item["query"], 
            "sql": item["query"],
            "db_id": item["db_id"]
        }
        all_data.append(sample)
    
    # Shuffle and Split
    random.shuffle(all_data)
    
    # [OPTIMIZATION] Limit dataset size for faster training
    # Use only 2000 samples total (instead of 7000)
    # This keeps training time reasonable (e.g., < 1 hour) while still learning SQL
    n = min(len(all_data), 2000)
    all_data = all_data[:n]
    
    train_end = int(n * 0.8)
    val_end = int(n * 0.9)
    
    train_set = all_data[:train_end]
    val_set = all_data[train_end:val_end]
    test_set = all_data[val_end:]
    
    # 4. Save to disk
    with open(os.path.join(OUTPUT_DIR, "train.json"), 'w') as f:
        json.dump(train_set, f, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "validation.json"), 'w') as f:
        json.dump(val_set, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "test.json"), 'w') as f:
        json.dump(test_set, f, indent=2)
        
    print(f"Data processing complete.")
    print(f"Total Samples: {n}")
    print(f"Saved to {OUTPUT_DIR}:")
    print(f"- Train: {len(train_set)}")
    print(f"- Validation: {len(val_set)}")
    print(f"- Test: {len(test_set)}")

if __name__ == "__main__":
    process()
