# Visa Mock Interview System (VMIS) - LLM-Powered Features

A Flask-based web application that provides AI-powered tools for visa interview preparation, including dynamic question generation, intelligent feedback, and session summarization.

## 🚀 Features

### LLM-Powered Features

- **Dynamic Question Generation**: Generate tailored interview questions based on specific topics and difficulty levels
- **Intelligent Feedback**: Get constructive feedback on performance notes using AI analysis
- **Session Summarization**: Transform interview notes into professional summaries with key insights

### Traditional Features

- User management system
- Manual feedback submission and retrieval
- Interview session tracking
- Performance monitoring

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL)
- **LLM Integration**: Google Gemini API
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with responsive design

## 📋 Requirements

- Python 3.8+
- Google API Key (for Gemini LLM)
- Internet connection (for LLM API calls)

## 🔧 Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd VMIS
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

1. Copy the example environment file:

   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and add your configuration:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   DATABASE_URL=sqlite:///vmis.db
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

### 5. Get Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Create a new API key
3. Add the key to your `.env` file

### 6. Initialize Database

```bash
python run.py
```

The database will be automatically created on first run.

## 🚀 Running the Application

### Development Mode

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Production Mode

```bash
set FLASK_ENV=production
python run.py
```

## 📖 API Endpoints

### LLM-Powered Routes

- `GET/POST /llm/generate_questions` - Generate interview questions
- `GET/POST /llm/generate_feedback` - Generate AI feedback
- `GET/POST /llm/summarize_session` - Summarize interview sessions
- `GET /llm/features` - LLM features overview page

### Traditional Routes

- `GET /` - Home page
- `GET /feedback` - Feedback form
- `POST /create_user` - Create new user
- `POST /submit_feedback` - Submit feedback
- `GET /view_feedbacks/<user_id>` - View user feedbacks

## 🧪 Testing

### Run Test Suite

```bash
python test_llm_features.py
```

This will:

- Test input validation for all forms
- Test LLM API integration
- Test error handling scenarios
- Generate a detailed test report (`llm_feature_tests.txt`)

### Manual Testing

1. **Question Generation**:

   - Navigate to `/llm/generate_questions`
   - Enter topic: "communication skills"
   - Select difficulty: "medium"
   - Number of questions: 5

2. **Feedback Generation**:

   - Navigate to `/llm/generate_feedback`
   - Enter performance notes about an interview

3. **Session Summary**:
   - Navigate to `/llm/summarize_session`
   - Enter detailed interview notes

## 📁 Project Structure

```
VMIS/
├── app/
│   ├── models.py              # Database models
│   ├── routes.py              # Traditional routes
│   ├── llm_routes.py          # LLM-powered routes
│   ├── llm_service.py         # LLM API integration
│   ├── static/
│   │   ├── styles.css         # Application styles
│   │   └── script.js          # Client-side JavaScript
│   └── templates/
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── llm_features.html  # LLM features overview
│       ├── generate_questions.html
│       ├── generate_feedback.html
│       └── summarize_session.html
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── test_llm_features.py       # Test suite
├── .env.example              # Environment variables template
├── llm_api_logs.txt          # LLM API interaction logs
├── llm_feature_tests.txt     # Test results
└── README.md                 # This file
```

## 🔒 Security Features

### Input Validation

- **Topic Validation**: Alphanumeric characters, spaces, and basic punctuation only (2-100 chars)
- **Performance Notes**: Minimum 10 characters, maximum 2000 characters
- **Interview Notes**: Minimum 20 characters, maximum 3000 characters
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **XSS Prevention**: Template escaping enabled

### Error Handling

- Comprehensive API error handling
- Network timeout protection (30 seconds)
- Graceful degradation when LLM API is unavailable
- User-friendly error messages
- Detailed logging for debugging

## 📊 Logging and Monitoring

### LLM API Logs

All LLM interactions are logged to `llm_api_logs.txt` including:

- Timestamp
- Input data
- Output data
- Error messages (if any)

### Application Logs

- API errors logged to `api_errors.log`
- Request/response cycles
- Performance metrics

## 🎨 User Interface Features

### Responsive Design

- Mobile-friendly navigation
- Adaptive layouts for different screen sizes
- Touch-friendly buttons and forms

### Interactive Elements

- Real-time character counters
- Loading spinners for LLM operations
- Copy-to-clipboard functionality
- Print-friendly summaries
- Email sharing for summaries

### Accessibility

- Semantic HTML structure
- Proper form labels
- Keyboard navigation support
- High contrast design

## 🔧 Configuration Options

### Environment Variables

```
GOOGLE_API_KEY          # Required: Google Gemini API key
DATABASE_URL            # Optional: Database connection string
FLASK_ENV              # Optional: development/production
FLASK_DEBUG            # Optional: True/False
REQUEST_LIMIT          # Optional: API rate limit per minute
TIME_WINDOW            # Optional: Rate limit time window
```

### LLM Configuration

- **Model**: Google Gemini 2.5 Flash (configurable)
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Max Tokens**: Varies by feature (256-1024)
- **Timeout**: 30 seconds

## 🚨 Troubleshooting

### Common Issues

1. **"Google API key is missing"**

   - Ensure `GOOGLE_API_KEY` is set in `.env` file
   - Verify the API key is valid and active

2. **"Network error or API timeout"**

   - Check internet connection
   - Verify Google API service status
   - Consider increasing timeout in `llm_service.py`

3. **"Database not found"**

   - Ensure `DATABASE_URL` is properly set
   - Run the application once to auto-create SQLite database

4. **"Template not found"**
   - Verify all template files exist in `app/templates/`
   - Check file paths in `run.py`

### Performance Optimization

1. **LLM Response Caching**

   - Responses are cached based on input
   - Clear cache by restarting application

2. **Database Optimization**
   - Use PostgreSQL for production
   - Add database indexes for frequently queried fields

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section
2. Review the test results in `llm_feature_tests.txt`
3. Check API logs in `llm_api_logs.txt`
4. Create an issue on the project repository

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice-to-text interview transcription
- [ ] Advanced analytics dashboard
- [ ] User authentication and authorization
- [ ] Integration with calendar systems
- [ ] Mobile application
- [ ] Advanced LLM model selection
- [ ] Custom prompt templates
- [ ] Interview scoring algorithms

## 📊 Version History

### v1.0.0 (Current)

- Initial LLM-powered features implementation
- Question generation system
- Feedback generation system
- Session summarization
- Comprehensive testing suite
- Responsive web interface

---

**Built with ❤️ for visa interview preparation**
├── test_cases.txt
├── README.md

````

## Setup Instructions

1. Install Python 3.x
2. Install Flask:
   ```bash
   pip install flask
````

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
