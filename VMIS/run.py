from flask import Flask
import os
from app.routes import bp

# Set the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
