"""
Sentiment Analysis for VMIS Feedback Classification
This script uses BERT for sentiment analysis of interview feedback.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_name='cardiffnlp/twitter-roberta-base-sentiment-latest'):
        """Initialize sentiment analyzer with a pre-trained model."""
        logger.info(f"Loading sentiment analysis model: {model_name}")
        
        try:
            # Use pipeline for easier sentiment analysis
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=model_name,
                tokenizer=model_name
            )
            logger.info("Sentiment analysis model loaded successfully!")
            
        except Exception as e:
            logger.warning(f"Failed to load {model_name}, falling back to default model")
            # Fallback to a simpler model
            self.sentiment_pipeline = pipeline("sentiment-analysis")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of given text."""
        try:
            result = self.sentiment_pipeline(text)
            return result[0]
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {"label": "UNKNOWN", "score": 0.0}
    
    def analyze_feedback_batch(self, feedback_list):
        """Analyze sentiment for a batch of feedback texts."""
        results = []
        for feedback in feedback_list:
            sentiment = self.analyze_sentiment(feedback)
            results.append({
                "feedback": feedback,
                "sentiment": sentiment["label"],
                "confidence": sentiment["score"]
            })
        return results
    
    def classify_interview_performance(self, feedback):
        """Classify interview performance based on feedback sentiment."""
        sentiment_result = self.analyze_sentiment(feedback)
        
        label = sentiment_result["label"].upper()
        confidence = sentiment_result["score"]
        
        # Map sentiment to performance categories
        if label in ["POSITIVE", "POS"]:
            if confidence > 0.8:
                performance = "Excellent"
            elif confidence > 0.6:
                performance = "Good"
            else:
                performance = "Satisfactory"
        elif label in ["NEGATIVE", "NEG"]:
            if confidence > 0.8:
                performance = "Poor"
            elif confidence > 0.6:
                performance = "Needs Improvement"
            else:
                performance = "Below Average"
        else:  # NEUTRAL
            performance = "Average"
        
        return {
            "performance_rating": performance,
            "sentiment": label,
            "confidence": confidence,
            "feedback": feedback
        }

def main():
    """Demonstrate sentiment analysis capabilities."""
    print("=== Sentiment Analysis for VMIS Feedback ===\n")
    
    # Initialize the analyzer
    analyzer = SentimentAnalyzer()
    
    # Sample feedback texts for VMIS
    vmis_feedback_samples = [
        "The candidate demonstrated excellent problem-solving skills and clear communication throughout the interview.",
        "Poor performance overall, candidate struggled with basic concepts and couldn't answer simple questions.",
        "Average interview performance, candidate showed some knowledge but lacked depth in technical areas.",
        "Outstanding candidate! Strong technical background, excellent presentation skills, and great cultural fit.",
        "The interview was disappointing. Candidate was unprepared and gave vague answers to most questions.",
        "Solid performance with room for improvement. Good technical skills but needs better communication.",
        "Exceptional candidate with innovative thinking and strong leadership potential.",
        "Candidate showed basic understanding but made several critical errors in problem-solving.",
        "Very impressed with the candidate's approach to complex problems and ability to think on their feet.",
        "Mediocre performance, neither outstanding nor concerning, but meets minimum requirements."
    ]
    
    print("1. INDIVIDUAL SENTIMENT ANALYSIS")
    print("-" * 50)
    
    for i, feedback in enumerate(vmis_feedback_samples, 1):
        print(f"\nFeedback {i}: {feedback}")
        result = analyzer.analyze_sentiment(feedback)
        print(f"Sentiment: {result['label']} (Confidence: {result['score']:.3f})")
    
    print("\n\n2. BATCH SENTIMENT ANALYSIS")
    print("-" * 50)
    
    batch_results = analyzer.analyze_feedback_batch(vmis_feedback_samples[:5])
    for result in batch_results:
        print(f"\nFeedback: {result['feedback'][:60]}...")
        print(f"Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.3f})")
    
    print("\n\n3. INTERVIEW PERFORMANCE CLASSIFICATION")
    print("-" * 50)
    
    performance_feedback = [
        "The candidate exceeded expectations in all areas of the technical interview.",
        "Candidate failed to demonstrate basic programming knowledge and couldn't solve simple problems.",
        "Interview went well, candidate showed competence but nothing exceptional.",
        "Absolutely brilliant performance! This candidate would be a great addition to our team.",
        "Very concerning interview, candidate seemed unprepared and disinterested."
    ]
    
    for feedback in performance_feedback:
        print(f"\nFeedback: {feedback}")
        classification = analyzer.classify_interview_performance(feedback)
        print(f"Performance Rating: {classification['performance_rating']}")
        print(f"Sentiment: {classification['sentiment']} (Confidence: {classification['confidence']:.3f})")
    
    print("\n\n4. SENTIMENT DISTRIBUTION ANALYSIS")
    print("-" * 50)
    
    all_results = analyzer.analyze_feedback_batch(vmis_feedback_samples)
    
    # Count sentiments
    sentiment_counts = {}
    total_confidence = 0
    
    for result in all_results:
        sentiment = result['sentiment']
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts[sentiment] = 1
        total_confidence += result['confidence']
    
    print(f"Total feedback samples analyzed: {len(all_results)}")
    print(f"Average confidence: {total_confidence/len(all_results):.3f}")
    print("\nSentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(all_results)) * 100
        print(f"  {sentiment}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
