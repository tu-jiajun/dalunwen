import argparse
import json
import sqlite3
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from tqdm import tqdm
import os

def load_tables(tables_file):
    tables = {}
    with open(tables_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            tables[data['id']] = data['header']
    return tables

def evaluate(args):
    # Load tables
    print("Loading tables...")
    tables_path = os.path.join(args.data_dir, "test.tables.jsonl")
    if not os.path.exists(tables_path):
        print(f"Error: {tables_path} not found.")
        return
    tables = load_tables(tables_path)
    
    # Load test data
    print("Loading test data...")
    test_data_path = os.path.join(args.data_dir, "test.jsonl")
    if not os.path.exists(test_data_path):
        print(f"Error: {test_data_path} not found.")
        return
        
    test_data = []
    with open(test_data_path, 'r') as f:
        for line in f:
            test_data.append(json.loads(line))
            
    if args.limit:
        test_data = test_data[:args.limit]
        
    # Load model
    print(f"Loading model from {args.model_path}...")
    try:
        tokenizer = BartTokenizer.from_pretrained(args.model_path)
        model = BartForConditionalGeneration.from_pretrained(args.model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    model.eval()
    
    # Connect to DB for execution evaluation
    db_path = os.path.join(args.data_dir, "test.db")
    conn = None
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
    else:
        print(f"Warning: {db_path} not found. Execution accuracy will be skipped.")
    
    em_correct = 0
    ex_correct = 0
    total = 0
    
    results = []
    
    print("Starting evaluation...")
    for example in tqdm(test_data):
        total += 1
        question = example['question']
        table_id = example['table_id']
        header = tables.get(table_id, [])
        
        # Format input (Generic format, adjust if user's model differs)
        # Format: "Question: ... Table: col1, col2, ..."
        table_str = ", ".join(header)
        input_text = f"Question: {question} Table: {table_str}"
        
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=128)
            
        generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
        gold_sql = example['query']
        
        # Exact Match
        # Normalize simple spacing and case
        gen_norm = " ".join(generated_sql.split()).lower().strip().replace(";", "")
        gold_norm = " ".join(gold_sql.split()).lower().strip().replace(";", "")
        
        is_em = gen_norm == gold_norm
        if is_em:
            em_correct += 1
            
        # Execution Match
        is_ex = False
        if conn:
            try:
                cursor = conn.cursor()
                # Run gold
                cursor.execute(gold_sql)
                gold_res = set(cursor.fetchall())
                
                # Run generated
                cursor.execute(generated_sql)
                gen_res = set(cursor.fetchall())
                
                is_ex = gold_res == gen_res
            except Exception as e:
                # print(f"Execution error: {e}")
                is_ex = False
            
        if is_ex:
            ex_correct += 1
            
        results.append({
            "question": question,
            "generated": generated_sql,
            "gold": gold_sql,
            "em": is_em,
            "ex": is_ex
        })
        
    print(f"Total: {total}")
    print(f"Exact Match Accuracy: {em_correct/total:.4f}")
    if conn:
        print(f"Execution Accuracy: {ex_correct/total:.4f}")
    
    # Save detailed results
    output_file = "evaluation_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Detailed results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="facebook/bart-base", help="Path to the BART model or HuggingFace model name")
    parser.add_argument("--data_dir", type=str, default="/Users/hexiapeng/Documents/Git/dalunwen/packages/textTosql/data/Criteria2SQL/data", help="Path to data directory")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of examples for quick test")
    args = parser.parse_args()
    evaluate(args)
