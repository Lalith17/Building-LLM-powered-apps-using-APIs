"""
Custom Prompts for VMIS - Interview Feedback, Summarization, and Question Generation
This script demonstrates advanced prompt engineering for specific VMIS use cases.
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VMISPromptEngine:
    def __init__(self, model_name='gpt2'):
        """Initialize the custom prompt engine for VMIS."""
        logger.info(f"Loading model for custom prompts: {model_name}")
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        logger.info("Custom prompt engine loaded successfully!")
    
    def generate_response(self, prompt, max_length=150, temperature=0.7):
        """Generate response for a given prompt."""
        try:
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=len(input_ids[0]) + max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2,
                    top_p=0.9
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the original prompt from the response
            response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Unable to generate response."
    
    def generate_interview_feedback(self, performance_description):
        """Generate structured feedback for interview performance."""
        
        # Template for feedback generation
        feedback_prompt = f"""
Interview Performance Analysis:
Candidate Performance: {performance_description}

Structured Feedback:
Strengths:"""
        
        response = self.generate_response(feedback_prompt, max_length=100)
        
        # Clean up the response
        if response:
            return f"Strengths: {response}"
        return "Unable to generate feedback."
    
    def summarize_interview_notes(self, interview_notes):
        """Summarize interview notes into key strengths and weaknesses."""
        
        summary_prompt = f"""
Interview Notes: {interview_notes}

Summary:
Key Strengths:"""
        
        response = self.generate_response(summary_prompt, max_length=120)
        
        return response if response else "Unable to generate summary."
    
    def create_follow_up_questions(self, previous_response, topic_area):
        """Create follow-up interview questions based on previous responses."""
        
        question_prompt = f"""
Previous Response: {previous_response}
Topic Area: {topic_area}

Follow-up Question:"""
        
        response = self.generate_response(question_prompt, max_length=80)
        
        return response if response else "Unable to generate follow-up question."
    
    def generate_behavioral_questions(self, competency):
        """Generate behavioral interview questions for specific competencies."""
        
        behavioral_prompt = f"""
Competency: {competency}

Behavioral Interview Question:"""
        
        response = self.generate_response(behavioral_prompt, max_length=60)
        
        return response if response else "Unable to generate behavioral question."
    
    def create_technical_assessment(self, role, difficulty_level):
        """Create technical assessment questions for specific roles."""
        
        technical_prompt = f"""
Role: {role}
Difficulty: {difficulty_level}

Technical Assessment Question:"""
        
        response = self.generate_response(technical_prompt, max_length=100)
        
        return response if response else "Unable to generate technical question."
    
    def performance_rating_feedback(self, skills_assessment):
        """Generate performance rating with specific feedback."""
        
        rating_prompt = f"""
Skills Assessment: {skills_assessment}

