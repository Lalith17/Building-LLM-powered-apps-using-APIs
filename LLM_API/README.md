# LLM API Integration for Visa Mock Interview System

This project integrates a Large Language Model (LLM) API into the Visa Mock Interview System (VMIS) to provide intelligent features like text generation, summarization, and sentiment analysis.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository/LLM_API
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the API key (Google Gemini):**
    - Create a `.env` file in the `LLM_API` directory.
    - Add the following line to the `.env` file:
      ```
      GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
      ```
    - Replace `"YOUR_GOOGLE_API_KEY"` with your actual Google Generative API key.

## Running the Application

To run the Flask application, execute the following command in the `LLM_API` directory:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Testing the Functionality (Gemini)

You can test the API endpoint using a tool like `curl` or Postman. The local Flask route is unchanged: `/api/llm_tasks`.

### Example Request (curl)

```bash
curl -X POST http://127.0.0.1:5000/api/llm_tasks \
-H "Content-Type: application/json" \
-d '{
    "user_id": "test_user",
    "task": "generate_text",
    "prompt": "Generate a follow-up question for: Explain a situation where you demonstrated leadership skills."
}'
```

### Direct Gemini test (curl)

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1/models/text-bison-001:generate?key=YOUR_GOOGLE_API_KEY" \
-H "Content-Type: application/json" \
-d '{"prompt":{"text":"Generate a follow-up question for: Explain a situation where you demonstrated leadership skills."}}'
```

Replace `YOUR_GOOGLE_API_KEY` with the key you put in `.env`.

## Flowchart

Here is a flowchart illustrating the API interaction and caching mechanism:

![Flowchart](flowchart.png)
