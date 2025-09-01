"""
Main Runner Script for LLM Assignment
This script orchestrates all the LLM tasks and generates comprehensive results.
"""

import sys
import os
import json
import logging
from datetime import datetime

# Import all our custom modules
from text_generation import TextGenerator
from sentiment_analysis import SentimentAnalyzer
from masked_language_modeling import MaskedLanguageModel
from evaluation_metrics import LLMEvaluator
from custom_prompts import VMISPromptEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('llm_assignment_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LLMAssignmentRunner:
    def __init__(self):
        """Initialize the assignment runner."""
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tasks_completed': [],
            'text_generation': {},
            'sentiment_analysis': {},
            'masked_language_modeling': {},
            'evaluation_metrics': {},
            'custom_prompts': {}
        }
        
        self.test_cases = []
        self.evaluation_results = []
    
    def run_text_generation_task(self):
        """Run the text generation task."""
        logger.info("Starting Text Generation Task...")
        
        try:
            generator = TextGenerator()
            
            # Test cases for text generation
            test_prompts = [
                "Generate a technical interview question about Python programming:",
                "Create a behavioral interview question about teamwork:",
                "Design a problem-solving question for software engineers:",
                "Generate feedback for excellent interview performance:",
                "Create a follow-up question about leadership experience:"
            ]
            
            generation_results = []
            
            for prompt in test_prompts:
                questions = generator.generate_interview_question(prompt, max_length=80)
                for question in questions:
                    test_case = {
                        'task': 'text_generation',
                        'prompt': prompt,
                        'generated_output': question,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.test_cases.append(test_case)
                    generation_results.append(test_case)
            
            self.results['text_generation'] = {
                'status': 'completed',
                'total_generations': len(generation_results),
                'sample_outputs': generation_results[:3]  # Store first 3 as samples
            }
            
            self.results['tasks_completed'].append('text_generation')
            logger.info("Text Generation Task completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in text generation task: {e}")
            self.results['text_generation'] = {'status': 'failed', 'error': str(e)}
    
    def run_sentiment_analysis_task(self):
        """Run the sentiment analysis task."""
        logger.info("Starting Sentiment Analysis Task...")
        
        try:
            analyzer = SentimentAnalyzer()
            
            # Test feedback samples
            feedback_samples = [
                "The candidate demonstrated excellent problem-solving skills and clear communication throughout the interview.",
                "Poor performance overall, candidate struggled with basic concepts and couldn't answer simple questions.",
                "Average interview performance, candidate showed some knowledge but lacked depth in technical areas.",
                "Outstanding candidate! Strong technical background, excellent presentation skills, and great cultural fit.",
                "The interview was disappointing. Candidate was unprepared and gave vague answers to most questions.",
                "Solid performance with room for improvement. Good technical skills but needs better communication.",
                "Exceptional candidate with innovative thinking and strong leadership potential.",
                "Candidate showed basic understanding but made several critical errors in problem-solving."
            ]
            
            sentiment_results = []
            
            for feedback in feedback_samples:
                result = analyzer.classify_interview_performance(feedback)
                test_case = {
                    'task': 'sentiment_analysis',
                    'input_feedback': feedback,
                    'sentiment': result['sentiment'],
                    'performance_rating': result['performance_rating'],
                    'confidence': result['confidence'],
                    'timestamp': datetime.now().isoformat()
                }
                self.test_cases.append(test_case)
                sentiment_results.append(test_case)
            
            # Calculate distribution
            sentiment_counts = {}
            total_confidence = 0
            
            for result in sentiment_results:
                sentiment = result['sentiment']
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
                total_confidence += result['confidence']
            
            self.results['sentiment_analysis'] = {
                'status': 'completed',
                'total_analyzed': len(sentiment_results),
                'sentiment_distribution': sentiment_counts,
                'average_confidence': total_confidence / len(sentiment_results),
                'sample_results': sentiment_results[:3]
            }
            
            self.results['tasks_completed'].append('sentiment_analysis')
            logger.info("Sentiment Analysis Task completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis task: {e}")
            self.results['sentiment_analysis'] = {'status': 'failed', 'error': str(e)}
    
    def run_masked_language_modeling_task(self):
        """Run the masked language modeling task."""
        logger.info("Starting Masked Language Modeling Task...")
        
        try:
            mlm = MaskedLanguageModel()
            
            # Test sentences with masks
            masked_sentences = [
                "The candidate demonstrated excellent [MASK] skills during the interview.",
                "The interview went [MASK] and we were impressed with their performance.",
                "We need to [MASK] the candidate's technical abilities before making a decision.",
                "The candidate's [MASK] to complex problems was outstanding.",
                "During the [MASK] process, we evaluate both technical and soft skills.",
                "The applicant showed great [MASK] when solving the coding challenge.",
                "Her [MASK] skills impressed the entire interview panel.",
                "The final [MASK] will be with the hiring manager next week."
            ]
            
            mlm_results = []
            
            for sentence in masked_sentences:
                predictions = mlm.predict_masked_word(sentence, top_k=3)
                test_case = {
                    'task': 'masked_language_modeling',
                    'masked_sentence': sentence,
                    'predictions': predictions[:3],  # Top 3 predictions
                    'timestamp': datetime.now().isoformat()
                }
                self.test_cases.append(test_case)
                mlm_results.append(test_case)
            
            self.results['masked_language_modeling'] = {
                'status': 'completed',
                'total_predictions': len(mlm_results),
                'sample_results': mlm_results[:3]
            }
            
            self.results['tasks_completed'].append('masked_language_modeling')
            logger.info("Masked Language Modeling Task completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in masked language modeling task: {e}")
            self.results['masked_language_modeling'] = {'status': 'failed', 'error': str(e)}
    
    def run_evaluation_metrics_task(self):
        """Run the evaluation metrics task."""
        logger.info("Starting Evaluation Metrics Task...")
        
        try:
            evaluator = LLMEvaluator()
            
            # Sample evaluation data
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
            
            # Store evaluation results
            for result in results:
                eval_case = {
                    'task': 'evaluation_metrics',
                    'prompt': result['prompt'],
                    'reference': result['reference'],
                    'generated': result['generated'],
                    'bleu_score': result['bleu_score'],
                    'rouge_scores': result['rouge_scores'],
                    'perplexity': result['perplexity'],
                    'timestamp': result['timestamp']
                }
                self.evaluation_results.append(eval_case)
            
            self.results['evaluation_metrics'] = {
                'status': 'completed',
                'average_metrics': avg_metrics,
                'individual_results': results[:3]  # Store first 3 as samples
            }
            
            self.results['tasks_completed'].append('evaluation_metrics')
            logger.info("Evaluation Metrics Task completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in evaluation metrics task: {e}")
            self.results['evaluation_metrics'] = {'status': 'failed', 'error': str(e)}
    
    def run_custom_prompts_task(self):
        """Run the custom prompts task."""
        logger.info("Starting Custom Prompts Task...")
        
        try:
            engine = VMISPromptEngine()
            
            # Test custom prompt scenarios
            custom_scenarios = [
                {
                    'type': 'feedback',
                    'input': 'The candidate demonstrates strong analytical skills but lacks communication abilities.',
                    'method': 'generate_interview_feedback'
                },
                {
                    'type': 'summary',
                    'input': 'Candidate answered technical questions well, showed good coding skills, but was nervous during presentation',
                    'method': 'summarize_interview_notes'
                },
                {
                    'type': 'follow_up',
                    'input': 'I used Python and machine learning to solve the problem',
                    'topic': 'Technical Implementation',
                    'method': 'create_follow_up_questions'
                },
                {
                    'type': 'behavioral',
                    'input': 'Leadership and Team Management',
                    'method': 'generate_behavioral_questions'
                },
                {
                    'type': 'technical',
                    'role': 'Software Engineer',
                    'difficulty': 'Intermediate',
                    'method': 'create_technical_assessment'
                }
            ]
            
            custom_results = []
            
            for scenario in custom_scenarios:
                if scenario['type'] == 'feedback':
                    output = engine.generate_interview_feedback(scenario['input'])
                elif scenario['type'] == 'summary':
                    output = engine.summarize_interview_notes(scenario['input'])
                elif scenario['type'] == 'follow_up':
                    output = engine.create_follow_up_questions(scenario['input'], scenario['topic'])
                elif scenario['type'] == 'behavioral':
                    output = engine.generate_behavioral_questions(scenario['input'])
                elif scenario['type'] == 'technical':
                    output = engine.create_technical_assessment(scenario['role'], scenario['difficulty'])
                
                test_case = {
                    'task': 'custom_prompts',
                    'prompt_type': scenario['type'],
                    'input': scenario.get('input', ''),
                    'generated_output': output,
                    'timestamp': datetime.now().isoformat()
                }
                self.test_cases.append(test_case)
                custom_results.append(test_case)
            
            self.results['custom_prompts'] = {
                'status': 'completed',
                'total_prompts': len(custom_results),
                'prompt_types': list(set([r['prompt_type'] for r in custom_results])),
                'sample_results': custom_results[:3]
            }
            
            self.results['tasks_completed'].append('custom_prompts')
            logger.info("Custom Prompts Task completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in custom prompts task: {e}")
            self.results['custom_prompts'] = {'status': 'failed', 'error': str(e)}
    
    def save_results(self):
        """Save all results to files."""
        logger.info("Saving results to files...")
        
        try:
            # Save test cases
            with open('test_cases.txt', 'w', encoding='utf-8') as f:
                f.write("LLM Assignment Test Cases\n")
                f.write("=" * 50 + "\n\n")
                
                for i, case in enumerate(self.test_cases, 1):
                    f.write(f"Test Case {i}:\n")
                    f.write(f"Task: {case['task']}\n")
                    f.write(f"Timestamp: {case['timestamp']}\n")
                    
                    if 'prompt' in case:
                        f.write(f"Prompt: {case['prompt']}\n")
                    if 'input_feedback' in case:
                        f.write(f"Input: {case['input_feedback']}\n")
                    if 'masked_sentence' in case:
                        f.write(f"Masked Sentence: {case['masked_sentence']}\n")
                    if 'generated_output' in case:
                        f.write(f"Output: {case['generated_output']}\n")
                    if 'sentiment' in case:
                        f.write(f"Sentiment: {case['sentiment']} (Confidence: {case['confidence']:.3f})\n")
                    if 'predictions' in case:
                        f.write("Predictions:\n")
                        for pred in case['predictions']:
                            f.write(f"  - {pred['predicted_word']} (confidence: {pred['confidence']:.3f})\n")
                    
                    f.write("\n" + "-" * 30 + "\n\n")
            
            # Save evaluation results
            with open('evaluation_results.txt', 'w', encoding='utf-8') as f:
                f.write("LLM Evaluation Results\n")
                f.write("=" * 50 + "\n\n")
                
                if self.results['evaluation_metrics']['status'] == 'completed':
                    avg_metrics = self.results['evaluation_metrics']['average_metrics']
                    f.write("AVERAGE METRICS:\n")
                    f.write(f"Average Perplexity: {avg_metrics['average_perplexity']:.2f}\n")
                    f.write(f"Average BLEU Score: {avg_metrics['average_bleu']:.4f}\n")
                    f.write(f"Average ROUGE-1: {avg_metrics['average_rouge1']:.4f}\n")
                    f.write(f"Average ROUGE-2: {avg_metrics['average_rouge2']:.4f}\n")
                    f.write(f"Average ROUGE-L: {avg_metrics['average_rougeL']:.4f}\n")
                    f.write(f"Total Samples: {avg_metrics['total_samples']}\n\n")
                
                f.write("INDIVIDUAL RESULTS:\n")
                f.write("-" * 30 + "\n")
                
                for i, result in enumerate(self.evaluation_results, 1):
                    f.write(f"\nEvaluation {i}:\n")
                    f.write(f"Prompt: {result['prompt']}\n")
                    f.write(f"Reference: {result['reference']}\n")
                    f.write(f"Generated: {result['generated']}\n")
                    f.write(f"BLEU Score: {result['bleu_score']:.4f}\n")
                    f.write(f"ROUGE-1: {result['rouge_scores']['rouge1']:.4f}\n")
                    f.write(f"ROUGE-2: {result['rouge_scores']['rouge2']:.4f}\n")
                    f.write(f"ROUGE-L: {result['rouge_scores']['rougeL']:.4f}\n")
                    f.write(f"Perplexity: {result['perplexity']:.2f}\n")
                    f.write("-" * 20 + "\n")
            
            # Save comprehensive results as JSON
            with open('comprehensive_results.json', 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            
            logger.info("Results saved successfully!")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def generate_summary_report(self):
        """Generate a summary report."""
        logger.info("Generating summary report...")
        
        with open('assignment_summary.txt', 'w', encoding='utf-8') as f:
            f.write("LLM Assignment Summary Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Execution Date: {self.results['timestamp']}\n")
            f.write(f"Tasks Completed: {len(self.results['tasks_completed'])}/5\n")
            f.write(f"Completed Tasks: {', '.join(self.results['tasks_completed'])}\n\n")
            
            f.write("TASK DETAILS:\n")
            f.write("-" * 20 + "\n\n")
            
            for task in ['text_generation', 'sentiment_analysis', 'masked_language_modeling', 'evaluation_metrics', 'custom_prompts']:
                task_result = self.results.get(task, {})
                f.write(f"{task.replace('_', ' ').title()}:\n")
                f.write(f"  Status: {task_result.get('status', 'Not executed')}\n")
                
                if task_result.get('status') == 'completed':
                    if task == 'text_generation':
                        f.write(f"  Total Generations: {task_result.get('total_generations', 0)}\n")
                    elif task == 'sentiment_analysis':
                        f.write(f"  Total Analyzed: {task_result.get('total_analyzed', 0)}\n")
                        f.write(f"  Average Confidence: {task_result.get('average_confidence', 0):.3f}\n")
                    elif task == 'masked_language_modeling':
                        f.write(f"  Total Predictions: {task_result.get('total_predictions', 0)}\n")
                    elif task == 'evaluation_metrics':
                        avg_metrics = task_result.get('average_metrics', {})
                        f.write(f"  Average BLEU: {avg_metrics.get('average_bleu', 0):.4f}\n")
                        f.write(f"  Average ROUGE-1: {avg_metrics.get('average_rouge1', 0):.4f}\n")
                    elif task == 'custom_prompts':
                        f.write(f"  Total Prompts: {task_result.get('total_prompts', 0)}\n")
                        f.write(f"  Prompt Types: {', '.join(task_result.get('prompt_types', []))}\n")
                
                f.write("\n")
            
            f.write(f"Total Test Cases Generated: {len(self.test_cases)}\n")
            f.write(f"Total Evaluation Results: {len(self.evaluation_results)}\n")
    
    def run_all_tasks(self):
        """Run all LLM assignment tasks."""
        logger.info("Starting LLM Assignment Runner...")
        
        tasks = [
            self.run_text_generation_task,
            self.run_sentiment_analysis_task,
            self.run_masked_language_modeling_task,
            self.run_evaluation_metrics_task,
            self.run_custom_prompts_task
        ]
        
        for task in tasks:
            try:
                task()
            except Exception as e:
                logger.error(f"Error in task {task.__name__}: {e}")
                continue
        
        # Save all results
        self.save_results()
        self.generate_summary_report()
        
        logger.info("LLM Assignment completed!")
        logger.info(f"Tasks completed: {len(self.results['tasks_completed'])}/5")
        logger.info(f"Check the following files for results:")
        logger.info("  - test_cases.txt")
        logger.info("  - evaluation_results.txt") 
        logger.info("  - comprehensive_results.json")
        logger.info("  - assignment_summary.txt")
        logger.info("  - llm_assignment_log.txt")

def main():
    """Main function to run the LLM assignment."""
    runner = LLMAssignmentRunner()
    runner.run_all_tasks()

if __name__ == "__main__":
    main()
