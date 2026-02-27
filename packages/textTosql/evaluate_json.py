import json
import argparse
import sys
import os
import evaluate as hf_evaluate

# Add current directory to path to import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from utils.db_utils import MockDB
    from utils.converter import structured_to_sql
except ImportError:
    # Fallback if run from different directory
    sys.path.append(os.path.join(current_dir, "packages", "textTosql"))
    from utils.db_utils import MockDB
    from utils.converter import structured_to_sql

def evaluate_json(input_file):
    print(f"Evaluating {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print("Error: Empty data file.")
        return

    # Check if ground_truth_sql is missing (for backward compatibility)
    if "ground_truth_sql" not in data[0]:
        print("Note: 'ground_truth_sql' field missing in results. Attempting to load from data/test.json...")
        # Assume test.json is in ../data/test.json relative to this script
        test_file_path = os.path.join(current_dir, "data", "test.json")
        
        if os.path.exists(test_file_path):
            with open(test_file_path, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
                # Merge by index
                for i, item in enumerate(data):
                    if i < len(test_data):
                        item["ground_truth_sql"] = test_data[i].get("sql", "")
            print(f"Loaded ground truth SQLs from {test_file_path}")
        else:
            print(f"Warning: test.json not found at {test_file_path}. EM and EX scores will be 0.")

    predictions = []
    references = []
    
    em_count = 0
    ex_count = 0
    
    db = MockDB()
    
    # Try to load metrics
    print("Loading metrics (ROUGE, BLEU)...")
    try:
        rouge = hf_evaluate.load("rouge")
        bleu = hf_evaluate.load("bleu")
    except Exception as e:
        print(f"Warning: Failed to load metrics directly ({e}). Trying reload...")
        import importlib
        importlib.reload(hf_evaluate)
        rouge = hf_evaluate.load("rouge")
        bleu = hf_evaluate.load("bleu")

    print("Computing scores...")
    for item in data:
        pred_structured = item.get("pred_structured", "")
        ground_truth_structured = item.get("ground_truth_structured", "")
        ground_truth_sql = item.get("ground_truth_sql", "")
        
        predictions.append(pred_structured)
        references.append(ground_truth_structured)
        
        # EM (Exact Match) for SQL
        try:
            pred_sql = structured_to_sql(pred_structured)
            if pred_sql.strip().lower() == ground_truth_sql.strip().lower():
                em_count += 1
        except:
            pred_sql = ""

        # EX (Execution Accuracy)
        try:
            res_pred = db.execute_query(pred_sql)
            res_gt = db.execute_query(ground_truth_sql)
            
            if res_pred is not None and res_gt is not None:
                # Sort both to ensure order doesn't matter
                res_pred = res_pred.sort_values(by="id").reset_index(drop=True)
                res_gt = res_gt.sort_values(by="id").reset_index(drop=True)
                
                if res_pred.equals(res_gt):
                    ex_count += 1
        except Exception:
            pass

    # Compute Metrics
    rouge_results = rouge.compute(predictions=predictions, references=references)
    bleu_results = bleu.compute(predictions=predictions, references=references)
    
    em_score = em_count / len(data) if len(data) > 0 else 0
    ex_score = ex_count / len(data) if len(data) > 0 else 0
    
    print("\n" + "="*40)
    print(f"Evaluation Results")
    print("="*40)
    print(f"File: {os.path.basename(input_file)}")
    print(f"Model: {data[0].get('model_name', 'Unknown')}")
    print("-" * 20)
    print(f"ROUGE-1: {rouge_results['rouge1']:.4f}")
    print(f"ROUGE-2: {rouge_results['rouge2']:.4f}")
    print(f"ROUGE-L: {rouge_results['rougeL']:.4f}")
    print(f"BLEU:    {bleu_results['bleu']:.4f}")
    print("-" * 20)
    print(f"EM (SQL Exact Match):     {em_score:.4f}")
    print(f"EX (Execution Accuracy):  {ex_score:.4f}")
    print("="*40 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Text-to-SQL results JSON file.")
    parser.add_argument("input_file", help="Path to the JSON results file")
    args = parser.parse_args()
    
    evaluate_json(args.input_file)
