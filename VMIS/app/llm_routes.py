from flask import Blueprint, render_template, request, jsonify, flash
import re
from app.llm_service import generate_interview_questions, generate_feedback, summarize_session

llm_bp = Blueprint('llm', __name__, url_prefix='/llm')

def validate_topic(topic):
    """Validate topic input using regex"""
    if not topic or len(topic.strip()) == 0:
        return False, "Topic cannot be empty"
    
    # Allow alphanumeric characters, spaces, hyphens, and common punctuation
    pattern = r'^[a-zA-Z0-9\s\-.,()]+$'
    if not re.match(pattern, topic.strip()):
        return False, "Topic contains invalid characters. Only letters, numbers, spaces, and basic punctuation are allowed"
    
    if len(topic.strip()) < 2:
        return False, "Topic must be at least 2 characters long"
    
    if len(topic.strip()) > 100:
        return False, "Topic must be less than 100 characters"
    
    return True, None

def validate_performance_notes(notes):
    """Validate performance notes input"""
    if not notes or len(notes.strip()) == 0:
        return False, "Performance notes cannot be empty"
    
    if len(notes.strip()) < 10:
        return False, "Performance notes must be at least 10 characters long"
    
    if len(notes.strip()) > 2000:
        return False, "Performance notes must be less than 2000 characters"
    
    return True, None

def validate_interview_notes(notes):
    """Validate interview notes input"""
    if not notes or len(notes.strip()) == 0:
        return False, "Interview notes cannot be empty"
    
    if len(notes.strip()) < 20:
        return False, "Interview notes must be at least 20 characters long"
    
    if len(notes.strip()) > 3000:
        return False, "Interview notes must be less than 3000 characters"
    
    return True, None

@llm_bp.route('/features')
def llm_features():
    """Display the LLM features page"""
    return render_template('llm_features.html')

@llm_bp.route('/generate_questions', methods=['GET', 'POST'])
def generate_questions_route():
    """Generate interview questions based on topic"""
    if request.method == 'GET':
        return render_template('generate_questions.html')
    
    try:
        # Get form data
        topic = request.form.get('topic', '').strip()
        difficulty = request.form.get('difficulty', 'medium').strip()
        count = request.form.get('count', '5')
        
        # Validate inputs
        is_valid, error_message = validate_topic(topic)
        if not is_valid:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 400
            return render_template('generate_questions.html', error=error_message)
        
        # Validate count
        try:
            count = int(count)
            if count < 1 or count > 10:
                raise ValueError("Count must be between 1 and 10")
        except ValueError:
            error_message = "Number of questions must be a valid number between 1 and 10"
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 400
            return render_template('generate_questions.html', error=error_message)
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        # Generate questions
        result = generate_interview_questions(topic, difficulty, count)
        
        if result.get("success"):
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({
                    "success": True, 
                    "questions": result["questions"],
                    "topic": topic,
                    "difficulty": difficulty
                })
            return render_template('generate_questions.html', 
                                 questions=result["questions"],
                                 topic=topic,
                                 difficulty=difficulty,
                                 success=True)
        else:
            error_message = result.get("error", "Failed to generate questions")
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 500
            return render_template('generate_questions.html', error=error_message)
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"success": False, "error": error_message}), 500
        return render_template('generate_questions.html', error=error_message)

@llm_bp.route('/generate_feedback', methods=['GET', 'POST'])
def generate_feedback_route():
    """Generate feedback based on performance notes"""
    if request.method == 'GET':
        return render_template('generate_feedback.html')
    
    try:
        # Get form data
        performance_notes = request.form.get('performance_notes', '').strip()
        
        # Validate input
        is_valid, error_message = validate_performance_notes(performance_notes)
        if not is_valid:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 400
            return render_template('generate_feedback.html', error=error_message)
        
        # Generate feedback
        result = generate_feedback(performance_notes)
        
        if result.get("success"):
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({
                    "success": True, 
                    "feedback": result["text"]
                })
            return render_template('generate_feedback.html', 
                                 feedback=result["text"],
                                 success=True)
        else:
            error_message = result.get("error", "Failed to generate feedback")
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 500
            return render_template('generate_feedback.html', error=error_message)
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"success": False, "error": error_message}), 500
        return render_template('generate_feedback.html', error=error_message)

@llm_bp.route('/summarize_session', methods=['GET', 'POST'])
def summarize_session_route():
    """Summarize interview session notes"""
    if request.method == 'GET':
        return render_template('summarize_session.html')
    
    try:
        # Get form data
        interview_notes = request.form.get('interview_notes', '').strip()
        
        # Validate input
        is_valid, error_message = validate_interview_notes(interview_notes)
        if not is_valid:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 400
            return render_template('summarize_session.html', error=error_message)
        
        # Generate summary
        result = summarize_session(interview_notes)
        
        if result.get("success"):
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({
                    "success": True, 
                    "summary": result["text"]
                })
            return render_template('summarize_session.html', 
                                 summary=result["text"],
                                 success=True)
        else:
            error_message = result.get("error", "Failed to generate summary")
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "error": error_message}), 500
            return render_template('summarize_session.html', error=error_message)
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"success": False, "error": error_message}), 500
        return render_template('summarize_session.html', error=error_message)
