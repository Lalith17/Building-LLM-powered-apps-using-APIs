"""
VMIS LLM Features Demonstration Script
=====================================

This script demonstrates the LLM-powered features of the Visa Mock Interview System.
Run this script to see example outputs from each feature.

Note: Requires GOOGLE_API_KEY to be set in the .env file
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.llm_service import generate_interview_questions, generate_feedback, summarize_session

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demo_question_generation():
    print_section("QUESTION GENERATION DEMO")
    
    topics = [
        ("communication skills", "medium", 3),
        ("technical knowledge", "hard", 2),
        ("travel purpose", "easy", 4)
    ]
    
    for topic, difficulty, count in topics:
        print(f"\n🎯 Topic: {topic}")
        print(f"📊 Difficulty: {difficulty}")
        print(f"🔢 Count: {count}")
        print("-" * 40)
        
        result = generate_interview_questions(topic, difficulty, count)
        
        if result.get("success"):
            questions = result.get("questions", [])
            for i, question in enumerate(questions, 1):
                print(f"{i}. {question}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        print()

def demo_feedback_generation():
    print_section("FEEDBACK GENERATION DEMO")
    
    performance_notes = """
    The candidate demonstrated strong verbal communication skills and maintained good eye contact throughout the interview. They provided clear, detailed answers to questions about their travel purpose and showed comprehensive knowledge of their destination country.

    Strengths observed:
    - Confident speaking voice
    - Well-prepared documentation
    - Clear travel itinerary
    - Strong ties to home country

    Areas for improvement:
    - Seemed slightly nervous when discussing financial details
    - Could provide more specific examples of previous travel experience
    - Body language became tense during complex questions

    Overall impression: Well-prepared candidate with good potential for visa approval.
    """
    
    print("📝 Performance Notes:")
    print(performance_notes)
    print("\n" + "-" * 40)
    print("🤖 Generated Feedback:")
    
    result = generate_feedback(performance_notes)
    
    if result.get("success"):
        print(result["text"])
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

def demo_session_summary():
    print_section("SESSION SUMMARY DEMO")
    
    interview_notes = """
    Interview Session - Visa Application Assessment
    Date: September 1, 2025
    Duration: 30 minutes
    
    Questions Asked:
    1. Purpose of visit - Candidate explained business conference attendance
    2. Duration of stay - Clearly stated 10-day visit
    3. Financial situation - Provided bank statements and sponsor letter
    4. Employment status - Confirmed current job with 3-year tenure
    5. Previous travel history - Mentioned visits to Canada and UK
    6. Ties to home country - Discussed family, property ownership, job responsibilities
    
    Candidate Responses:
    - Very articulate and confident in communication
    - Provided comprehensive documentation package
    - Demonstrated clear understanding of visa requirements
    - Showed genuine purpose for travel
    - Maintained professional demeanor throughout
    
    Documentation Provided:
    - Valid passport with 18 months validity
    - Bank statements showing sufficient funds
    - Employment letter and salary certificate
    - Hotel reservations and return flight tickets
    - Conference invitation letter
    
    Interviewer Observations:
    - Candidate was well-prepared and organized
    - Responses were consistent and believable
    - No red flags or concerning behaviors noted
    - Strong evidence of intent to return to home country
    
    Recommendation: Positive assessment for visa approval
    Risk level: Low
    """
    
    print("📋 Interview Notes:")
    print(interview_notes)
    print("\n" + "-" * 40)
    print("📊 Generated Summary:")
    
    result = summarize_session(interview_notes)
    
    if result.get("success"):
        print(result["text"])
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

def main():
    print("🚀 VMIS LLM Features Demonstration")
    print("This demonstration shows the capabilities of the AI-powered features.")
    print("\nNote: If you see API errors, ensure your GOOGLE_API_KEY is set in the .env file")
    
    try:
        demo_question_generation()
        demo_feedback_generation() 
        demo_session_summary()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✅ All features have been demonstrated!")
        print("\n🌐 To use these features interactively:")
        print("1. Run: python run.py")
        print("2. Open: http://localhost:5000")
        print("3. Navigate to LLM Features section")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        print("\nThis might be due to:")
        print("- Missing GOOGLE_API_KEY in .env file")
        print("- Network connectivity issues") 
        print("- LLM API service unavailable")

if __name__ == "__main__":
    main()
