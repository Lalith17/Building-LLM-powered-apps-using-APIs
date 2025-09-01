import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = "models/gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Logging configuration
LOG_FILE = "llm_api_logs.txt"

def log_interaction(input_data, output_data, error=None):
    """Log LLM API interactions to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "input": input_data,
        "output": output_data,
        "error": error
    }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, indent=2) + "\n" + "="*50 + "\n")

def query_llm(prompt, max_tokens=512):
    """Send query to LLM API and return response"""
    if not GOOGLE_API_KEY:
        error_msg = "Google API key is missing. Please set GOOGLE_API_KEY in your environment."
        log_interaction(prompt, None, error_msg)
        return {"error": error_msg}
    
    url = f"{BASE_URL}/{MODEL_ID}:generateContent"
    headers = {"X-goog-api-key": GOOGLE_API_KEY, "Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            error_msg = f"API error: status={response.status_code}, body={response.text}"
            log_interaction(prompt, None, error_msg)
            return {"error": error_msg}
        
        result = response.json()
        
        # Extract text from response
        try:
            candidates = result.get("candidates", [])
            if candidates and len(candidates) > 0:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts and len(parts) > 0:
                    generated_text = parts[0].get("text", "")
                    log_interaction(prompt, generated_text)
                    return {"success": True, "text": generated_text}
        except Exception as e:
            error_msg = f"Error parsing response: {str(e)}"
            log_interaction(prompt, None, error_msg)
            return {"error": error_msg}
        
        error_msg = "Unexpected response format"
        log_interaction(prompt, None, error_msg)
        return {"error": error_msg}
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        log_interaction(prompt, None, error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        log_interaction(prompt, None, error_msg)
        return {"error": error_msg}

def generate_interview_questions(topic, difficulty="medium", count=5):
    """Generate interview questions for a specific topic"""
    prompt = f"""
Generate {count} interview questions for a visa interview focusing on {topic}.
The questions should be at {difficulty} difficulty level and relevant to visa interviews.
Format the response as a numbered list.
Each question should be practical and help assess the candidate's preparation.

Topic: {topic}
Difficulty: {difficulty}
Number of questions: {count}
"""
    
    result = query_llm(prompt, max_tokens=1024)
    if result.get("success"):
        # Parse the questions into a list
        text = result["text"]
        questions = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering and clean up
                clean_question = line.split('.', 1)[-1].strip()
                if clean_question:
                    questions.append(clean_question)
        
        return {"success": True, "questions": questions, "raw_text": text}
    else:
        return result

def generate_feedback(performance_notes):
    """Generate constructive feedback based on performance notes"""
    prompt = f"""
Based on the following performance notes from a visa mock interview, provide constructive feedback.
The feedback should be:
1. Specific and actionable
2. Balanced (highlight both strengths and areas for improvement)
3. Professional and encouraging
4. Structured with clear sections

Performance notes: {performance_notes}

Please structure your feedback with the following sections:
- Strengths
- Areas for Improvement
- Specific Recommendations
- Overall Assessment
"""
    
    result = query_llm(prompt, max_tokens=1024)
    return result

def summarize_session(interview_notes):
    """Summarize interview session notes"""
    prompt = f"""
Summarize the following interview session notes into a concise, professional summary.
The summary should include:
1. Key topics covered
2. Candidate's overall performance
3. Main strengths observed
4. Primary areas needing attention
5. Recommended next steps

Interview notes: {interview_notes}

Please provide a well-structured summary that would be useful for both the candidate and interviewer.
"""
    
    result = query_llm(prompt, max_tokens=768)
    return result
