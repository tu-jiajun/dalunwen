import torch
import os

# 使用国内镜像加速下载
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from transformers import BartForConditionalGeneration, BartTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import os

class BartSemanticParser:
    def __init__(self, model_name="facebook/bart-base", output_dir="./results"):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.output_dir = output_dir

    def preprocess_function(self, examples):
        # Input: Natural Language Text
        inputs = examples["text"]
        # Target: Structured Representation (JSON string)
        targets = examples["structured"]
        
        model_inputs = self.tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
        
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(targets, max_length=128, truncation=True, padding="max_length")

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def train(self, train_path, val_path, epochs=3):
        dataset = load_dataset("json", data_files={"train": train_path, "validation": val_path})
        tokenized_datasets = dataset.map(self.preprocess_function, batched=True)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=epochs,
            weight_decay=0.01,
            save_total_limit=2,
            logging_dir='./logs',
            report_to="none" # Disable wandb/tensorboard for simplicity
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["validation"],
        )

        print("Starting training...")
        trainer.train()
        print("Training complete.")
        
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)

    def generate(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", max_length=128, truncation=True)
        # Move inputs to same device as model
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        outputs = self.model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Ensure data exists
    if not os.path.exists("data/train.json"):
        print("Data not found. Please run data/generate_mock_data.py first.")
        exit(1)
        
    parser = BartSemanticParser()
    parser.train("data/train.json", "data/validation.json", epochs=5) # Use 5 epoch for demo
