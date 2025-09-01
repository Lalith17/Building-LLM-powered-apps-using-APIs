"""
Text Generation using Pre-trained LLM (GPT-2)
This script demonstrates text generation for creating interview questions.
"""

import logging
import warnings
warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import transformers with error handling
try:
    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers library loaded successfully")
except ImportError as e:
    logger.warning(f"Transformers not available: {e}")
    TRANSFORMERS_AVAILABLE = False
except Exception as e:
    logger.warning(f"Error loading transformers: {e}")
    TRANSFORMERS_AVAILABLE = False

class TextGenerator:
    def __init__(self, model_name='gpt2'):
        """Initialize the text generator with a pre-trained model."""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available, using mock responses")
            self.mock_mode = True
            return
        
        try:
            logger.info(f"Loading {model_name} model...")
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            
            # Add padding token
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.mock_mode = False
            
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.info("Falling back to mock mode")
            self.mock_mode = True
    
    def generate_interview_question(self, prompt, max_length=100, num_return_sequences=1, temperature=0.8):
        """Generate interview questions based on a given prompt."""
        if self.mock_mode:
            return self._mock_interview_question(prompt)
        
        try:
            # Encode the prompt
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
            
            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=max_length,
                    num_return_sequences=num_return_sequences,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Decode the generated text
            generated_texts = []
            for output in outputs:
                generated_text = self.tokenizer.decode(output, skip_special_tokens=True)
                generated_texts.append(generated_text)
            
            return generated_texts
            
        except Exception as e:
            logger.error(f"Error in text generation: {e}")
            return self._mock_interview_question(prompt)
    
    def _mock_interview_question(self, prompt):
        """Generate mock interview questions when model is not available."""
        mock_questions = {
            "python": "What are the key differences between lists and tuples in Python, and when would you use each data structure?",
            "teamwork": "Can you describe a time when you had to work with a difficult team member and how you handled the situation?",
            "problem": "Walk me through your approach to debugging a complex software issue that you've encountered.",
            "feedback": "Feedback: The candidate demonstrated strong technical skills with room for improvement in communication.",
            "leadership": "Tell me about a time when you had to lead a project or team through a challenging situation."
        }
        
        # Simple keyword matching for mock responses
        prompt_lower = prompt.lower()
        if "python" in prompt_lower or "programming" in prompt_lower:
            return [mock_questions["python"]]
        elif "teamwork" in prompt_lower or "team" in prompt_lower:
            return [mock_questions["teamwork"]]
        elif "problem" in prompt_lower or "solving" in prompt_lower:
            return [mock_questions["problem"]]
        elif "feedback" in prompt_lower or "performance" in prompt_lower:
            return [mock_questions["feedback"]]
        elif "leadership" in prompt_lower or "lead" in prompt_lower:
            return [mock_questions["leadership"]]
        else:
            return ["What specific experience do you have that makes you qualified for this position?"]
    
    def generate_feedback(self, performance_description, max_length=80):
        """Generate feedback for interview performance."""
        if self.mock_mode:
            return self._mock_feedback(performance_description)
        
        feedback_prompt = f"Interview feedback for candidate performance: {performance_description}\nFeedback:"
        
        try:
            input_ids = self.tokenizer.encode(feedback_prompt, return_tensors='pt')
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=len(input_ids[0]) + max_length,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the feedback part
            feedback = generated_text.replace(feedback_prompt, "").strip()
            
            return feedback
            
        except Exception as e:
            logger.error(f"Error in feedback generation: {e}")
            return self._mock_feedback(performance_description)
    
    def _mock_feedback(self, performance_description):
        """Generate mock feedback when model is not available."""
        desc_lower = performance_description.lower()
        if "strong" in desc_lower or "excellent" in desc_lower:
            return "Outstanding performance with excellent technical skills and clear communication."
        elif "poor" in desc_lower or "weak" in desc_lower:
            return "Performance needs improvement. Recommend additional training and practice."
        elif "communication" in desc_lower and "lacks" in desc_lower:
            return "Strong technical abilities demonstrated. Needs improvement in communication and presentation skills."
        else:
            return "Solid performance overall with areas for continued development and growth."
    
    def summarize_interview(self, interview_notes, max_length=100):
        """Summarize interview notes into key strengths and weaknesses."""
        if self.mock_mode:
            return self._mock_summary(interview_notes)
        
        summary_prompt = f"Interview summary - Notes: {interview_notes}\nKey strengths and weaknesses:"
        
        try:
            input_ids = self.tokenizer.encode(summary_prompt, return_tensors='pt')
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=len(input_ids[0]) + max_length,
                    temperature=0.6,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            summary = generated_text.replace(summary_prompt, "").strip()
            
            return summary
            
        except Exception as e:
            logger.error(f"Error in interview summarization: {e}")
            return self._mock_summary(interview_notes)
    
    def _mock_summary(self, interview_notes):
        """Generate mock summary when model is not available."""
        notes_lower = interview_notes.lower()
        strengths = []
        weaknesses = []
        
        # Extract strengths
        if "technical" in notes_lower and ("good" in notes_lower or "strong" in notes_lower):
            strengths.append("Strong technical background")
        if "coding" in notes_lower and ("good" in notes_lower or "well" in notes_lower):
            strengths.append("Good coding skills")
        if "problem" in notes_lower and "solving" in notes_lower:
            strengths.append("Problem-solving abilities")
        if "communication" in notes_lower and ("good" in notes_lower or "clear" in notes_lower):
            strengths.append("Clear communication")
        
        # Extract weaknesses
        if "nervous" in notes_lower or "presentation" in notes_lower:
            weaknesses.append("Presentation skills")
        if "lacks" in notes_lower or "needs" in notes_lower:
            if "experience" in notes_lower:
                weaknesses.append("More experience needed")
            if "communication" in notes_lower:
                weaknesses.append("Communication skills")
        
        # Default if no specific patterns found
        if not strengths:
            strengths = ["Technical competence", "Problem-solving approach"]
        if not weaknesses:
            weaknesses = ["Area for continued development"]
        
        return f"Strengths: {', '.join(strengths)}. Areas for improvement: {', '.join(weaknesses)}."

