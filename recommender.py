# recommender.py

# === 1. IMPORTS ===
import pandas as pd
import numpy as np
import json
import re
import math
import textstat
import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# === 2. GLOBAL DATA LOADING ===
columns_of_interest_books = ['book_id', 'title', 'average_rating', 'ratings_count','description', 'num_pages', 'popular_shelves','image_url','authors']
json_files_books = ['goodreads_books_children_sample.json', 'goodreads_books_young_adult_sample.json']
data_books = []

for json_file in json_files_books:
    with open(json_file, 'r') as file:
        for line in file:
            record = json.loads(line)
            filtered_record = {key:record[key] for key in columns_of_interest_books}
            data_books.append(filtered_record)

books = pd.DataFrame(data_books)
books['description_length'] = books['description'].apply(len)
books = books[books['description_length'] != 0]
books = books.drop('description_length', axis=1)

columns_of_interest_authors = ['author_id', 'name']
data_authors = []
with open('goodreads_book_authors.json', 'r') as file:
    for line in file:
        record = json.loads(line)
        filtered_record = {key:record[key] for key in columns_of_interest_authors}
        data_authors.append(filtered_record)
authors = pd.DataFrame(data_authors)

def get_name(author_id):
    if author_id in authors['author_id'].values:
        return authors.loc[authors['author_id'] == author_id, 'name'].values[0]
    return None

columns_of_interest_interactions = ['user_id','book_id','is_read','rating']
json_files_interactions = ['goodreads_interactions_children_sample.json', 'goodreads_interactions_young_adult_sample.json']
data_interactions = []
for json_file in json_files_interactions:
    with open(json_file, 'r') as file:
        for line in file:
            record = json.loads(line)
            filtered_record = {key:record[key] for key in columns_of_interest_interactions}
            data_interactions.append(filtered_record)
interactions = pd.DataFrame(data_interactions)
interactions = interactions[interactions['is_read'] != 0]

# === 3. TEXT HELPERS ===
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    lemmatizer = WordNetLemmatizer()
    word_list = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(word) for word in word_list])

def load_nlp_models():
    try:
        return spacy.load("en_core_web_sm")
    except:
        try:
            spacy.cli.download("en_core_web_sm")
            return spacy.load("en_core_web_sm")
        except:
            return None

# === 4. GENRE DETECTION ===
def detect_book_genre_with_advanced_nlp(book_data, genre_classifier=None, min_confidence=3, exclude_shelves=None):
    if exclude_shelves is None:
        exclude_shelves = get_default_excluded_shelves()
    # Extract genres from structured shelf data
    shelf_genres = extract_genres_from_shelves(book_data, get_genre_map(), exclude_shelves)
    title = str(book_data.get('title', ''))
    description = str(book_data.get('description', ''))

    nlp_genres = {}
    # Only perform NLP analysis if we have enough text
    if len(shelf_genres) < 4 & len(description) > 500:
        nlp_genres.update(analyze_with_tfidf(title, description))
        nlp_genres.update(extract_named_entities(title, description))
    # Combine all signals and apply minimum confidence threshold
    final_genres = combine_all_genre_signals(shelf_genres, nlp_genres, min_confidence)
    return final_genres[:3]

def get_default_excluded_shelves():
    # removes shelf names that aren't useful for genre classification
    return {
        'to-read', 'currently-reading', 'owned', 'default',
        'favorites', 'books-i-own', 'ebook', 'kindle',
        'library', 'audiobook', 'owned-books', 'to-buy',
        'calibre', 're-read', 'unread', 'favourites', 'my-books'
    }

