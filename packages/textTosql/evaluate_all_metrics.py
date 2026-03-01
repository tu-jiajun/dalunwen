import argparse
import json
import os
import re

import sacrebleu
import sqlparse
from rouge_score import rouge_scorer
from sqlparse.sql import Where


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_sql(s):
    s = (s or "").strip().replace(";", "")
    s = " ".join(s.split()).lower()
    return s


def canonical_sql(sql):
    sql = normalize_sql(sql)
    if not sql:
        return None
    stmts = sqlparse.parse(sql)
    if not stmts:
        return None
    stmt = stmts[0]

    from_seen = False
    select_seen = False
    select_parts = []
    from_parts = []
    for tok in stmt.tokens:
        if tok.is_whitespace:
            continue
        t = tok.value.lower().strip()
        if t == "select":
            select_seen = True
            continue
        if t == "from":
            from_seen = True
            select_seen = False
            continue
        if isinstance(tok, Where):
            break
        if select_seen:
            select_parts.append(tok.value)
        if from_seen:
            from_parts.append(tok.value)

    select_text = normalize_sql(" ".join(select_parts))
    from_text = normalize_sql(" ".join(from_parts))
    from_text = from_text.split()[0] if from_text else ""

    where = None
    for tok in stmt.tokens:
        if isinstance(tok, Where):
            where = tok
            break

    conds = []
    if where is not None:
        parts = []
        current = []
        for tok in where.tokens:
            if tok.is_whitespace:
                continue
            t = tok.value.lower().strip()
            if t == "where":
                continue
            if t == "or":
                return None
            if t == "and":
                if current:
                    parts.append(" ".join(current))
                    current = []
                continue
            if "(" in t or ")" in t:
                return None
            current.append(tok.value)
        if current:
            parts.append(" ".join(current))

        for p in parts:
            p = normalize_sql(p)
            m = re.match(r"^([a-z0-9_\.]+)\s*(=|>=|<=|<>|>|<)\s*(.+)$", p)
            if not m:
                return None
            col, op, val = m.group(1), m.group(2), m.group(3)
            val = val.strip().strip("'").strip('"')
            conds.append((col, op, val))

    conds = tuple(sorted(conds))
    return (select_text, from_text, conds)


def rouge_scores(preds, refs):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    r1 = 0.0
    r2 = 0.0
    rl = 0.0
    n = len(preds)
    for p, r in zip(preds, refs):
        s = scorer.score(r, p)
        r1 += s["rouge1"].fmeasure
        r2 += s["rouge2"].fmeasure
        rl += s["rougeL"].fmeasure
    if n == 0:
        return 0.0, 0.0, 0.0
    return r1 / n, r2 / n, rl / n


def bleu_score(preds, refs):
    score = sacrebleu.corpus_bleu(preds, [refs], tokenize="none").score
    return score / 100.0, score


def mean_bool(items, key):
    vals = [1.0 if x.get(key) else 0.0 for x in items]
    return sum(vals) / len(vals) if vals else 0.0


def cma_score(items):
    matches = []
    for x in items:
        p = canonical_sql(x.get("generated", ""))
        r = canonical_sql(x.get("gold", ""))
        if p is None or r is None:
            matches.append(1.0 if normalize_sql(x.get("generated", "")) == normalize_sql(x.get("gold", "")) else 0.0)
        else:
            matches.append(1.0 if p == r else 0.0)
    return sum(matches) / len(matches) if matches else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to evaluation_results.json")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise SystemExit(f"File not found: {args.input_file}")

    data = load_json(args.input_file)
    preds = [str(x.get("generated", "") or "") for x in data]
    refs = [str(x.get("gold", "") or "") for x in data]

    rouge1, rouge2, rougeL = rouge_scores(preds, refs)
    bleu, bleu_100 = bleu_score(preds, refs)
    em = mean_bool(data, "em")
    ex = mean_bool(data, "ex")
    cma = cma_score(data)

    print(f"File: {os.path.basename(args.input_file)}")
    print(f"Count: {len(data)}")
    print(f"ROUGE-1: {rouge1:.4f}")
    print(f"ROUGE-2: {rouge2:.4f}")
    print(f"ROUGE-L: {rougeL:.4f}")
    print(f"BLEU: {bleu:.4f} (sacrebleu={bleu_100:.4f})")
    print(f"EM: {em:.4f}")
    print(f"EX: {ex:.4f}")
    print(f"CMA: {cma:.4f}")


if __name__ == "__main__":
    main()
