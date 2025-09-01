import os
import requests
import json
import time
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Choose a model that your key can access. Based on your list, use Gemini 2.5 Flash by default.
# Alternatives you can set here: "models/gemini-1.5-flash", "models/gemini-1.5-pro-002", "models/gemini-2.5-flash", etc.
MODEL_ID = "models/gemini-2.5-flash"
# Use the v1beta endpoint and the generateContent method (per docs)
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Caching dictionary
cache = {}

# Rate limiting dictionary
user_requests = {}
REQUEST_LIMIT = 10  # requests per minute
TIME_WINDOW = 60  # seconds


def log_error(error_message):
    with open("api_errors.log", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")


def rate_limit(user_id):
    if user_id not in user_requests:
        user_requests[user_id] = []

    current_time = time.time()
    # Remove requests outside the time window
    user_requests[user_id] = [req_time for req_time in user_requests[user_id] if current_time - req_time < TIME_WINDOW]

    if len(user_requests[user_id]) >= REQUEST_LIMIT:
        return True  # Rate limit exceeded

    user_requests[user_id].append(current_time)
    return False


def query(payload, model_id=MODEL_ID):
    # Simple cache key
    cache_key = (model_id, json.dumps(payload, sort_keys=True))
    if cache_key in cache:
        return cache[cache_key]

    if not GOOGLE_API_KEY:
        error_message = "Google API key is missing. Please set GOOGLE_API_KEY in your environment or .env file."
        log_error(error_message)
        return {"error": error_message}

    # Use the generateContent method path and send the API key in header per docs
    url = f"{BASE_URL}/{model_id}:generateContent"
    headers = {"X-goog-api-key": GOOGLE_API_KEY, "Content-Type": "application/json"}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        # If the API responds with non-2xx, capture the body for debugging
        if resp.status_code < 200 or resp.status_code >= 300:
            body_text = resp.text
            error_message = f"API error: status={resp.status_code}, body={body_text}"
            log_error(error_message)
            return {"error": error_message}
        result = resp.json()

        # Cache the result
        cache[cache_key] = result
        return result

    except requests.exceptions.RequestException as e:
        # include response text if available
        resp_text = ""
        resp_obj = getattr(e, 'response', None)
        try:
            if resp_obj is not None and hasattr(resp_obj, 'text'):
                resp_text = resp_obj.text
        except Exception:
            resp_text = ""
        error_message = f"Network error or API timeout: {e}. Response body: {resp_text}"
        log_error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        log_error(error_message)
        return {"error": error_message}


def _extract_generated_text(response_json):
    # Google Generative API v1/v1beta responses may have different shapes; try common fields
    try:
        # v1beta generateContent may return 'candidates' or 'outputs' or 'content' nested in 'candidates'
        # text-bison / generativelanguage: candidates -> [ { "content": ... } ]
        candidates = response_json.get("candidates")
        if candidates and isinstance(candidates, list) and len(candidates) > 0:
            first = candidates[0]
            if "content" in first:
                return first["content"]
            if "output" in first:
                return first["output"]
        # v1beta may instead include outputs -> [ { "contents": [ { "text": ... } ] } ]
        outputs = response_json.get("outputs")
        if outputs and isinstance(outputs, list) and len(outputs) > 0:
            out0 = outputs[0]
            # try nested contents/parts
            contents = out0.get("contents") or out0.get("candidates")
            if contents and isinstance(contents, list) and len(contents) > 0:
                part0 = contents[0]
                # part0 may have 'text' or 'parts' with parts[0].text
                if "text" in part0:
                    return part0["text"]
                if "parts" in part0 and isinstance(part0["parts"], list) and len(part0["parts"])>0:
                    p = part0["parts"][0]
                    if "text" in p:
                        return p["text"]
        # fallback to text or result fields
        for key in ("output", "text", "generated_text", "content"):
            if key in response_json:
                return response_json[key]
    except Exception:
        pass
    return json.dumps(response_json)


def generate_text(prompt, temperature=0.2, max_output_tokens=256):
    # Use the minimal v1beta payload shape that the API accepts: contents -> parts -> text
    payload = {"contents": [{"parts": [{"text": prompt}] }]}
    resp = query(payload)
    if "error" in resp:
        return resp
    generated = _extract_generated_text(resp)
    return {"generated_text": generated}


def summarize_text(text, max_output_tokens=150):
    instruction = f"Summarize the following feedback into concise bullet points:\n\n{text}"
    payload = {"contents": [{"parts": [{"text": instruction}]}]}
    resp = query(payload)
    if "error" in resp:
        return resp
    summary = _extract_generated_text(resp)
    return {"summary": summary}


def analyze_sentiment(text, max_output_tokens=64):
    instruction = (
        "Classify the sentiment of the following text as Positive, Neutral, or Negative. "
        "Return only one word: Positive, Neutral, or Negative.\n\nText:\n" + text
    )
    payload = {"contents": [{"parts": [{"text": instruction}]}]}
    resp = query(payload)
    if "error" in resp:
        return resp
    label = _extract_generated_text(resp)
    # normalize label
    if isinstance(label, str):
        label_clean = label.strip().split('\n')[0].strip().capitalize()
        if label_clean.lower().startswith('pos'):
            label_clean = 'Positive'
        elif label_clean.lower().startswith('neg'):
            label_clean = 'Negative'
        elif label_clean.lower().startswith('neu'):
            label_clean = 'Neutral'
        return {"sentiment": label_clean}
    return {"sentiment": label}
