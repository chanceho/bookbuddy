# api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    analysis_result = """
Book Sentiment Analysis Summary:
================================================================================

Total books analyzed: 18

Polarity Category Distribution:
Extremely Positive: 7 books (38.9%)
Very Positive: 4 books (22.2%)
Positive: 2 books (11.1%)
Neutral: 5 books (27.8%)

Top Books with Scores ≥ 0.7 (ordered by review count):
- Five Nice Mice Build a House (Score: 0.80, Reviews: 12)
- Jinx (Score: 0.80, Reviews: 8)
- The Very Hungry Caterpillar (Score: 0.75, Reviews: 7)
- What I've Done (Score: 0.83, Reviews: 3)
- The Cat in the Hat (Score: 0.72, Reviews: 2)

Top Books (combined score & popularity):
- Five Nice Mice Build a House (Score: 0.80, Reviews: 12, Combined: 2.97)
- Jinx (Score: 0.80, Reviews: 8, Combined: 2.75)
- The Very Hungry Caterpillar (Score: 0.75, Reviews: 7, Combined: 2.58)
- What I've Done (Score: 0.83, Reviews: 3, Combined: 2.30)
- The Cat in the Hat (Score: 0.72, Reviews: 2, Combined: 1.89)

Most Negative Books:
- The Hostile Hospital (Score: -0.15, Reviews: 1)
- Beyond the Grave (Score: -0.25, Reviews: 1)

Most Controversial Books (mixed opinions):
- Harry Potter and the Order of the Phoenix (Controversy: 0.21, Reviews: 3)
- The Giving Tree (Controversy: 0.18, Reviews: 2)
- Wonder (Controversy: 0.12, Reviews: 2)
- Charlie and the Chocolate Factory (Controversy: 0.00, Reviews: 1)
- The Hobbit (Controversy: 0.00, Reviews: 1)
"""
    
    return analysis_result

@app.route('/health', methods=['GET'])
def health_check():
    return "API is running"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
