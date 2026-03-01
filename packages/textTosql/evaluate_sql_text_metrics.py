import argparse
import json
import os

import sacrebleu
from rouge_score import rouge_scorer


def load_pairs(path, pred_key, ref_key):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    preds = [str(x.get(pred_key, "") or "") for x in data]
    refs = [str(x.get(ref_key, "") or "") for x in data]
    return preds, refs


def compute(preds, refs):
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    rouge_l_f = 0.0
    n = len(preds)
    for p, r in zip(preds, refs):
        rouge_l_f += scorer.score(r, p)["rougeL"].fmeasure
    rouge_l_f = rouge_l_f / n if n else 0.0
    bleu = sacrebleu.corpus_bleu(preds, [refs], tokenize="none").score
    return rouge_l_f, bleu


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to JSON file")
    parser.add_argument("--pred_key", default="generated")
    parser.add_argument("--ref_key", default="gold")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise SystemExit(f"File not found: {args.input_file}")

    preds, refs = load_pairs(args.input_file, args.pred_key, args.ref_key)
    rouge_l_f, bleu = compute(preds, refs)

    print(f"File: {os.path.basename(args.input_file)}")
    print(f"Count: {len(preds)}")
    print(f"ROUGE-L(F1): {rouge_l_f:.4f}")
    print(f"BLEU: {bleu:.4f}")


if __name__ == '__main__':
    main()
