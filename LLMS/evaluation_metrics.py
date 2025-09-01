"""
LLM Evaluation Metrics: BLEU, ROUGE, and Perplexity
This script evaluates LLM performance on text generation tasks.
"""

import torch
import math
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from rouge_score import rouge_scorer
import nltk
import logging
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMEvaluator:
    def __init__(self, model_name='gpt2'):
        """Initialize the evaluator with a language model."""
        logger.info(f"Loading model for evaluation: {model_name}")
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Initialize ROUGE scorer
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'], 
            use_stemmer=True
        )
        
        logger.info("Model and evaluators loaded successfully!")
    
    def calculate_perplexity(self, text):
        """Calculate perplexity of the given text."""
        try:
            # Encode the text
            encodings = self.tokenizer(text, return_tensors='pt')
            
            # Calculate loss
            with torch.no_grad():
                outputs = self.model(**encodings, labels=encodings['input_ids'])
                loss = outputs.loss
                
            # Calculate perplexity
            perplexity = torch.exp(loss).item()
            return perplexity
            
        except Exception as e:
            logger.error(f"Error calculating perplexity: {e}")
            return None
    
    def calculate_bleu_score(self, reference, candidate):
        """Calculate BLEU score between reference and candidate text."""
        try:
            # Tokenize the sentences
            reference_tokens = [reference.split()]  # List of lists for sentence_bleu
            candidate_tokens = candidate.split()
            
            # Calculate BLEU score
            bleu_score = sentence_bleu(reference_tokens, candidate_tokens)
            return bleu_score
            
        except Exception as e:
            logger.error(f"Error calculating BLEU score: {e}")
            return None
    
    def calculate_rouge_scores(self, reference, candidate):
        """Calculate ROUGE scores between reference and candidate text."""
        try:
            scores = self.rouge_scorer.score(reference, candidate)
            
            # Extract F1 scores
            rouge_scores = {
                'rouge1': scores['rouge1'].fmeasure,
                'rouge2': scores['rouge2'].fmeasure,
                'rougeL': scores['rougeL'].fmeasure
            }
            
            return rouge_scores
            
        except Exception as e:
            logger.error(f"Error calculating ROUGE scores: {e}")
            return None
    
    def evaluate_text_generation(self, prompt, reference_text, generated_text):
        """Comprehensive evaluation of generated text."""
        results = {
            'prompt': prompt,
            'reference': reference_text,
            'generated': generated_text,
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate perplexity of generated text
        perplexity = self.calculate_perplexity(generated_text)
        results['perplexity'] = perplexity
        
        # Calculate BLEU score
        bleu_score = self.calculate_bleu_score(reference_text, generated_text)
        results['bleu_score'] = bleu_score
        
        # Calculate ROUGE scores
        rouge_scores = self.calculate_rouge_scores(reference_text, generated_text)
        results['rouge_scores'] = rouge_scores
        
        return results
    
    def batch_evaluation(self, evaluation_data):
        """Evaluate multiple text generation examples."""
        all_results = []
        
        total_perplexity = 0
        total_bleu = 0
        rouge_totals = {'rouge1': 0, 'rouge2': 0, 'rougeL': 0}
        valid_count = 0
        
        for data in evaluation_data:
            prompt = data['prompt']
            reference = data['reference']
            generated = data['generated']
            
            result = self.evaluate_text_generation(prompt, reference, generated)
            all_results.append(result)
            
            # Accumulate scores for averaging
            if result['perplexity'] is not None:
                total_perplexity += result['perplexity']
            if result['bleu_score'] is not None:
                total_bleu += result['bleu_score']
            if result['rouge_scores'] is not None:
                for key in rouge_totals:
                    rouge_totals[key] += result['rouge_scores'][key]
            
            valid_count += 1
        
        # Calculate averages
        if valid_count > 0:
            avg_metrics = {
                'average_perplexity': total_perplexity / valid_count,
                'average_bleu': total_bleu / valid_count,
                'average_rouge1': rouge_totals['rouge1'] / valid_count,
                'average_rouge2': rouge_totals['rouge2'] / valid_count,
                'average_rougeL': rouge_totals['rougeL'] / valid_count,
                'total_samples': valid_count
            }
        else:
            avg_metrics = {}
        
        return all_results, avg_metrics
    
    def generate_and_evaluate(self, prompt, reference_text, max_length=100):
        """Generate text and evaluate it against reference."""
        try:
            # Generate text
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=max_length,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Evaluate the generated text
            return self.evaluate_text_generation(prompt, reference_text, generated_text)
            
        except Exception as e:
            logger.error(f"Error in generation and evaluation: {e}")
            return None

def main():
    """Demonstrate LLM evaluation metrics."""
    print("=== LLM Evaluation Metrics ===\n")
    
    # Initialize evaluator
    evaluator = LLMEvaluator()
    
    print("1. SINGLE TEXT EVALUATION")
    print("-" * 40)
    
    # Example data for evaluation
    prompt = "Generate an interview question about Python programming:"
    reference = "What are the key differences between lists and tuples in Python, and when would you use each data structure?"
    generated = "Can you explain the difference between Python lists and tuples and provide examples of when to use them?"
    
    result = evaluator.evaluate_text_generation(prompt, reference, generated)
    
    print(f"Prompt: {prompt}")
    print(f"Reference: {reference}")
    print(f"Generated: {generated}")
    print(f"\nEvaluation Results:")
    print(f"  Perplexity: {result['perplexity']:.2f}")
    print(f"  BLEU Score: {result['bleu_score']:.4f}")
    print(f"  ROUGE-1: {result['rouge_scores']['rouge1']:.4f}")
    print(f"  ROUGE-2: {result['rouge_scores']['rouge2']:.4f}")
    print(f"  ROUGE-L: {result['rouge_scores']['rougeL']:.4f}")
    
    print("\n\n2. BATCH EVALUATION")
    print("-" * 40)
    
    # Sample evaluation data for VMIS
    evaluation_data = [
        {
            'prompt': "Generate feedback for excellent performance:",
            'reference': "Outstanding performance! The candidate demonstrated exceptional technical skills and clear communication.",
            'generated': "Excellent work! The candidate showed strong technical abilities and communicated very well."
        },
        {
            'prompt': "Create a follow-up question about teamwork:",
            'reference': "Can you describe a time when you had to work with a difficult team member and how you handled it?",
            'generated': "Tell me about a challenging team situation you faced and how you resolved it."
        },
        {
            'prompt': "Summarize interview strengths and weaknesses:",
            'reference': "Strengths: Strong technical background, good problem-solving. Weaknesses: Needs improvement in communication skills.",
            'generated': "Strengths: Solid technical knowledge, analytical thinking. Areas for improvement: Communication and presentation."
        },
        {
            'prompt': "Generate a coding interview question:",
            'reference': "Write a function to find the longest substring without repeating characters in a given string.",
            'generated': "Implement a method to determine the longest substring with unique characters from an input string."
        },
        {
            'prompt': "Create behavioral interview feedback:",
            'reference': "The candidate showed good leadership potential but needs more experience in conflict resolution.",
            'generated': "Strong leadership qualities demonstrated, however requires development in handling team conflicts."
        }
    ]
    
    results, avg_metrics = evaluator.batch_evaluation(evaluation_data)
    
    print(f"Evaluated {len(results)} samples")
    print(f"\nAverage Metrics:")
    print(f"  Average Perplexity: {avg_metrics['average_perplexity']:.2f}")
    print(f"  Average BLEU Score: {avg_metrics['average_bleu']:.4f}")
    print(f"  Average ROUGE-1: {avg_metrics['average_rouge1']:.4f}")
    print(f"  Average ROUGE-2: {avg_metrics['average_rouge2']:.4f}")
    print(f"  Average ROUGE-L: {avg_metrics['average_rougeL']:.4f}")
    
    print("\n\n3. DETAILED INDIVIDUAL RESULTS")
    print("-" * 40)
    
    for i, result in enumerate(results, 1):
        print(f"\nSample {i}:")
        print(f"  BLEU: {result['bleu_score']:.4f}")
        print(f"  ROUGE-1: {result['rouge_scores']['rouge1']:.4f}")
        print(f"  Perplexity: {result['perplexity']:.2f}")
    
    print("\n\n4. GENERATE AND EVALUATE NEW TEXT")
    print("-" * 40)
    
    new_prompts = [
        ("Generate a technical interview question about databases:", 
         "Explain the difference between SQL and NoSQL databases and when you would choose each."),
        ("Create feedback for average performance:", 
         "The candidate performed adequately but has room for improvement in several areas."),
        ("Generate a follow-up question about problem-solving:", 
         "Walk me through your approach to debugging a complex software issue.")
    ]
    
    for prompt, reference in new_prompts:
        print(f"\nPrompt: {prompt}")
        result = evaluator.generate_and_evaluate(prompt, reference)
        
        if result:
            print(f"Generated: {result['generated']}")
            print(f"BLEU: {result['bleu_score']:.4f}, ROUGE-1: {result['rouge_scores']['rouge1']:.4f}, Perplexity: {result['perplexity']:.2f}")
    
    return results, avg_metrics

if __name__ == "__main__":
    results, metrics = main()
