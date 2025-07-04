# VMIS Flask Application

## Overview

This is a basic Flask backend for the Visa Mock Interview System (VMIS). It handles user feedback and renders dynamic content using Jinja2 templates.

## Project Structure

```
VMIS/
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── feedback_form.html
│   ├── static/
│   │   ├── styles.css
│   │   ├── script.js
│   ├── routes.py
├── run.py
├── test_cases.txt
├── README.md
```

## Setup Instructions

1. Install Python 3.x
2. Install Flask:
   ```bash
   pip install flask
   ```
3. Run the application:
   ```bash
   python run.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000/`

## Features

- Home page with welcome message
- Feedback form with validation
- Success/error messages after submission
- Simple navigation and styling

## Test Cases

See `test_cases.txt` for example inputs and expected outputs.

## Notes

- Feedback is stored in memory (not persistent).
- For advanced tasks, you can save feedback to a file or database.
