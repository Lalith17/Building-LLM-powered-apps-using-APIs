# 🎯 VisiPrep: AI-Powered Visa Mock Interview System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![LLM](https://img.shields.io/badge/LLM-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive AI-powered platform designed to help users prepare for visa interviews through intelligent mock interviews, automated feedback generation, and advanced language model integration.

## 🌟 Overview

VisiPrep is a multi-component system that combines traditional web development with cutting-edge AI technologies to provide a complete visa interview preparation experience. The system leverages Large Language Models (LLMs) to generate dynamic questions, provide intelligent feedback, and create comprehensive session summaries.

## 🏗️ System Architecture

```
VisiPrep/
├── 🌐 Landing_Page/          # Modern responsive landing page
├── 🤖 LLM_API/              # Standalone LLM API service
├── 🧠 LLMS/                 # LLM research and evaluation
├── 🛠️ Visa_Mock_Interview_System/  # Basic utility functions
├── 📱 VMIS/                 # Main Flask application
└── 📦 zips/                 # Archived components
```

## 🚀 Key Features

### 🌐 **Landing Page** - User Interface

- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices
- **Dark Mode Toggle**: Persistent theme switching with local storage
- **Contact Form**: Client-side validation with smooth animations
- **Modern UI**: Bootstrap 5 integration with custom CSS animations
- **Accessibility**: FontAwesome icons and semantic HTML structure

### 🤖 **LLM API Integration** - AI Backend

- **Google Gemini Integration**: Advanced text generation and analysis
- **Multiple AI Tasks**: Text generation, summarization, sentiment analysis
- **RESTful API**: Clean endpoints for seamless integration
- **Environment Security**: Secure API key management with .env files
- **Error Handling**: Robust error management and logging

### 🧠 **LLM Research Module** - AI Exploration

- **Text Generation**: GPT-2 based dynamic content creation
- **Sentiment Analysis**: BERT-powered emotion and tone detection
- **Masked Language Modeling**: Context-aware text completion
- **Evaluation Metrics**: BLEU, ROUGE, and Perplexity scoring
- **Custom Prompts**: Specialized prompts for interview scenarios
- **Comprehensive Testing**: Detailed evaluation and performance metrics

### 📱 **Main Application (VMIS)** - Core Platform

- **Dynamic Question Generation**: AI-powered interview questions based on topics
- **Intelligent Feedback**: Constructive AI analysis of user responses
- **Session Summarization**: Professional summaries with key insights
- **User Management**: Complete user registration and session tracking
- **Database Integration**: SQLAlchemy with SQLite/PostgreSQL support
- **Responsive Templates**: Mobile-first design with interactive elements

### 🛠️ **Utility System** - Data Management

- **Input Validation**: Comprehensive data sanitization and validation
- **User Classification**: Age-based categorization system
- **File Operations**: Safe data persistence and retrieval
- **Logging System**: Comprehensive audit trail and error tracking
- **Menu Interface**: User-friendly command-line interaction

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- Google API Key (for Gemini LLM integration)
- Modern web browser (for frontend components)

### Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Lalith17/Building-LLM-powered-apps-using-APIs.git
   cd VisiPrep
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   # For main VMIS application
   cd VMIS
   pip install -r requirements.txt

   # For LLM research module
   cd ../LLMS
   pip install transformers torch datasets evaluate rouge-score sacrebleu nltk numpy pandas

   # For standalone LLM API
   cd ../LLM_API
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   # Create .env file in LLM_API and VMIS directories
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

5. **Initialize Database**

   ```bash
   cd VMIS
   python setup.py
   ```

6. **Run the Application**
   ```bash
   python run.py
   ```

## 🎮 Usage Guide

### Landing Page

1. Open `Landing_Page/index.html` in a web browser
2. Use the navigation menu to explore different sections
3. Toggle dark mode for better viewing experience
4. Fill out the contact form to get started

### Main VMIS Application

1. Navigate to `http://localhost:5000` after running the Flask app
2. Access LLM-powered features from the main dashboard:
   - **Generate Questions**: Create custom interview questions
   - **Get Feedback**: Receive AI-powered performance analysis
   - **Summarize Sessions**: Generate professional session reports

### LLM Research Module

```bash
cd LLMS
python main_runner.py  # Run all LLM tasks
# Or run individual components:
python text_generation.py
python sentiment_analysis.py
python masked_language_modeling.py
```

### Standalone LLM API

```bash
cd LLM_API
python app.py  # Runs on http://127.0.0.1:5000
# Test with curl:
curl -X POST http://127.0.0.1:5000/api/llm_tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "generate_text", "prompt": "Your prompt here"}'
```

## 📊 Component Details

| Component          | Technology Stack                     | Purpose         | Key Features                                          |
| ------------------ | ------------------------------------ | --------------- | ----------------------------------------------------- |
| **Landing Page**   | HTML5, CSS3, Bootstrap 5, JavaScript | User Interface  | Responsive design, dark mode, animations              |
| **LLM API**        | Flask, Google Gemini API, Python     | AI Backend      | Text generation, sentiment analysis, summarization    |
| **LLM Research**   | Transformers, PyTorch, BERT, GPT-2   | AI Research     | Model evaluation, custom prompts, metrics             |
| **VMIS Core**      | Flask, SQLAlchemy, SQLite            | Main Platform   | User management, interview simulation, AI integration |
| **Utility System** | Python, File I/O, Logging            | Data Management | Validation, classification, data persistence          |

## 🧪 Testing

### Automated Tests

```bash
# VMIS application tests
cd VMIS
python test_llm_features.py

# LLM API tests
cd LLM_API
python run_tests.py

# LLM research evaluation
cd LLMS
python main_runner.py  # Includes comprehensive testing
```

### Manual Testing

- Use the provided test cases in each module's `test_cases.txt`
- Check the generated output files for verification
- Review logs for debugging and performance analysis

## 📈 Performance & Monitoring

### Logging

- **Application Logs**: `VMIS/llm_api_logs.txt`
- **Utility Logs**: `Visa_Mock_Interview_System/app_logs.txt`
- **Research Results**: `LLMS/comprehensive_results.json`

### Metrics & Evaluation

- **BLEU Scores**: Translation and text generation quality
- **ROUGE Scores**: Summarization effectiveness
- **Perplexity**: Language model performance
- **Response Times**: API call latency monitoring

## 🛡️ Security Features

- **API Key Management**: Secure environment variable storage
- **Input Validation**: Comprehensive data sanitization
- **Error Handling**: Graceful failure management
- **Logging**: Audit trail for security monitoring

## 🔮 Future Enhancements

- [ ] Multi-language support for international users
- [ ] Voice-based interview simulation
- [ ] Advanced analytics dashboard
- [ ] Integration with additional LLM providers
- [ ] Mobile application development
- [ ] Real-time collaboration features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📚 Quick Navigation

- [🌐 Landing Page Documentation](Landing_Page/README.md)
- [🤖 LLM API Documentation](LLM_API/README.md)
- [🧠 LLM Research Documentation](LLMS/README.md)
- [📱 VMIS Core Documentation](VMIS/README.md)
- [🛠️ Utility System Documentation](Visa_Mock_Interview_System/README.md)

---
