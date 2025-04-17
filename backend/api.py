import pandas as pd
import gzip
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import get_hybrid_recommendations, get_book_details
import os
import gc

app = Flask(__name__)

CORS(app, resources={
    r"/recommend_books": {
        "origins": ["http://localhost:3000","https://bookbuddy-pj.vercel.app"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

CORS(app, resources={   
    r"/book/*": {
        "origins": ["http://localhost:3000","https://bookbuddy-pj.vercel.app"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

@app.route('/recommend_books', methods=['GET','POST'])
def recommend_books():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'ageGroup' not in data or 'genre' not in data:
            return jsonify({
                "error": "Missing required fields (ageGroup and genre)"
            }), 400

        age_group = data['ageGroup']
        genre = data['genre']

        recommendations = get_hybrid_recommendations(age_group, genre)
        
        # Handle case when no books are found
        if isinstance(recommendations, dict) and 'error' in recommendations:
            return jsonify(recommendations), 404

        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        gc.collect()
    

@app.route('/book/<book_id>')
def get_book(book_id):
    try:
        # Use the recommender's get_book_details function
        book_details = get_book_details(book_id)
        
        if not book_details:
            return jsonify({"error": "Book not found"}), 404
            
        return jsonify(book_details)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        gc.collect()

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)