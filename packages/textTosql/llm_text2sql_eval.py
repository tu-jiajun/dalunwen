import argparse
import json
import os
import random
import sqlite3
import time

import requests
from tqdm import tqdm


def load_env_key(env_file):
    if not env_file:
        return None
    if not os.path.exists(env_file):
        raise SystemExit(f"Env file not found: {env_file}")
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k in ("ALI_LLM_API_KEY", "DASHSCOPE_API_KEY") and v:
                return v
    return None


def load_tables(tables_file):
    tables = {}
    with open(tables_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            tables[data["id"]] = data["header"]
    return tables


def load_jsonl(path, limit=None, seed=42, shuffle=False):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    if shuffle:
        r = random.Random(seed)
        r.shuffle(rows)
    if limit:
        rows = rows[:limit]
    return rows


def normalize_sql(s):
    s = (s or "").strip().replace(";", "")
    s = " ".join(s.split()).lower()
    return s


def build_messages(question, header, table_name):
    table_str = ", ".join(header)
    system = (
        "You are a Text-to-SQL assistant. Output only one SQL query. No markdown. No explanation. "
        "Always select only the id column. Do not use SELECT *. "
        "Use only the provided table name and columns. "
        "Use 1/0 for boolean conditions. Do not quote numbers."
    )
    user = (
        f"Table name: {table_name}\n"
        f"Columns: {table_str}\n"
        f"Question: {question}\n"
        f"SQL:"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def chat_completion(base_url, api_key, model, messages, timeout=60, max_tokens=256, temperature=0.0, top_p=1.0, retries=5):
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }
    last_err = None
    for i in range(retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if r.status_code >= 500:
                raise RuntimeError(f"ServerError {r.status_code}: {r.text[:500]}")
            if r.status_code >= 400:
                raise RuntimeError(f"ClientError {r.status_code}: {r.text[:500]}")
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            last_err = e
            time.sleep(min(2 ** i, 16))
    raise last_err


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data/Criteria2SQL/data")
    parser.add_argument("--base_url", type=str, default="https://dashscope.aliyuncs.com/compatible-mode/v1")
    parser.add_argument("--model", type=str, default="qwen-max")
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--env_file", type=str, default=None)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--shuffle", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--table_name", type=str, default="records")
    parser.add_argument("--output_file", type=str, default="evaluation_results_llm_qwenmax.json")
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    api_key = (
        args.api_key
        or os.environ.get("ALI_LLM_API_KEY")
        or os.environ.get("DASHSCOPE_API_KEY")
        or load_env_key(args.env_file)
    )
    if not api_key:
        raise SystemExit("Missing api key: set ALI_LLM_API_KEY (or pass --api_key).")

    tables_path = os.path.join(args.data_dir, "test.tables.jsonl")
    test_path = os.path.join(args.data_dir, "test.jsonl")
    tables = load_tables(tables_path)
    test_data = load_jsonl(test_path, limit=args.limit, seed=args.seed, shuffle=args.shuffle)

    db_path = os.path.join(args.data_dir, "test.db")
    conn = sqlite3.connect(db_path) if os.path.exists(db_path) else None

    results = []
    em_correct = 0
    ex_correct = 0

    for eg in tqdm(test_data):
        question = eg["question"]
        table_id = eg["table_id"]
        header = tables.get(table_id, [])
        gold_sql = eg["query"]

        messages = build_messages(question, header, args.table_name)
        try:
            generated_sql = chat_completion(
                base_url=args.base_url,
                api_key=api_key,
                model=args.model,
                messages=messages,
                timeout=args.timeout,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
        except Exception as e:
            generated_sql = ""

        gen_norm = normalize_sql(generated_sql)
        gold_norm = normalize_sql(gold_sql)
        is_em = gen_norm == gold_norm
        if is_em:
            em_correct += 1

        is_ex = False
        if conn and generated_sql:
            try:
                cursor = conn.cursor()
                cursor.execute(gold_sql)
                gold_res = set(cursor.fetchall())
                cursor.execute(generated_sql)
                gen_res = set(cursor.fetchall())
                is_ex = gold_res == gen_res
            except Exception:
                is_ex = False

        if is_ex:
            ex_correct += 1

        results.append(
            {
                "question": question,
                "generated": generated_sql,
                "gold": gold_sql,
                "em": is_em,
                "ex": is_ex,
                "model_name": args.model,
            }
        )

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total = len(results) if results else 1
    print(f"Saved: {args.output_file}")
    print(f"Total: {len(results)}")
    print(f"EM: {em_correct/total:.4f}")
    print(f"EX: {ex_correct/total:.4f}")


if __name__ == "__main__":
    main()