def get_genre_map():
    # Dictionary mapping shelf keywords to standardized genre names
    return {
        'fantasy': 'Fantasy',
        'sci-fi': 'Science Fiction',
        'science-fiction': 'Science Fiction',
        'mystery': 'Mystery/Thriller',
        'thriller': 'Mystery/Thriller',
        'romance': 'Romance',
        'historical': 'Historical Fiction',
        'history': 'History',
        'horror': 'Horror',
        'young-adult': 'Young Adult',
        'ya': 'Young Adult',
        'childrens': 'Children\'s',
        'children': 'Children\'s',
        'kids': 'Children\'s',
        'dystopian': 'Dystopian',
        'classic': 'Classics',
        'classics': 'Classics',
        'biography': 'Biography/Memoir',
        'memoir': 'Biography/Memoir',
        'autobiography': 'Biography/Memoir',
        'self-help': 'Self Help',
        'business': 'Business',
        'philosophy': 'Philosophy',
        'psychology': 'Psychology',
        'science': 'Science',
        'poetry': 'Poetry',
        'comic': 'Comics/Graphic Novels',
        'graphic-novel': 'Comics/Graphic Novels',
        'manga': 'Manga',
        'cooking': 'Cooking/Food',
        'cookbook': 'Cooking/Food',
        'food': 'Cooking/Food',
        'travel': 'Travel',
        'religion': 'Religion/Spirituality',
        'spirituality': 'Religion/Spirituality',
        'art': 'Art/Photography',
        'photography': 'Art/Photography',
        'reference': 'Reference',
        'textbook': 'Textbook/Education',
        'education': 'Textbook/Education'
    }

def extract_genres_from_shelves(book_data, genre_map, exclude_shelves):
    # Extract genre information from book's popular shelves data by using shelf counts as confidence scores (more users shelving = higher confidence)
    shelf_genres = {}
    popular_shelves = book_data.get('popular_shelves', [])
    if isinstance(popular_shelves, list) and popular_shelves:
        for shelf in popular_shelves:
            shelf_name = shelf.get('name', '').strip().lower()
            shelf_count = int(shelf.get('count', 0))

            if shelf_name in exclude_shelves:
                continue

            for keyword, genre_name in genre_map.items():
                if keyword in shelf_name:
                    if genre_name in shelf_genres:
                        shelf_genres[genre_name] += shelf_count
                    else:
                        shelf_genres[genre_name] = shelf_count
                    break
    return shelf_genres


