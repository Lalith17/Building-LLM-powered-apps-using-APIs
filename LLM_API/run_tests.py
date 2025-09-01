import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

from llm_integration import generate_text, summarize_text, analyze_sentiment

OUTFILE = 'api_test_results.txt'

TESTS = [
    {
        'name': 'Text Generation - leadership follow-up',
        'type': 'generate_text',
        'input': 'Generate a follow-up question for: Explain a situation where you demonstrated leadership skills.'
    },
    {
        'name': 'Text Generation - teamwork',
        'type': 'generate_text',
        'input': 'Generate an interview question about teamwork.'
    },
    {
        'name': 'Summarization - feedback block',
        'type': 'summarize_text',
        'input': (
            'The Visa Mock Interview System is a comprehensive platform designed to help users prepare for visa interviews. '
            'It offers a realistic simulation of the interview process, complete with a wide range of questions covering various aspects '
            'of the visa application. The system also provides detailed feedback on user performance, highlighting areas of strength and '
            'suggesting improvements. By using this system, applicants can build their confidence and significantly increase their chances of success.'
        )
    },
    {
        'name': 'Sentiment Analysis - positive feedback',
        'type': 'analyze_sentiment',
        'input': 'I found the feedback from the mock interview to be incredibly helpful. It was detailed, constructive, and gave me a clear understanding of what I need to work on.'
    },
    {
        'name': 'Summarization - longer text',
        'type': 'summarize_text',
        'input': (
            'The new LLM integration feature has been a game-changer for our platform. It allows us to provide more intelligent and personalized feedback to our users. '
            'The text generation capability helps us create a vast and diverse question bank, while the summarization feature makes it easy for users to digest their performance reports. '
            'The sentiment analysis tool has also been invaluable in gauging user satisfaction and identifying areas where we can improve. Overall, the integration has been a resounding success, and we are excited to explore more ways to leverage the power of LLMs in the future.'
        )
    }
]


def run_test(test):
    ttype = test['type']
    inp = test['input']
    try:
        if ttype == 'generate_text':
            out = generate_text(inp)
        elif ttype == 'summarize_text':
            out = summarize_text(inp)
        elif ttype == 'analyze_sentiment':
            out = analyze_sentiment(inp)
        else:
            out = {'error': 'Unknown test type'}
    except Exception as e:
        out = {'error': str(e)}
    return out


def append_result(name, test_input, output, observation):
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    with open(OUTFILE, 'a', encoding='utf-8') as f:
        f.write(f"Test: {name}\n")
        f.write(f"Timestamp: {ts}\n")
        f.write(f"Input: {test_input}\n")
        f.write(f"Output: {output}\n")
        f.write(f"Observations: {observation}\n")
        f.write("---\n\n")


if __name__ == '__main__':
    print('Running LLM API tests...')
    summary = []
    for test in TESTS:
        print(f"Running: {test['name']}")
        result = run_test(test)
        # create a short observation
        if isinstance(result, dict) and 'error' in result:
            obs = f"Error: {result['error']}"
        else:
            obs = 'Success'
        append_result(test['name'], test['input'], result, obs)
        summary.append((test['name'], obs))
        # small delay to avoid rapid-fire
        time.sleep(1)

    print('\nTest Summary:')
    for name, obs in summary:
        print(f"- {name}: {obs}")
    print(f"Results appended to {OUTFILE}")
