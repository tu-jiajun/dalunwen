import torch
from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq, DataCollatorForLanguageModeling, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset
from .model_factory import get_model
import json
import os

class UnifiedTrainer:
    def __init__(self, model_name, output_dir="./results"):
        self.model_name = model_name
        print(f"Loading model: {model_name}...")
        self.model, self.tokenizer = get_model(model_name)
        self.output_dir = output_dir
        
        # Determine model type for data processing
        self.is_causal_lm = "gpt2" in model_name.lower()
        self.is_tapas = "tapas" in model_name.lower()

    def preprocess_function(self, examples):
        # Handle Causal LM (GPT-2)
        if self.is_causal_lm:
            # Correcting access to examples
            # examples["text"] is a list of strings
            formatted_inputs = [f"{t} -> {s}" for t, s in zip(examples["text"], examples["structured"])]
            model_inputs = self.tokenizer(formatted_inputs, max_length=128, truncation=True, padding="max_length")
            model_inputs["labels"] = model_inputs["input_ids"].copy()
            return model_inputs
            
        # Handle Seq2Seq (T5, BART, BERT2BERT)
        elif not self.is_tapas:
            inputs = self.tokenizer(examples["text"], max_length=128, truncation=True, padding="max_length")
            # Setup the tokenizer for targets
            # Check if tokenizer has as_target_tokenizer (older transformers) or use tokenizer directly (newer transformers)
            if hasattr(self.tokenizer, "as_target_tokenizer"):
                with self.tokenizer.as_target_tokenizer():
                    labels = self.tokenizer(examples["structured"], max_length=128, truncation=True, padding="max_length")
            else:
                # For newer transformers (e.g. T5TokenizerFast), just use tokenizer for targets too
                labels = self.tokenizer(text_target=examples["structured"], max_length=128, truncation=True, padding="max_length")
                
            inputs["labels"] = labels["input_ids"]
            return inputs
            
        else:
            # TAPAS typically requires table data. 
            # For this text-to-sql generation task, we might be limited.
            # We return basic tokenization to avoid crash during mapping
            return self.tokenizer(examples["text"], truncation=True, padding="max_length")

    def train(self, train_path, val_path, epochs=5, batch_size=8):
        if self.is_tapas:
            print(f"Skipping training for {self.model_name} as it is a Table QA model and standard Seq2Seq training is not supported here.")
            return

        print(f"Starting training for {self.model_name}...")
        # Load dataset
        dataset = load_dataset("json", data_files={"train": train_path, "validation": val_path})
        
        # Tokenize
        tokenized_datasets = dataset.map(self.preprocess_function, batched=True)
        
        # Data Collator
        if self.is_causal_lm:
            data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)
            training_args = TrainingArguments(
                output_dir=f"{self.output_dir}/{self.model_name}",
                evaluation_strategy="epoch",
                learning_rate=2e-5,
                per_device_train_batch_size=batch_size,
                per_device_eval_batch_size=batch_size,
                num_train_epochs=epochs,
                weight_decay=0.01,
                save_total_limit=2,
                logging_dir='./logs',
                report_to="none"
            )
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=tokenized_datasets["train"],
                eval_dataset=tokenized_datasets["validation"],
                data_collator=data_collator
            )
        else:
            data_collator = DataCollatorForSeq2Seq(tokenizer=self.tokenizer, model=self.model)
            training_args = Seq2SeqTrainingArguments(
                output_dir=f"{self.output_dir}/{self.model_name}",
                evaluation_strategy="epoch",
                learning_rate=2e-5,
                per_device_train_batch_size=batch_size,
                per_device_eval_batch_size=batch_size,
                num_train_epochs=epochs,
                weight_decay=0.01,
                save_total_limit=2,
                logging_dir='./logs',
                report_to="none",
                predict_with_generate=True
            )
            trainer = Seq2SeqTrainer(
                model=self.model,
                args=training_args,
                train_dataset=tokenized_datasets["train"],
                eval_dataset=tokenized_datasets["validation"],
                data_collator=data_collator
            )
        
        trainer.train()
        
        # Save model
        save_path = f"{self.output_dir}/{self.model_name}"
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
        print(f"Model saved to {save_path}")

    def generate_json(self, test_path, output_json_path):
        dataset = load_dataset("json", data_files={"test": test_path})["test"]
        results = []
        
        print(f"Generating results for {self.model_name}...")
        
        # Move model to device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)
        
        # Batch generation for speed up
        batch_size = 8
        
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            input_texts = batch["text"]
            
            if self.is_causal_lm:
                # Causal LM generation (processing one by one for now to keep logic simple, but can be batched)
                for j, input_text in enumerate(input_texts):
                    input_ids = self.tokenizer.encode(f"{input_text} ->", return_tensors="pt").to(device)
                    pad_token_id = self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None else self.tokenizer.eos_token_id
                    attention_mask = (input_ids != pad_token_id).long()
                    
                    outputs = self.model.generate(
                        input_ids, 
                        attention_mask=attention_mask,
                        max_length=128, 
                        num_beams=4, 
                        early_stopping=True,
                        pad_token_id=pad_token_id
                    )
                    generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    if "->" in generated_text:
                        pred_structured = generated_text.split("->")[-1].strip()
                    else:
                        pred_structured = generated_text
                    
                    results.append({
                        "model_name": self.model_name,
                        "input_text": input_text,
                        "ground_truth_structured": batch["structured"][j],
                        "ground_truth_sql": batch.get("sql", [""]*len(batch))[j],
                        "pred_structured": pred_structured
                    })
                    
            elif self.is_tapas:
                 for j, input_text in enumerate(input_texts):
                    results.append({
                        "model_name": self.model_name,
                        "input_text": input_text,
                        "ground_truth_structured": batch["structured"][j],
                        "ground_truth_sql": batch.get("sql", [""]*len(batch))[j],
                        "pred_structured": "TAPAS_GENERATION_NOT_SUPPORTED"
                    })
                 
            else:
                # Seq2Seq Batch Generation
                inputs = self.tokenizer(input_texts, return_tensors="pt", max_length=128, truncation=True, padding=True).to(device)
                outputs = self.model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
                decoded_preds = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
                
                for j, pred_structured in enumerate(decoded_preds):
                    results.append({
                        "model_name": self.model_name,
                        "input_text": input_texts[j],
                        "ground_truth_structured": batch["structured"][j],
                        "ground_truth_sql": batch.get("sql", [""]*len(batch))[j] if "sql" in batch else "",
                        "pred_structured": pred_structured
                    })
            
            print(f"Processed {i + len(batch)} / {len(dataset)} samples")
            
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_json_path}")
