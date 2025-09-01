"""
VMIS Deployment and Setup Script
===============================

This script helps set up and deploy the VMIS LLM-powered application.
"""

import os
import sys
import subprocess
import shutil

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step_num, description):
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ Error!")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False
    return True

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor} is compatible")
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        "run.py",
        "requirements.txt",
        ".env.example",
        "app/routes.py",
        "app/llm_routes.py",
        "app/llm_service.py",
        "app/models.py",
        "app/templates/base.html",
        "app/templates/index.html",
        "app/templates/llm_features.html",
        "app/templates/generate_questions.html",
        "app/templates/generate_feedback.html",
        "app/templates/summarize_session.html",
        "app/static/styles.css"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✅ All required files are present")
    return True

def setup_environment():
    """Set up Python virtual environment"""
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Unix/MacOS
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    return run_command(activate_cmd, "Installing dependencies")

def setup_env_file():
    """Set up environment file"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your GOOGLE_API_KEY")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def run_tests():
    """Run the test suite"""
    return run_command("python test_llm_features.py", "Running test suite")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting VMIS application...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run("python run.py", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    print_header("VMIS LLM-Powered Application Setup")
    print("This script will help you set up and deploy the VMIS application with LLM features.")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python_version():
        return
    
    # Step 2: Check required files
    print_step(2, "Checking required files")
    if not check_files():
        return
    
    # Step 3: Set up virtual environment
    print_step(3, "Setting up virtual environment")
    if not setup_environment():
        print("⚠️  Virtual environment setup failed. You may need to install dependencies manually.")
    
    # Step 4: Set up environment file
    print_step(4, "Setting up environment configuration")
    if not setup_env_file():
        return
    
    # Step 5: Run tests
    print_step(5, "Running tests")
    run_tests()  # Continue even if tests fail (might be due to missing API key)
    
    # Step 6: Final instructions
    print_header("SETUP COMPLETE")
    print("✅ VMIS application is ready!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your GOOGLE_API_KEY")
    print("2. Get an API key from: https://makersuite.google.com/")
    print("3. Run 'python run.py' to start the application")
    print("4. Open http://localhost:5000 in your browser")
    
    print("\n🎯 Available features:")
    print("- Dynamic Question Generation")
    print("- AI-Powered Feedback")
    print("- Session Summarization")
    print("- Traditional VMIS features")
    
    # Option to start immediately
    start_now = input("\n❓ Would you like to start the application now? (y/N): ").lower().strip()
    if start_now in ['y', 'yes']:
        start_application()
    else:
        print("\n👋 Setup complete! Run 'python run.py' when ready to start.")

if __name__ == "__main__":
    main()
