from flask import Blueprint, render_template, request, redirect, url_for
import re
from app.models import db, User, Feedback

bp = Blueprint('main', __name__)

feedback_list = []  # Temporary storage for feedback

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/feedback')
def feedback():
    return render_template('feedback_form.html', message=None)

@bp.route('/create_user', methods=['POST'])
def create_user():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    if not name or not email:
        return "Name and email are required", 400
    if User.query.filter_by(email=email).first():
        return "Email already exists", 400
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return "User created successfully", 201

@bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    user_id = request.form.get('user_id', '').strip()
    feedback_text = request.form.get('feedback', '').strip()
    if not user_id or not feedback_text:
        return "User ID and feedback are required", 400
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    feedback = Feedback(user_id=user_id, feedback=feedback_text)
    db.session.add(feedback)
    db.session.commit()
    return "Feedback submitted successfully", 201

@bp.route('/view_feedbacks/<int:user_id>', methods=['GET'])
def view_feedbacks(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    feedbacks = Feedback.query.filter_by(user_id=user_id).all()
    return {"feedbacks": [f.feedback for f in feedbacks]}, 200

@bp.route('/update_feedback/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return "Feedback not found", 404
    feedback_text = request.form.get('feedback', '').strip()
    if not feedback_text:
        return "Feedback text is required", 400
    feedback.feedback = feedback_text
    db.session.commit()
    return "Feedback updated successfully", 200

@bp.route('/delete_feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return "Feedback not found", 404
    db.session.delete(feedback)
    db.session.commit()
    return "Feedback deleted successfully", 200
