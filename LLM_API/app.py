from flask import Flask, request, jsonify
from llm_integration import generate_text, summarize_text, analyze_sentiment, rate_limit

app = Flask(__name__)

@app.route('/api/llm_tasks', methods=['POST'])
def llm_tasks():
    data = request.get_json()
    
    if not data or 'task' not in data or 'user_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
        
    user_id = data['user_id']
    if rate_limit(user_id):
        return jsonify({"error": "Rate limit exceeded"}), 429
        
    task = data['task']
    
    if task == 'generate_text':
        if 'prompt' not in data:
            return jsonify({"error": "Prompt is required for text generation"}), 400
        result = generate_text(data['prompt'])
    elif task == 'summarize_text':
        if 'text' not in data:
            return jsonify({"error": "Text is required for summarization"}), 400
        result = summarize_text(data['text'])
    elif task == 'analyze_sentiment':
        if 'text' not in data:
            return jsonify({"error": "Text is required for sentiment analysis"}), 400
        result = analyze_sentiment(data['text'])
    else:
        return jsonify({"error": "Invalid task"}), 400
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
