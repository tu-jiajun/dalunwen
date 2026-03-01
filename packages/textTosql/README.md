# Text-to-SQL 评测（小模型 + 大模型）

本 README 仅说明如何在本目录完成 Text-to-SQL 的两类评测：

- 小模型：本地 HuggingFace Seq2Seq 模型微调 + 评测（BART/BioBART/PubMedBART/T5 等）
- 大模型：调用 DashScope OpenAI 兼容接口（qwen-max）生成 SQL + 评测

默认数据集：`data/Criteria2SQL/data`（train/dev/test 与 test.db）。

## 目录

- 小模型（本地微调与评测）
- 大模型（qwen-max 在线评测）
- 指标与输出文件

## 小模型（本地微调与评测）

相关脚本：
- `train_bart.py`：微调任意 Seq2Seq 模型（BART/T5 等）
- `run_bart_eval.py`：对训练好的模型做生成与评测（EM/EX），并保存明细 JSON
- `evaluate_all_metrics.py`：对明细 JSON 计算 ROUGE/BLEU/EM/EX/CMA
- `python ./venv/bin/python`

进入目录：

```bash
cd packages/textTosql
```

### 1) 训练（示例：BART-base）

```bash
python train_bart.py ^
  --base_model facebook/bart-base ^
  --data_dir data/Criteria2SQL/data ^
  --epochs 1 ^
  --batch_size 4 ^
  --output_dir output/bart-text2sql
```

其它可替换模型（示例）：
- `facebook/bart-large`
- `GanjinZero/biobart-base`
- `mse30/bart-base-finetuned-pubmed`
- `google-t5/t5-base`

### 2) 生成与评测（EM/EX + 明细 JSON）

```bash
python run_bart_eval.py ^
  --model_path output/bart-text2sql ^
  --data_dir data/Criteria2SQL/data ^
  --output_file evaluation_results_small.json
```

### 3) 汇总指标（ROUGE/BLEU/EM/EX/CMA）

```bash
python evaluate_all_metrics.py evaluation_results_small.json
```

## 大模型（qwen-max 在线评测）

相关脚本：
- `llm_text2sql_eval.py`：逐条请求 LLM 生成 SQL，计算 EM/EX，并保存明细 JSON

### 1) 准备 API Key

推荐使用环境变量（不要把 Key 写进代码或提交到仓库）：
- `ALI_LLM_API_KEY` 或 `DASHSCOPE_API_KEY`

脚本也支持从后端 `.env` 读取（`--env_file`）。

### 2) 小范围试跑（省 token）

```bash
python llm_text2sql_eval.py ^
  --data_dir data/Criteria2SQL/data ^
  --base_url https://dashscope.aliyuncs.com/compatible-mode/v1 ^
  --model qwen-max ^
  --env_file ..\backend\.env ^
  --limit 20 ^
  --output_file evaluation_results_llm_qwenmax_20.json
```

### 3) 全量 test 跑完（303 条）

不传 `--limit` 或传 `--limit 0` 都表示跑全量 test：

```bash
python llm_text2sql_eval.py ^
  --data_dir data/Criteria2SQL/data ^
  --base_url https://dashscope.aliyuncs.com/compatible-mode/v1 ^
  --model qwen-max ^
  --env_file ..\backend\.env ^
  --limit 0 ^
  --output_file evaluation_results_llm_qwenmax_all.json
```

跑完后同样可以用统一脚本汇总指标：

```bash
python evaluate_all_metrics.py evaluation_results_llm_qwenmax_all.json
```

## 指标与输出文件

- `run_bart_eval.py` / `llm_text2sql_eval.py` 输出明细 JSON：包含 `generated/gold/em/ex`
- `evaluate_all_metrics.py` 读取明细 JSON，计算并打印：
  - ROUGE-1 / ROUGE-2 / ROUGE-L
  - BLEU（sacrebleu）
  - EM（规范化后完全一致）
  - EX（执行结果一致，需要 `test.db`）
  - CMA（脚本内定义的一致性指标）

## 评测结果（test=303）

下表为同一数据集 test 集（303 条）上的对比结果。

小模型（BART 系列）说明：
- 使用 `train_bart.py` 微调后再用 `run_bart_eval.py` 评测
- 本次对比的微调采用相同训练预算：`epochs=1` 且 `max_steps=200`

大模型（qwen-max）说明：
- 使用 `llm_text2sql_eval.py` 在线生成 SQL 后评测

| 模型 | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU | EM | EX | CMA |
|---|---:|---:|---:|---:|---:|---:|---:|
| BART-base (facebook/bart-base) | 0.8517 | 0.8013 | 0.8421 | 0.5143 | 0.3795 | 0.4092 | 0.3795 |
| BART-large (facebook/bart-large) | 0.8709 | 0.8364 | 0.8635 | 0.5596 | 0.4950 | 0.5347 | 0.4950 |
| BioBART (GanjinZero/biobart-base) | 0.8584 | 0.8139 | 0.8531 | 0.5343 | 0.4224 | 0.4488 | 0.4224 |
| PubMedBART (mse30/bart-base-finetuned-pubmed) | 0.8719 | 0.8297 | 0.8661 | 0.5534 | 0.4290 | 0.4455 | 0.4290 |
| qwen-max（LLM） | 0.9144 | 0.8614 | 0.9038 | 0.0356 | 0.4719 | 0.5545 | 0.4851 |

对应明细文件（JSON）示例：
- qwen-max：`evaluation_results_llm_qwenmax_all_v2.json`
