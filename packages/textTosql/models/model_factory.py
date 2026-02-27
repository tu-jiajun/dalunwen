import os

# Set HF mirror for faster downloads in China
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from transformers import (
    BartForConditionalGeneration, BartTokenizer,
    T5ForConditionalGeneration, T5Tokenizer,
    GPT2LMHeadModel, GPT2Tokenizer,
    BertTokenizer, EncoderDecoderModel,
    AutoTokenizer, AutoModelForSeq2SeqLM,
    TapasForQuestionAnswering, TapasTokenizer
)
import torch

def get_model(model_name):
    model_name = model_name.lower()
    
    # 1. GPT-2 (Causal LM)
    if "gpt2" in model_name:
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        return model, tokenizer
        
    # 2. T5-small (Seq2Seq)
    elif "t5-small" in model_name:
        tokenizer = T5Tokenizer.from_pretrained("t5-small")
        model = T5ForConditionalGeneration.from_pretrained("t5-small")
        return model, tokenizer
        
    # 3. T5-base (Seq2Seq)
    elif "t5-base" in model_name:
        tokenizer = T5Tokenizer.from_pretrained("t5-base")
        model = T5ForConditionalGeneration.from_pretrained("t5-base")
        return model, tokenizer
        
    # 4. BioBERT (Encoder -> Seq2Seq via EncoderDecoderModel)
    elif "biobert" in model_name:
        # Using dmis-lab/biobert-base-cased-v1.2
        tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.2")
        # Initialize BERT2BERT
        model = EncoderDecoderModel.from_encoder_decoder_pretrained(
            "dmis-lab/biobert-base-cased-v1.2", 
            "dmis-lab/biobert-base-cased-v1.2"
        )
        # Set special tokens for generation
        model.config.decoder_start_token_id = tokenizer.cls_token_id
        model.config.pad_token_id = tokenizer.pad_token_id
        model.config.vocab_size = model.config.decoder.vocab_size
        return model, tokenizer
        
    # 5. ClinicalBERT (Encoder -> Seq2Seq via EncoderDecoderModel)
    elif "clinicalbert" in model_name:
        # Using emilyalsentzer/Bio_ClinicalBERT
        tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
        model = EncoderDecoderModel.from_encoder_decoder_pretrained(
            "emilyalsentzer/Bio_ClinicalBERT", 
            "emilyalsentzer/Bio_ClinicalBERT"
        )
        model.config.decoder_start_token_id = tokenizer.cls_token_id
        model.config.pad_token_id = tokenizer.pad_token_id
        model.config.vocab_size = model.config.decoder.vocab_size
        return model, tokenizer

    # 6. TAPAS (Table QA)
    elif "tapas" in model_name:
        # Warning: TAPAS is typically for Table QA, not text-to-SQL generation.
        # We load it here as requested, but it might require specific input formatting (tables).
        # We'll use google/tapas-base-finetuned-wikisql-supervised for relevance.
        tokenizer = TapasTokenizer.from_pretrained("google/tapas-base-finetuned-wikisql-supervised")
        model = TapasForQuestionAnswering.from_pretrained("google/tapas-base-finetuned-wikisql-supervised")
        return model, tokenizer
        
    # 7. BART-large-CNN (Seq2Seq)
    elif "bart" in model_name:
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
        model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        return model, tokenizer
        
    else:
        # Default fallback
        print(f"Warning: Model {model_name} not explicitly handled, trying AutoModel...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            return model, tokenizer
        except:
            raise ValueError(f"Unsupported model: {model_name}")
