# 临床试验 Text-to-SQL 复现

本包在合成数据集上（模仿 UW BioNLP ClinicalTrials.gov 数据集）使用多种开源模型（BART, T5, GPT-2, BERT等）复现了 Text-to-SQL 实验。

## 概述

1. **语义解析（第一阶段）**：将自然语言标准转换为结构化表示（JSON）。
2. **SQL 生成（第二阶段）**：将结构化表示转换为 SQL 查询。
3. **评估**：
   * **ROUGE/BLEU**：衡量语义解析的准确性。
   * **EM（精确匹配）**：衡量 SQL 语法的正确性。
   * **EX（执行准确率）**：衡量在模拟数据库上的查询结果正确性。

## 安装与运行

1. 创建虚拟环境并安装依赖：

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. 生成合成数据（由于原始数据受限）：

   ```bash
   # python ./venv/bin/python 
   ./venv/bin/python data/generate_mock_data.py
   ```

## 支持的开源模型

您可以使用以下脚本训练和评估不同的模型：

* `python models/run_gpt2.py`
* `python models/run_t5_small.py`
* `python models/run_t5_base.py`
* `python models/run_biobert.py`
* `python models/run_clinicalbert.py`
* `python models/run_bart_large_cnn.py`
* `python models/run_tapas.py` (仅加载，不进行标准 Text-to-SQL 训练)

## 评估结果

运行上述脚本后，会在 `results/` 目录下生成 `<model_name>_results.json` 文件。
您可以使用以下命令计算详细的分数（ROUGE, BLEU, EM, EX）：

```bash
# 例如评估 GPT-2 的结果
python evaluate_json.py results/gpt2_results.json
```

## 目录结构

* `data/`：包含生成的数据集。
* `models/`：
    * `unified_trainer.py`: 统一训练器。
    * `model_factory.py`: 模型工厂。
    * `run_*.py`: 各个模型的执行脚本。
* `utils/`：数据库和转换的辅助函数。
* `run_evaluation.py`：旧版评估脚本。
* `evaluate_json.py`: 新版 JSON 结果评估脚本。
