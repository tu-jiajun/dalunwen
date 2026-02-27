import os
import sys

# Set HF mirror for faster downloads in China (Must be before importing transformers)
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# Add parent directory to path to import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from models.unified_trainer import UnifiedTrainer

def main():
    model_name = "t5-small"
    output_dir = os.path.join(parent_dir, "results")
    data_dir = os.path.join(parent_dir, "data")
    
    train_path = os.path.join(data_dir, "train.json")
    val_path = os.path.join(data_dir, "validation.json")
    test_path = os.path.join(data_dir, "test.json")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Initializing trainer for {model_name}...")
    trainer = UnifiedTrainer(model_name, output_dir)
    
    # Train
    trainer.train(train_path, val_path)
    
    # Generate JSON
    output_json_path = os.path.join(output_dir, f"{model_name}_results.json")
    trainer.generate_json(test_path, output_json_path)

    # Evaluate
    print("\nStarting evaluation...")
    try:
        from evaluate_json import evaluate_json
    except ImportError:
        sys.path.append(parent_dir)
        from evaluate_json import evaluate_json
    
    evaluate_json(output_json_path)

if __name__ == "__main__":
    main()
