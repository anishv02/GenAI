import requests
from bs4 import BeautifulSoup


def fetch_website_contents(url: str) -> str:
    """
    Fetch and extract the main text content from a website.
    
    Args:
        url: The URL of the website to scrape
        
    Returns:
        The extracted text content from the website
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        return text
        
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
