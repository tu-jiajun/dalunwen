import json
import os
import evaluate as hf_evaluate

# 使用国内镜像加速下载
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import pandas as pd
from datasets import load_dataset
from transformers import BartForConditionalGeneration, BartTokenizer
from utils.db_utils import MockDB
from utils.converter import structured_to_sql

class Evaluator:
    def __init__(self, model_path="results", test_data_path="data/test.json"):
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model = BartForConditionalGeneration.from_pretrained(model_path)
        self.test_data = load_dataset("json", data_files={"test": test_data_path})["test"]
        self.db = MockDB()

    def evaluate(self):
        # 使用 evaluate.load 的替代方案：直接实例化
        # 注意：evaluate.load() 是加载 metric 的标准方法，如果它不存在，说明 evaluate 安装有问题
        # 或者有同名文件 evaluate.py 导致冲突。
        # 我们这里尝试直接 import 具体的 metric 类（虽然 evaluate 库通常不这样用）
        # 或者更可能的：当前目录下有名为 evaluate.py 的文件吗？
        # 检查 sys.modules
        
        # 再次尝试最标准的加载方式，但打印调试信息
        print(f"Evaluate file: {hf_evaluate.__file__}")
        try:
            rouge = hf_evaluate.load("rouge")
            bleu = hf_evaluate.load("bleu")
        except AttributeError:
            # 如果真的没有 load，可能是版本问题，但 0.4.x 应该有。
            # 这里的 fallback 是使用本地计算或其他库，但为保持一致性，我们尝试重新 reload
            import importlib
            importlib.reload(hf_evaluate)
            rouge = hf_evaluate.load("rouge")
            bleu = hf_evaluate.load("bleu")
        
        predictions = []
        references = []
        
        em_count = 0
        ex_count = 0
        
        for example in self.test_data:
            input_text = example["text"]
            ground_truth_structured = example["structured"]
            ground_truth_sql = example["sql"]
            
            # Generate structured output
            inputs = self.tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
            outputs = self.model.generate(inputs["input_ids"], max_length=128, num_beams=4, early_stopping=True)
            pred_structured = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            predictions.append(pred_structured)
            references.append(ground_truth_structured)
            
            # EM (Exact Match) for SQL
            # Convert structured to SQL
            try:
                pred_sql = structured_to_sql(pred_structured)
                # Normalize SQL (simple lower case and space stripping for mock)
                if pred_sql.strip().lower() == ground_truth_sql.strip().lower():
                    em_count += 1
            except:
                pred_sql = ""

            # EX (Execution Accuracy)
            try:
                res_pred = self.db.execute_query(pred_sql)
                res_gt = self.db.execute_query(ground_truth_sql)
                
                if res_pred is not None and res_gt is not None:
                    # Sort both to ensure order doesn't matter
                    res_pred = res_pred.sort_values(by="id").reset_index(drop=True)
                    res_gt = res_gt.sort_values(by="id").reset_index(drop=True)
                    
                    if res_pred.equals(res_gt):
                        ex_count += 1
            except Exception as e:
                pass
                
        # Compute Metrics
        rouge_results = rouge.compute(predictions=predictions, references=references)
        bleu_results = bleu.compute(predictions=predictions, references=references)
        
        em_score = em_count / len(self.test_data)
        ex_score = ex_count / len(self.test_data)
        
        print(f"ROUGE-1: {rouge_results['rouge1']:.4f}")
        print(f"ROUGE-2: {rouge_results['rouge2']:.4f}")
        print(f"ROUGE-L: {rouge_results['rougeL']:.4f}")
        print(f"BLEU: {bleu_results['bleu']:.4f}")
        print(f"EM (SQL Exact Match): {em_score:.4f}")
        print(f"EX (Execution Accuracy): {ex_score:.4f}")

if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate()
