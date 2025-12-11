"""
Vercel Serverless Function for Website Summarizer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Use Groq API (cloud)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if GROQ_API_KEY:
    llm_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )
    MODEL = "llama-3.1-8b-instant"
else:
    llm_client = None
    MODEL = None

# System prompt
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


def fetch_website_contents(url):
    """Fetch and extract text content from a website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines)
        
        return clean_text[:8000]
    except Exception as e:
        return f"Error fetching website: {str(e)}"


def messages_for(website_content):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website_content}
    ]


def summarize(url):
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
    try:
        if not llm_client:
            return jsonify({"error": "GROQ_API_KEY not configured"}), 500
            
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
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
    return jsonify({
        "status": "ok",
        "model": MODEL
    })


@app.route('/')
def index():
    return jsonify({"message": "Website Summarizer API"})
