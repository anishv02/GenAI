import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

// Use environment variable for API URL, fallback to localhost for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submittedUrl, setSubmittedUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError('');
    setSummary('');
    setSubmittedUrl(url);

    try {
      const response = await fetch(`${API_URL}/api/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to summarize website');
      }

      setSummary(data.summary);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">🔮</div>
        </div>
        <h1>Website Summarizer</h1>
        <p>
          Drop any URL and get an instant AI-powered summary. 
          No more endless scrolling through web pages.
        </p>
        <div className="powered-by">
          ⚡ Powered by <span>Ollama + Gemma3</span>
        </div>
      </header>

      <main className="main-container">
        <section className="input-section">
          <form onSubmit={handleSubmit}>
            <div className="input-wrapper">
              <input
                type="text"
                className="url-input"
                placeholder="Paste website URL here... (e.g., https://example.com)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={loading}
              />
              <button 
                type="submit" 
                className="submit-btn"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="spinner"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <span className="icon">✨</span>
                    Summarize
                  </>
                )}
              </button>
            </div>
          </form>
        </section>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {summary && (
          <section className="result-section">
            <div className="result-header">
              <h3>
                <span>📄</span>
                Summary
              </h3>
              <span className="url-badge">{submittedUrl}</span>
            </div>
            <div className="result-content">
              <div className="markdown-content">
                <ReactMarkdown>{summary}</ReactMarkdown>
              </div>
            </div>
          </section>
        )}

        {!summary && !loading && !error && (
          <div className="features">
            <div className="feature-card">
              <div className="icon">🚀</div>
              <h4>Lightning Fast</h4>
              <p>Get summaries in seconds with local AI processing</p>
            </div>
            <div className="feature-card">
              <div className="icon">🔒</div>
              <h4>100% Private</h4>
              <p>Everything runs locally on your machine</p>
            </div>
            <div className="feature-card">
              <div className="icon">💰</div>
              <h4>Completely Free</h4>
              <p>No API costs, no subscriptions needed</p>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>
          Built with React + Flask + Ollama | 
          <a href="https://github.com/anishv02/GenAI" target="_blank" rel="noopener noreferrer"> View on GitHub</a>
        </p>
      </footer>
    </div>
  );
}

export default App;
