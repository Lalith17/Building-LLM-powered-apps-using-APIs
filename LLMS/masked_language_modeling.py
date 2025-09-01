"""
Masked Language Modeling using BERT
This script demonstrates BERT's ability to predict missing words in sentences.
"""

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MaskedLanguageModel:
    def __init__(self, model_name='bert-base-uncased'):
        """Initialize the masked language model."""
        logger.info(f"Loading BERT model: {model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForMaskedLM.from_pretrained(model_name)
            
            # Also create a pipeline for easier use
            self.fill_mask_pipeline = pipeline(
                "fill-mask",
                model=model_name,
                tokenizer=model_name
            )
            
            logger.info("BERT model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict_masked_word(self, masked_sentence, top_k=5):
        """Predict the masked word in a sentence."""
        try:
            # Use the pipeline for prediction
            results = self.fill_mask_pipeline(masked_sentence, top_k=top_k)
            
            predictions = []
            for result in results:
                predictions.append({
                    "predicted_word": result["token_str"],
                    "confidence": result["score"],
                    "complete_sentence": result["sequence"]
                })
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error in masked word prediction: {e}")
            return []
    
    def predict_multiple_masks(self, sentence_with_masks, top_k=3):
        """Handle sentences with multiple [MASK] tokens."""
        try:
            # For multiple masks, we'll predict one at a time
            # This is a simplified approach
            results = self.fill_mask_pipeline(sentence_with_masks, top_k=top_k)
            
            if isinstance(results[0], list):
                # Multiple masks case
                return results
            else:
                # Single mask case
                return [results]
                
        except Exception as e:
            logger.error(f"Error in multiple mask prediction: {e}")
            return []
    
    def interview_context_prediction(self, interview_sentences):
        """Predict masked words in interview-related contexts."""
        predictions = {}
        
        for sentence in interview_sentences:
            print(f"\nOriginal: {sentence}")
            
            try:
                results = self.predict_masked_word(sentence, top_k=3)
                predictions[sentence] = results
                
                print("Predictions:")
                for i, pred in enumerate(results, 1):
                    print(f"  {i}. {pred['predicted_word']} (confidence: {pred['confidence']:.3f})")
                    print(f"     Complete: {pred['complete_sentence']}")
                
            except Exception as e:
                logger.error(f"Error processing sentence: {e}")
                predictions[sentence] = []
        
        return predictions

def main():
    """Demonstrate masked language modeling capabilities."""
    print("=== Masked Language Modeling with BERT ===\n")
    
    # Initialize the model
    mlm = MaskedLanguageModel()
    
    print("1. BASIC MASKED WORD PREDICTION")
    print("-" * 40)
    
    # Basic examples
    basic_sentences = [
        "The candidate demonstrated excellent [MASK] skills during the interview.",
        "The interview went [MASK] and we were impressed with their performance.",
        "We need to [MASK] the candidate's technical abilities before making a decision.",
        "The candidate's [MASK] to complex problems was outstanding.",
        "During the [MASK] process, we evaluate both technical and soft skills."
    ]
    
    for sentence in basic_sentences:
        print(f"\nSentence: {sentence}")
        predictions = mlm.predict_masked_word(sentence, top_k=3)
        
        print("Top predictions:")
        for i, pred in enumerate(predictions, 1):
            print(f"  {i}. '{pred['predicted_word']}' (confidence: {pred['confidence']:.3f})")
    
    print("\n\n2. INTERVIEW-SPECIFIC CONTEXT PREDICTION")
    print("-" * 40)
    
    # Interview-related sentences
    interview_sentences = [
        "The candidate's [MASK] experience makes them a strong fit for this role.",
        "We should schedule a [MASK] interview to assess their technical skills.",
        "The applicant showed great [MASK] when solving the coding challenge.",
        "Her [MASK] skills impressed the entire interview panel.",
        "The final [MASK] will be with the hiring manager next week."
    ]
    
    mlm.interview_context_prediction(interview_sentences)
    
    print("\n\n3. VMIS FEEDBACK CONTEXT PREDICTION")
    print("-" * 40)
    
    # VMIS-specific feedback sentences
    vmis_feedback_sentences = [
        "The candidate's performance was [MASK] throughout the entire interview.",
        "We recommend [MASK] this candidate for the next round of interviews.",
        "The applicant needs to improve their [MASK] skills before we can proceed.",
        "Overall, the interview was [MASK] and the candidate met our expectations.",
        "The candidate's [MASK] to work under pressure was clearly demonstrated."
    ]
    
    for sentence in vmis_feedback_sentences:
        print(f"\nFeedback: {sentence}")
        predictions = mlm.predict_masked_word(sentence, top_k=5)
        
        print("Predictions:")
        for i, pred in enumerate(predictions, 1):
            print(f"  {i}. '{pred['predicted_word']}' (score: {pred['confidence']:.3f})")
    
    print("\n\n4. ADVANCED: SENTENCE COMPLETION")
    print("-" * 40)
    
    # More complex sentences for completion
    complex_sentences = [
        "The interview process includes [MASK] assessment, technical evaluation, and [MASK] interview.",
        "Based on the candidate's [MASK], we believe they would be a [MASK] addition to our team.",
        "The applicant demonstrated [MASK] problem-solving skills and excellent [MASK] abilities."
    ]
    
    for sentence in complex_sentences:
        print(f"\nSentence: {sentence}")
        
        # Handle multiple masks by processing one at a time
        if sentence.count('[MASK]') > 1:
            print("(Note: Multiple masks detected - processing sequentially)")
        
        try:
            predictions = mlm.predict_masked_word(sentence, top_k=2)
            print("Top predictions for first [MASK]:")
            for i, pred in enumerate(predictions, 1):
                print(f"  {i}. '{pred['predicted_word']}' -> {pred['complete_sentence']}")
                
        except Exception as e:
            print(f"Error processing: {e}")

if __name__ == "__main__":
    main()
