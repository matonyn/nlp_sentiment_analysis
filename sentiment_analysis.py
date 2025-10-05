from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('sentiment.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        def preprocess_text(text):
            text = text.lower() # Lowercase
            text = re.sub(r'[^\w\s]', ' ', text) # Remove punctuation
            text = re.sub(r'\(.*?\)', ' ', text) # remove parentheses
            return text
        text = preprocess_text(text)
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            sentiment_label = 'Positive'
        elif sentiment < 0:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'
        return jsonify({'sentiment': sentiment_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)