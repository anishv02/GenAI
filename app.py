"""
Backend API for Website Summarizer
Supports both local Ollama and cloud Groq API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from scraper import fetch_website_contents
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Determine which LLM to use based on environment
USE_CLOUD = os.getenv('USE_CLOUD', 'false').lower() == 'true'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if USE_CLOUD and GROQ_API_KEY:
    # Use Groq API (cloud) - free and fast!
    llm_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )
    MODEL = "llama-3.1-8b-instant"
    print("☁️ Using Groq Cloud API")
else:
    # Use Ollama (local)
    llm_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    MODEL = "gemma3"
    print("🏠 Using Local Ollama")

# System prompt for summarization
system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""


def messages_for(website_content):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website_content}
    ]


def summarize(url):
    """Fetch website content and generate summary"""
    website_content = fetch_website_contents(url)
    
    if website_content.startswith("Error"):
        return {"error": website_content}
    
    response = llm_client.chat.completions.create(
        model=MODEL,
        messages=messages_for(website_content)
    )
    
    return {"summary": response.choices[0].message.content}


@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint to summarize a website"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        result = summarize(url)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "mode": "cloud" if USE_CLOUD else "local",
        "model": MODEL
    })


@app.route('/')
def index():
    return jsonify({"message": "Website Summarizer API", "health": "/api/health"})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"🚀 Starting Website Summarizer API on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port)
