import os
import sys

# Set HF mirror for faster downloads in China
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# Add parent directory to path to import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from models.unified_trainer import UnifiedTrainer

def main():
    # Use t5-base for better performance on complex Spider SQLs
    model_name = "t5-base" 
    
    # Custom output directories for Spider experiment
    output_dir = os.path.join(parent_dir, "results_spider_medical")
    data_dir = os.path.join(parent_dir, "data", "spider_medical")
    
    train_path = os.path.join(data_dir, "train.json")
    val_path = os.path.join(data_dir, "validation.json")
    test_path = os.path.join(data_dir, "test.json")
    
    # Ensure data exists
    if not os.path.exists(train_path):
        print(f"Error: Data not found at {data_dir}")
        print("Please run 'python data/process_spider_medical.py' first.")
        return

    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Initializing trainer for {model_name} on Spider Medical data...")
    trainer = UnifiedTrainer(model_name, output_dir)
    
    # Train
    # Increase epochs slightly as Spider data is harder but smaller
    trainer.train(train_path, val_path, epochs=5, batch_size=4)
    
    # Generate JSON
    output_json_path = os.path.join(output_dir, f"{model_name}_results.json")
    trainer.generate_json(test_path, output_json_path)

    # Evaluate
    # Note: Our standard 'evaluate_json.py' uses a MockDB which won't work for Spider SQLs
    # because Spider SQLs reference tables that don't exist in our simple MockDB.
    # So we only calculate text metrics (ROUGE/BLEU) here.
    print("\nStarting evaluation (Text Metrics Only)...")
    try:
        from evaluate_json import evaluate_json
        # We might need to suppress EX/EM execution or accept they will be 0
        evaluate_json(output_json_path)
    except ImportError:
        sys.path.append(parent_dir)
        from evaluate_json import evaluate_json
        evaluate_json(output_json_path)

if __name__ == "__main__":
    main()