def main():
    """Demonstrate text generation capabilities."""
    print("=== Text Generation with GPT-2 ===\n")
    
    # Initialize the generator
    generator = TextGenerator()
    
    # Test prompts for interview questions
    interview_prompts = [
        "Generate a technical interview question about Python programming:",
        "Create a behavioral interview question about teamwork:",
        "Design a problem-solving question for software engineers:",
    ]
    
    print("1. INTERVIEW QUESTION GENERATION")
    print("-" * 40)
    
    for i, prompt in enumerate(interview_prompts, 1):
        print(f"\nPrompt {i}: {prompt}")
        questions = generator.generate_interview_question(prompt, max_length=80)
        for j, question in enumerate(questions, 1):
            print(f"Generated Question {j}: {question}\n")
    
    print("\n2. FEEDBACK GENERATION")
    print("-" * 40)
    
    # Test feedback generation
    performance_descriptions = [
        "The candidate demonstrates strong analytical skills but lacks communication abilities.",
        "Excellent problem-solving approach with clear explanations and good coding practices.",
        "Shows creativity in solutions but needs improvement in technical depth."
    ]
    
    for desc in performance_descriptions:
        print(f"\nPerformance: {desc}")
        feedback = generator.generate_feedback(desc)
        print(f"Generated Feedback: {feedback}\n")
    
    print("\n3. INTERVIEW SUMMARIZATION")
    print("-" * 40)
    
    # Test interview summarization
    interview_notes = [
        "Candidate answered technical questions well, showed good coding skills, but was nervous during presentation",
        "Strong background in machine learning, excellent communication, lacks experience in system design",
        "Creative problem solver, good team player, needs improvement in time management"
    ]
    
    for notes in interview_notes:
        print(f"\nInterview Notes: {notes}")
        summary = generator.summarize_interview(notes)
        print(f"Summary: {summary}\n")

if __name__ == "__main__":
    main()
