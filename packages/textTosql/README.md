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
* `evaluate_json.py`: 新版 JSON 结果评估脚本。

## BART 模型训练与测试 (New)

### 1. 为什么直接测试效果很差？
如果您直接使用预训练的 `facebook/bart-base` 模型进行测试，准确率通常为 0。这是因为基础模型没有针对 Text-to-SQL 任务进行微调，它只会简单地复制输入或生成无关内容。**您必须先在数据集上进行训练才能获得有意义的结果。**

### 2. 训练模型
使用 `train_bart.py` 脚本在 Criteria2SQL 数据集上微调 BART 模型。

```bash
# 在 packages/textTosql 目录下，激活虚拟环境后运行
python train_bart.py --base_model facebook/bart-base --epochs 10 --batch_size 8 --output_dir output/bart-text2sql
```

*注意：在 CPU 上训练可能较慢。如果只有 CPU，建议先使用少量数据验证流程，或使用 `--base_model facebook/bart-base` (较小) 而非 large。*

训练完成后，模型权重和 tokenizer 将保存在 `output/bart-text2sql` 目录下。

### 3. 测试模型
使用 `run_bart_eval.py` 脚本评估训练好的模型。

```bash
# 使用刚才训练好的模型路径
python run_bart_eval.py --model_path output/bart-text2sql
```

### 4. 快速验证（使用未微调模型）
如果您只是想测试评估脚本是否工作，可以使用默认的 base 模型（预期准确率为 0）：

```bash
python run_bart_eval.py --model_path facebook/bart-base --limit 100
```

### 参数说明
**train_bart.py**:
- `--base_model`: 基础模型名称 (默认: `facebook/bart-base`)
- `--data_dir`: 数据目录
- `--output_dir`: 输出目录 (默认: `output/bart-text2sql`)
- `--epochs`: 训练轮数 (默认: 3)
- `--batch_size`: 批次大小 (默认: 8)

**run_bart_eval.py**:
- `--model_path`: 模型路径 (可以是本地路径或 HuggingFace ID)
- `--limit`: 测试样本数量限制