Performance Rating and Detailed Feedback:
Rating:"""
        
        response = self.generate_response(rating_prompt, max_length=120)
        
        return response if response else "Unable to generate rating feedback."

def main():
    """Demonstrate custom prompt engineering for VMIS."""
    print("=== Custom Prompts for VMIS ===\n")
    
    # Initialize the prompt engine
    engine = VMISPromptEngine()
    
    print("1. INTERVIEW FEEDBACK GENERATION")
    print("-" * 45)
    
    # Test performance descriptions
    performance_descriptions = [
        "The candidate demonstrates strong analytical skills but lacks communication abilities.",
        "Excellent problem-solving approach with clear explanations and good coding practices.",
        "Shows creativity in solutions but needs improvement in technical depth and presentation skills.",
        "Outstanding technical knowledge and leadership potential, minor areas for growth in time management.",
        "Basic understanding of concepts but struggled with complex problems and team collaboration scenarios."
    ]
    
    for i, description in enumerate(performance_descriptions, 1):
        print(f"\nExample {i}:")
        print(f"Input: {description}")
        feedback = engine.generate_interview_feedback(description)
        print(f"Generated Feedback: {feedback}")
    
    print("\n\n2. INTERVIEW SUMMARIZATION")
    print("-" * 45)
    
    # Test interview notes
    interview_notes_samples = [
        "Candidate answered technical questions well, showed good coding skills, but was nervous during presentation and had difficulty explaining complex concepts clearly.",
        "Strong background in machine learning and data science, excellent communication and problem-solving skills, but lacks experience in system design and scalability.",
        "Creative problem solver with innovative approaches, good team collaboration skills, but needs improvement in time management and meeting project deadlines.",
        "Solid programming fundamentals and debugging skills, shows enthusiasm for learning, but requires mentoring in advanced algorithms and software architecture.",
        "Exceptional leadership qualities and strategic thinking, strong technical foundation, minor areas for development in conflict resolution and stakeholder management."
    ]
    
    for i, notes in enumerate(interview_notes_samples, 1):
        print(f"\nInterview Notes {i}: {notes}")
        summary = engine.summarize_interview_notes(notes)
        print(f"Summary: {summary}")
    
    print("\n\n3. FOLLOW-UP QUESTION GENERATION")
    print("-" * 45)
    
    # Test follow-up scenarios
    follow_up_scenarios = [
        {
            'response': "I used Python and machine learning algorithms to solve the data analysis problem.",
            'topic': "Technical Implementation"
        },
        {
            'response': "I collaborated with my team by organizing daily stand-ups and using agile methodologies.",
            'topic': "Team Leadership"
        },
        {
            'response': "I handled the difficult situation by listening to all perspectives and finding a compromise.",
            'topic': "Conflict Resolution"
        },
        {
            'response': "I prioritized tasks based on business impact and deadlines, using project management tools.",
            'topic': "Project Management"
        }
    ]
    
    for i, scenario in enumerate(follow_up_scenarios, 1):
        print(f"\nScenario {i}:")
        print(f"Previous Response: {scenario['response']}")
        print(f"Topic Area: {scenario['topic']}")
        follow_up = engine.create_follow_up_questions(scenario['response'], scenario['topic'])
        print(f"Follow-up Question: {follow_up}")
    
    print("\n\n4. BEHAVIORAL QUESTION GENERATION")
    print("-" * 45)
    
    # Test competencies
    competencies = [
        "Leadership and Team Management",
        "Problem Solving and Critical Thinking",
        "Communication and Interpersonal Skills",
        "Adaptability and Change Management",
        "Customer Focus and Service Orientation"
    ]
    
    for competency in competencies:
        print(f"\nCompetency: {competency}")
        question = engine.generate_behavioral_questions(competency)
        print(f"Behavioral Question: {question}")
    
    print("\n\n5. TECHNICAL ASSESSMENT GENERATION")
    print("-" * 45)
    
    # Test technical roles and difficulty levels
    technical_scenarios = [
        {'role': 'Software Engineer', 'difficulty': 'Intermediate'},
        {'role': 'Data Scientist', 'difficulty': 'Advanced'},
        {'role': 'DevOps Engineer', 'difficulty': 'Senior'},
        {'role': 'Frontend Developer', 'difficulty': 'Junior'},
        {'role': 'Machine Learning Engineer', 'difficulty': 'Expert'}
    ]
    
    for scenario in technical_scenarios:
        print(f"\nRole: {scenario['role']} | Difficulty: {scenario['difficulty']}")
        question = engine.create_technical_assessment(scenario['role'], scenario['difficulty'])
        print(f"Technical Question: {question}")
    
    print("\n\n6. PERFORMANCE RATING WITH DETAILED FEEDBACK")
    print("-" * 45)
    
    # Test skills assessments
    skills_assessments = [
        "Strong in algorithms and data structures, good debugging skills, needs improvement in system design",
        "Excellent communication and leadership, solid technical foundation, requires growth in advanced programming concepts",
        "Outstanding problem-solving abilities, creative thinking, minor gaps in testing and documentation practices",
        "Good team collaboration and project management, adequate technical skills, needs development in strategic planning",
        "Exceptional technical expertise and innovation, strong analytical skills, requires improvement in mentoring and knowledge sharing"
    ]
    
    for i, assessment in enumerate(skills_assessments, 1):
        print(f"\nSkills Assessment {i}: {assessment}")
        rating_feedback = engine.performance_rating_feedback(assessment)
        print(f"Rating & Feedback: {rating_feedback}")
    
    print("\n\n7. VMIS INTEGRATION EXAMPLES")
    print("-" * 45)
    
    # Demonstrate how these would work in VMIS context
    vmis_examples = [
        {
            'scenario': 'Post-Interview Feedback',
            'input': 'Technical skills: 8/10, Communication: 6/10, Problem-solving: 9/10',
            'prompt_type': 'feedback'
        },
        {
            'scenario': 'Interview Summary for HR',
            'input': 'Candidate performed well in coding challenge, showed good system design knowledge, but had difficulty with behavioral questions about conflict resolution',
            'prompt_type': 'summary'
        },
        {
            'scenario': 'Next Round Preparation',
            'input': 'Candidate mentioned experience with microservices and cloud architecture',
            'prompt_type': 'follow_up'
        }
    ]
    
    for example in vmis_examples:
        print(f"\nVMIS Scenario: {example['scenario']}")
        print(f"Input: {example['input']}")
        
        if example['prompt_type'] == 'feedback':
            result = engine.generate_interview_feedback(example['input'])
        elif example['prompt_type'] == 'summary':
            result = engine.summarize_interview_notes(example['input'])
        elif example['prompt_type'] == 'follow_up':
            result = engine.create_follow_up_questions(example['input'], "System Architecture")
        
        print(f"VMIS Output: {result}")

if __name__ == "__main__":
    main()