def preprocess_text(text, lemmatize=True):
    """
    Preprocess text by removing special characters, lemmatizing, etc. We convert text to lowercase, remove URLs and HTML tags, remove non-alphabetic
    characters, normalize whitespace and optionally lemmatize words (reduce to base form)
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        word_list = nltk.word_tokenize(text)
        text = ' '.join([lemmatizer.lemmatize(word) for word in word_list])
    return text


def load_nlp_models():
    # Load spaCy models required for named entity recognition
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        try:
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        except:
            nlp = None
    return nlp


def analyze_with_tfidf(title, description):
    """
    Analyze book text using TF-IDF comparison against genre-specific vocabulary.

    Algorithm:
    1. Define genre-specific keyword sets
    2. Preprocess the book text (title + description)
    3. Create TF-IDF vectors for genre keywords and book text
    4. Calculate cosine similarity between book vector and each genre vector
    5. Convert similarities to confidence scores and return top matches
    """
    try:
        # Define genre keyword sets
        genre_keywords = {
            'Fantasy': 'magic wizard dragon elf quest sword magical kingdom witch sorcery myth fantasy',
            'Science Fiction': 'space alien future technology robot dystopian sci-fi futuristic planet spacecraft',
            'Mystery/Thriller': 'murder detective crime case investigation killer suspense clue mystery conspiracy',
            'Romance': 'love relationship passion romantic heart affair marriage emotion desire dating romance',
            'Historical Fiction': 'century historical period king queen ancient war empire era medieval history',
            'Horror': 'fear terror ghost scary monster supernatural haunt nightmare blood evil dark horror',
            'Young Adult': 'teen school young coming-of-age adolescent teenage youth friendship high-school',
            'Children\'s': 'child kid young picture-book learning bedtime simple adventure colorful illustrated',
            'Biography/Memoir': 'life autobiography personal real journey memoir experience story true figure',
            'Self Help': 'improve success happiness guide advice life motivation habit inspiration growth',
            'Business': 'market company entrepreneur success management leadership strategy finance career investment',
            'Dystopian': 'dystopia future society control survival oppression rebellion totalitarian apocalyptic regime'
        }

        # Preprocess text
        processed_text = preprocess_text(f"{title} {description}")

        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

        # Create corpus with genre keywords and the book text
        corpus = list(genre_keywords.values())
        corpus.append(processed_text)

        # Calculate TF-IDF
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Calculate similarity between book and each genre
        last_row_index = tfidf_matrix.shape[0] - 1
        similarities = cosine_similarity(tfidf_matrix[last_row_index], tfidf_matrix[:-1])[0]

        # Map similarities to genres
        genres = {}
        for i, genre in enumerate(genre_keywords.keys()):
            # Convert similarity scores to a more intuitive range (0-10)
            score = int(similarities[i] * 10)
            if score > 3:  # Only consider reasonable matches
                genres[genre] = score

        return genres
    except:
        return {}


def extract_named_entities(title, description):
    # Extract named entities from book text, use spaCy NLP model to process text and extract named entities before and mapping them to potential genres.
    try:
        nlp = load_nlp_models()
        if not nlp:
            return {}

        # Process text with spaCy
        doc = nlp(f"{title} {description}")

        # Extract entities
        entities = [ent.text.lower() for ent in doc.ents]

        # Define entity-genre associations
        entity_genre_map = {
            'fantasy': ['magic', 'wizard', 'dragon', 'elf', 'fairy', 'kingdom', 'quest', 'sorcerer'],
            'science fiction': ['space', 'planet', 'alien', 'robot', 'future', 'technology'],
            'historical fiction': ['century', 'king', 'queen', 'empire', 'war', 'battle', 'medieval', 'ancient'],
            'biography': ['life', 'biography', 'autobiography', 'memoir', 'president', 'politician', 'artist'],
            'science': ['research', 'experiment', 'theory', 'physics', 'biology', 'chemistry', 'scientist'],
            'religion': ['god', 'church', 'bible', 'faith', 'spiritual', 'religion', 'prayer']
        }

        # Find genres based on entities
        genres = {}
        for entity in entities:
            for genre, keywords in entity_genre_map.items():
                if any(keyword in entity for keyword in keywords):
                    standardized_genre = standardize_genre(genre)
                    genres[standardized_genre] = genres.get(standardized_genre, 0) + 1

        return genres
    except:
        return {}


def standardize_genre(genre):
    # Standardize genre names to a consistent format.
    genre_map = {
        'fantasy': 'Fantasy',
        'science fiction': 'Science Fiction',
        'historical fiction': 'Historical Fiction',
        'biography': 'Biography/Memoir',
        'science': 'Science',
        'religion': 'Religion/Spirituality'
    }
    return genre_map.get(genre.lower(), genre.title())


def combine_all_genre_signals(shelf_genres, nlp_genres, min_confidence):
    # Combine genre signals from different sources with appropriate weights.
    combined_scores = Counter()
    # Add shelf genres with the highest weight (explicit human categorization)
    for genre, score in shelf_genres.items():
        combined_scores[genre] += score * 3
    # Add NLP-detected genres with medium weight
    for genre, score in nlp_genres.items():
        combined_scores[genre] += score * 2
    # Sort by final score
    sorted_genres = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    # Filter by minimum confidence
    final_genres = [genre for genre, score in sorted_genres if score >= min_confidence]
    # Fallback if no confident genres
    if not final_genres and sorted_genres:
        final_genres = [sorted_genres[0][0]]
    return final_genres

# === 5. AGE DETECTION ===
def detect_age_range(book_data):
    if book_data.get('popular_shelves') is None:
        book_data['popular_shelves'] = []

    title = str(book_data.get('title', ''))
    description = str(book_data.get('description', ''))
    num_pages = book_data['num_pages']

    try:
        num_pages = int(book_data['num_pages'])
    except (KeyError, ValueError, TypeError):
        num_pages = 0

    age_scores = {
        '0-5': 0,
        '6-10': 0,
        '11-15': 0,
        '15+': 0
    }

    title_lower = title.lower()
    description_lower = description.lower()

    # Advanced NLP analysis of title and description
    title_complexity = analyze_text_complexity(title)
    desc_complexity = analyze_text_complexity(description)

    # Apply title complexity to age scores
    if title_complexity < 0.3:
        age_scores['0-5'] += 10
        age_scores['6-10'] += 5
    elif title_complexity < 0.5:
        age_scores['6-10'] += 8
        age_scores['0-5'] += 4
    elif title_complexity < 0.7:
        age_scores['11-15'] += 8
        age_scores['6-10'] += 4
    else:
        age_scores['15+'] += 8
        age_scores['11-15'] += 4

    # Apply description complexity to age scores
    if desc_complexity < 0.3:
        age_scores['0-5'] += 12
        age_scores['6-10'] += 6
    elif desc_complexity < 0.5:
        age_scores['6-10'] += 10
        age_scores['0-5'] += 5
    elif desc_complexity < 0.7:
        age_scores['11-15'] += 10
        age_scores['6-10'] += 5
    else:
        age_scores['15+'] += 12
        age_scores['11-15'] += 6

    # POS tag patterns analysis for age appropriateness
    pos_patterns = analyze_pos_patterns(description)
    for age_range, score in pos_patterns.items():
        age_scores[age_range] += score

    board_book_terms = ['board book', 'bedtime', 'goodnight', 'naptime', 'toddler', 'baby',
                        'alphabet', 'counting', 'colors', 'shapes', 'lullaby', 'nursery']

    if any(term in title_lower or term in description_lower for term in board_book_terms):
        age_scores['0-5'] += 12
        age_scores['6-10'] -= 5

    early_reader_terms = ['early reader', 'beginning reader', 'learn to read', 'level reader',
                          'first reader', 'step into reading', 'i can read', 'reading level']

    if any(term in title_lower or term in description_lower for term in early_reader_terms):
        age_scores['6-10'] += 12
        age_scores['0-5'] -= 2

    grade_terms = {
        '0-5': ['preschool', 'pre-k', 'kindergarten'],
        '6-10': ['grade 1', 'grade 2', 'grade 3', 'grade 4', 'first grade', 'second grade',
                 'third grade', 'fourth grade', 'fifth grade', 'elementary'],
        '11-15': ['grade 5', 'grade 6', 'grade 7', 'grade 8', 'middle school', 'middle-grade',
                  'middle grade', 'tween'],
        '15+': ['grade 9', 'grade 10', 'grade 11', 'grade 12', 'high school', 'teen', 'young adult',
                'ya', 'college', 'university']
    }

    for age_range, terms in grade_terms.items():
        if any(term in title_lower or term in description_lower for term in terms):
            age_scores[age_range] += 10

    if num_pages <= 32:
        age_scores['0-5'] += 15
        age_scores['6-10'] -= 3
    elif 33 <= num_pages <= 48:
        age_scores['0-5'] += 10
        age_scores['6-10'] += 5
    elif 49 <= num_pages <= 80:
        age_scores['6-10'] += 12
        age_scores['0-5'] -= 2
    elif 81 <= num_pages <= 120:
        age_scores['6-10'] += 8
        age_scores['11-15'] += 4
    elif 121 <= num_pages <= 200:
        age_scores['11-15'] += 8
        age_scores['6-10'] += 4
    elif 201 <= num_pages <= 350:
        age_scores['11-15'] += 10
        age_scores['15+'] += 5
    elif num_pages > 350:
        age_scores['15+'] += 12
        age_scores['11-15'] += 6

    # Content theme analysis with increased weight for theme matches
    content_themes = analyze_text_themes(title_lower, description_lower)
    for age_range, score in content_themes.items():
        age_scores[age_range] += score * 1.5

    # Shelf analysis
    shelves = book_data.get('popular_shelves', [])
    shelf_age_indicators = analyze_shelves_for_age(shelves)
    for age_range, score in shelf_age_indicators.items():
        age_scores[age_range] += score

    max_score = max(age_scores.values())
    final_age_range = max(age_scores.items(), key=lambda x: x[1])[0]

    return final_age_range


def analyze_text_complexity(text):
    if not text or len(text) < 5:
        return 0.5

    try:
        sentences = sent_tokenize(text)
        words = word_tokenize(text)

        if not sentences or not words:
            return 0.5

        avg_sentence_length = len(words) / max(1, len(sentences))
        avg_word_length = sum(len(word) for word in words if word.isalpha()) / max(1, len([w for w in words if
                                                                                           w.isalpha()]))

        # Calculate lexical diversity (larger vocabulary suggests more complex text)
        unique_words = len(set(word.lower() for word in words if word.isalpha()))
        lexical_diversity = unique_words / max(1, len([w for w in words if w.isalpha()]))

        # Calculate percentage of complex words (words with 3+ syllables)
        complex_words = sum(1 for word in words if word.isalpha() and textstat.syllable_count(word) >= 3)
        complex_words_pct = complex_words / max(1, len([w for w in words if w.isalpha()]))

        # Weighted complexity score
        complexity_score = (
                (avg_sentence_length / 25) * 0.3 +
                (avg_word_length / 7) * 0.2 +
                lexical_diversity * 0.25 +
                complex_words_pct * 0.25
        )

        return min(1.0, complexity_score)
    except:
        return 0.5


def analyze_pos_patterns(text):
    try:
        age_patterns = {
            '0-5': 0,
            '6-10': 0,
            '11-15': 0,
            '15+': 0
        }

        # Get POS tags
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)

        # Count parts of speech
        pos_counts = Counter(tag for word, tag in tagged)
        total_tokens = len(tagged)

        if total_tokens == 0:
            return age_patterns

        # Simple sentence structure (mainly nouns and verbs) - for young children
        simple_structure = (pos_counts.get('NN', 0) + pos_counts.get('NNS', 0) +
                            pos_counts.get('VB', 0) + pos_counts.get('VBZ', 0) +
                            pos_counts.get('VBP', 0)) / total_tokens

        # Complex sentence markers (conjunctions, relative pronouns, etc.)
        complex_markers = (pos_counts.get('IN', 0) + pos_counts.get('WDT', 0) +
                           pos_counts.get('WP', 0) + pos_counts.get('WRB', 0)) / total_tokens

        # Advanced language features (adjectives, adverbs, etc.)
        advanced_features = (pos_counts.get('JJ', 0) + pos_counts.get('JJR', 0) +
                             pos_counts.get('JJS', 0) + pos_counts.get('RB', 0) +
                             pos_counts.get('RBR', 0) + pos_counts.get('RBS', 0)) / total_tokens

        # Score assignment based on POS patterns
        if simple_structure > 0.6 and complex_markers < 0.1:
            age_patterns['0-5'] += 8
            age_patterns['6-10'] += 4
        elif simple_structure > 0.5 and complex_markers < 0.15:
            age_patterns['6-10'] += 7
            age_patterns['0-5'] += 3
        elif complex_markers > 0.15 and advanced_features > 0.2:
            age_patterns['11-15'] += 6
            age_patterns['15+'] += 3
        elif complex_markers > 0.2 and advanced_features > 0.25:
            age_patterns['15+'] += 8
            age_patterns['11-15'] += 4

        return age_patterns
    except:
        return {
            '0-5': 0,
            '6-10': 0,
            '11-15': 0,
            '15+': 0
        }


def analyze_text_themes(title, description):
    combined_text = title + " " + description

    theme_scores = {
        '0-5': 0,
        '6-10': 0,
        '11-15': 0,
        '15+': 0
    }

    early_themes = ['sleep', 'bed', 'nap', 'dream', 'moon', 'star', 'night', 'bunny', 'teddy',
                    'toy', 'farm', 'animal', 'cat', 'dog', 'duck', 'color', 'zoo', 'mommy',
                    'daddy', 'parent', 'bath', 'diaper', 'potty', 'train', 'truck', 'car',
                    'alphabet', 'abc', 'number', '123', 'count', 'rhyme']

    elementary_themes = ['school', 'teacher', 'friend', 'adventure', 'fun', 'magic', 'fairy',
                         'dragon', 'dinosaur', 'spy', 'detective', 'mystery', 'solve', 'game',
                         'play', 'team', 'sport', 'chapter', 'series', 'collect', 'comic',
                         'joke', 'funny', 'humor', 'silly', 'prank', 'robot', 'space', 'science']

    middle_themes = ['friend', 'school', 'bully', 'crush', 'team', 'competition', 'journal',
                     'diary', 'secret', 'club', 'grow', 'family', 'sibling', 'parent', 'problem',
                     'solve', 'quest', 'mission', 'summer', 'camp', 'vacation', 'holiday',
                     'fantasy', 'world', 'magic', 'spell', 'creature', 'monster', 'ghost']

    ya_themes = ['love', 'romance', 'relationship', 'kiss', 'boyfriend', 'girlfriend', 'dating',
                 'death', 'tragedy', 'war', 'battle', 'fight', 'survive', 'future', 'dystopian',
                 'apocalypse', 'society', 'rebellion', 'government', 'power', 'politics', 'identity',
                 'struggle', 'college', 'career', 'adult', 'mature', 'violence', 'blood']

    for theme in early_themes:
        if theme in combined_text:
            theme_scores['0-5'] += 1.5

    for theme in elementary_themes:
        if theme in combined_text:
            theme_scores['6-10'] += 1.5

    for theme in middle_themes:
        if theme in combined_text:
            theme_scores['11-15'] += 1.5

    for theme in ya_themes:
        if theme in combined_text:
            theme_scores['15+'] += 1.5

    return theme_scores


def analyze_shelves_for_age(shelves):
    shelf_patterns = {
        '0-5': ['picture book', 'board book', 'childrens', 'toddler', 'baby', 'preschool',
                'bedtime', 'nursery', 'concept book'],
        '6-10': ['early reader', 'chapter book', 'childrens', 'kids', 'elementary', 'juvenile',
                 'easy reader'],
        '11-15': ['middle grade', 'middle-grade', 'tween', 'juvenile', 'preteen'],
        '15+': ['young adult', 'ya', 'teen', 'high school', 'new adult', 'adult']
    }

    shelf_scores = {
        '0-5': 0,
        '6-10': 0,
        '11-15': 0,
        '15+': 0
    }

    for shelf in shelves:
        shelf_name = shelf.get('name', '').lower()
        shelf_count = int(shelf.get('count', 0))

        for age_range, patterns in shelf_patterns.items():
            if any(pattern in shelf_name for pattern in patterns):
                shelf_scores[age_range] += min(12, math.log(shelf_count + 1) * 2)

    return shelf_scores

# === 6. RECOMMENDER ENGINES ===
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books['description'])

def get_content_recommendations(book_id, top_n=6):
    book_row = books[books['book_id'] == book_id]
    index = books.index.get_loc(book_row.index[0])
    book_data = book_row.iloc[0].to_dict()
    target_genres = detect_book_genre_with_advanced_nlp(book_data)
    target_age = detect_age_range(book_data)

    sim_scores = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()

    for i in range(len(sim_scores)):
        if i == index:
            continue
        book_data_i = books.iloc[i].to_dict()
        genres_i = detect_book_genre_with_advanced_nlp(book_data_i)
        age_i = detect_age_range(book_data_i)

        if set(target_genres) & set(genres_i):
            sim_scores[i] *= 2
        if target_age == age_i:
            sim_scores[i] *= 2

    top_indices = np.argsort(sim_scores)[::-1][1:top_n+1]
    return books.iloc[top_indices][['book_id']]

def create_user_item_matrix():
    users = interactions['user_id'].nunique()
    items = interactions['book_id'].nunique()
    user_mapper = dict(zip(np.unique(interactions['user_id']), range(users)))
    item_mapper = dict(zip(np.unique(interactions['book_id']), range(items)))
    user_index = [user_mapper[i] for i in interactions['user_id']]
    item_index = [item_mapper[i] for i in interactions['book_id']]
    matrix = csr_matrix((interactions['rating'], (user_index, item_index)), shape=(users, items))
    return matrix.T, item_mapper, {v: k for k, v in item_mapper.items()}

user_item_matrix, item_mapper, item_inv_mapper = create_user_item_matrix()

def get_collaborative_recommendations(book_id, top_n=6):
    if book_id not in item_mapper:
        return pd.DataFrame(columns=['book_id', 'title'])
    
    try:
        item_ind = item_mapper[book_id]
        item_vec = user_item_matrix[item_ind].reshape(1, -1)
        
        # Find nearest neighbors
        kNN = NearestNeighbors(n_neighbors=top_n+1, algorithm="brute", metric="cosine")
        kNN.fit(user_item_matrix)
        neighbors = kNN.kneighbors(item_vec, return_distance=False)
        
        # Get neighbor IDs (excluding the book itself)
        ids = [item_inv_mapper[n] for n in neighbors[0][1:top_n+1]]
        
        # Return recommendations
        return books[books['book_id'].isin(ids)][['book_id', 'title']]
    
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame(columns=['book_id', 'title'])

# === 7. SEED BOOK SELECTOR ===
def get_seed_book_id(age_group, genre):
    candidates = []
    for _, row in books.iterrows():
        try:
            book_data = row.to_dict()
            genres = detect_book_genre_with_advanced_nlp(book_data)
            age = detect_age_range(book_data)
            if genre in genres and age == age_group:
                candidates.append((row['book_id'], row['ratings_count']))
        except:
            continue
    if not candidates:
        return None
    return max(candidates, key=lambda x: x[1])[0]

# === 8. ENTRY FUNCTIONS ===
def get_recommendations(book_id):
    content_df = get_content_recommendations(book_id)
    collab_df = get_collaborative_recommendations(book_id)
    recommendations = pd.concat([content_df, collab_df], ignore_index=True)
    result = []
    for book_id in recommendations['book_id']:
        book_details = books[books['book_id'] == book_id].iloc[0]
        authors_list = book_details['authors']
        author_names = [get_name(a['author_id']) for a in authors_list if get_name(a['author_id'])]
        book_metadata = {
            "book_id": book_details['book_id'],
            "title": book_details['title'],
            "author": " & ".join(author_names) if author_names else "Unknown",
            "coverImage": book_details['image_url']
        }
        result.append(book_metadata)
    return result

def get_hybrid_recommendations(age_group, genre):
    seed_id = get_seed_book_id(age_group, genre)
    if not seed_id:
        return {"error": "No book found for given filters."}
    return get_recommendations(seed_id)


def get_book_details(book_id):
    try:
        # Find the book in the dataframe
        book_row = books[books['book_id'] == book_id]
        if book_row.empty:
            return None
            
        book_data = book_row.iloc[0].to_dict()
        
        # Process authors
        authors_list = book_data.get('authors', [])
        author_names = []
        if isinstance(authors_list, list):
            author_names = [get_name(a.get('author_id')) for a in authors_list if a and get_name(a.get('author_id'))]
        authors_str = " & ".join(author_names) if author_names else "Unknown Author"
        
        # Detect genre and age group
        genres = detect_book_genre_with_advanced_nlp(book_data)
        primary_genre = genres[0] if genres else "Children"  # Default to "Children" if no genre detected
        age_group = detect_age_range(book_data)
        
        # Handle rating conversion
        try:
            rating = float(book_data.get('average_rating', 0))
        except (ValueError, TypeError):
            rating = 0.0
        
        return {
            "book_id": str(book_data.get('book_id', '')),
            "title": book_data.get('title', 'Untitled'),
            "authors": authors_str,
            "genre": primary_genre,
            "ageGroup": age_group,
            "rating": rating,
            "coverImage": book_data.get('image_url', '/book-placeholder.png'),
            "description": book_data.get('description', 'No description available')
        }
        
    except Exception as e:
        print(f"Error getting book details: {str(e)}")
        return None
