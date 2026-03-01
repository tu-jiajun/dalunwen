import argparse
import json
import os
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset

def load_tables(tables_file):
    tables = {}
    with open(tables_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            tables[data['id']] = data['header']
    return tables

def load_dataset(data_file, tables):
    data = []
    with open(data_file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            table_id = entry['table_id']
            question = entry['question']
            query = entry['query']
            
            header = tables.get(table_id, [])
            table_str = ", ".join(header)
            
            # Input format: Question: ... Table: ...
            input_text = f"Question: {question} Table: {table_str}"
            
            data.append({
                "input_text": input_text,
                "target_text": query
            })
    return data

def train_simple(model, train_dataset, data_collator, args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, foreach=False)
    loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, collate_fn=data_collator)
    step = 0
    for _ in range(args.epochs):
        for batch in loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            loss = model(**batch).loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            step += 1
            if args.max_steps and step >= args.max_steps:
                return

def train(args):
    # Check output dir
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Load data
    print("Loading tables...")
    tables_path = os.path.join(args.data_dir, "train.tables.jsonl")
    tables = load_tables(tables_path)
    
    print("Loading training data...")
    train_data_path = os.path.join(args.data_dir, "train.jsonl")
    train_data = load_dataset(train_data_path, tables)
    if args.limit:
        train_data = train_data[:args.limit]
    
    # Optional: Load dev data for evaluation
    dev_data = []
    dev_data_path = os.path.join(args.data_dir, "dev.jsonl")
    dev_tables_path = os.path.join(args.data_dir, "dev.tables.jsonl")
    if os.path.exists(dev_data_path) and os.path.exists(dev_tables_path):
        print("Loading dev data...")
        dev_tables = load_tables(dev_tables_path)
        dev_data = load_dataset(dev_data_path, dev_tables)
        if args.limit:
            dev_data = dev_data[:args.limit]
    
    # Create Datasets
    train_dataset = Dataset.from_list(train_data)
    eval_dataset = Dataset.from_list(dev_data) if dev_data else None
    
    # Tokenizer
    print(f"Loading tokenizer from {args.base_model}...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    
    def preprocess_function(examples):
        inputs = examples["input_text"]
        targets = examples["target_text"]
        
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        labels = tokenizer(text_target=targets, max_length=128, truncation=True)
            
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    print("Preprocessing data...")
    train_dataset = train_dataset.map(preprocess_function, batched=True)
    train_dataset = train_dataset.remove_columns(["input_text", "target_text"])
    if eval_dataset:
        eval_dataset = eval_dataset.map(preprocess_function, batched=True)
        eval_dataset = eval_dataset.remove_columns(["input_text", "target_text"])
        
    # Model
    print(f"Loading model from {args.base_model}...")
    model = AutoModelForSeq2SeqLM.from_pretrained(args.base_model)
    
    # Training Arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        predict_with_generate=True,
        num_train_epochs=args.epochs,
        logging_dir=f"{args.output_dir}/logs",
        logging_steps=100,
        save_strategy="epoch",
        evaluation_strategy="epoch" if eval_dataset else "no",
        learning_rate=args.learning_rate,
        save_total_limit=2,
        fp16=torch.cuda.is_available(), # Use mixed precision if GPU available
        push_to_hub=False,
    )
    
    # Data Collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    # Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    # Train
    print("Starting training...")
    try:
        trainer.train()
    except Exception as e:
        print(f"Trainer failed ({type(e).__name__}: {e}). Falling back to simple training loop.")
        train_simple(model, train_dataset, data_collator, args)
    
    # Save final model
    print(f"Saving model to {args.output_dir}...")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Training complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_model", type=str, default="facebook/bart-base", help="Base model to fine-tune")
    parser.add_argument("--data_dir", type=str, default="/Users/hexiapeng/Documents/Git/dalunwen/packages/textTosql/data/Criteria2SQL/data", help="Path to data directory")
    parser.add_argument("--output_dir", type=str, default="output/bart-text2sql", help="Directory to save trained model")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of training/dev examples for quick test")
    parser.add_argument("--max_steps", type=int, default=None, help="Max training steps for quick test")
    
    args = parser.parse_args()
    train(args)
