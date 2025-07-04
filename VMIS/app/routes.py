from flask import Blueprint, render_template, request, redirect, url_for
import re

bp = Blueprint('main', __name__)

feedback_list = []  # Temporary storage for feedback

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/feedback')
def feedback():
    return render_template('feedback_form.html', message=None)

@bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    feedback = request.form.get('feedback', '').strip()
    message = None
    if not name or not email or not feedback:
        message = 'All fields are required.'
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        message = 'Please enter a valid email address.'
    else:
        feedback_list.append({'name': name, 'email': email, 'feedback': feedback})
        message = 'Thank you for your feedback!'
    return render_template('feedback_form.html', message=message)
