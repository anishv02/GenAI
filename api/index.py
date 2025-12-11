"""
Vercel Serverless Function for Website Summarizer
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

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


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"status": "ok", "model": MODEL}
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            url = data.get('url', '')
            
            if not url:
                self._send_error(400, "URL is required")
                return
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if not llm_client:
                self._send_error(500, "GROQ_API_KEY not configured")
                return
            
            result = summarize(url)
            
            if "error" in result:
                self._send_error(400, result["error"])
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self._send_error(500, str(e))
    
    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
