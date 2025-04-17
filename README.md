## BookBuddy

BookBuddy is a book recommendation platform for kids, using a hybrid filtering algorithm. Users can select their favorite books, age group, and genre to receive personalized book recommendations. The system consists of a front-end (Next.js), a back-end (Django), and a recommendation engine built with Python.

📌 Features

📚 Personalized book recommendations based on hybrid filtering<br>
🏗️ Modern UI with Next.js<br>
🛠️ API for book data and recommendations<br>

---
🌐 **Live Demo**: [https://bookbuddy-pj.vercel.app](https://bookbuddy-pj.vercel.app)
📦 **Data Files**: Included in `data.zip`

## 🚀 Setup for Local Development

### Prerequisites
- Node.js v16+ (Frontend)
- Python 3.12+ (Backend)
- Git

### 1. Get Started
```bash
git clone https://github.com/chance-ho/bookbuddy.git
unzip data.zip -d backend/data
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```
Create .env.local:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```


### 3. Backend Setup
```bash
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .\.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Run the app locally
Frontend (in /frontend):
```bash
npm run dev
```

Backend (in /backend):
```bash
python api.py
```

### Access at:
Frontend: http://localhost:3000
API: http://localhost:8000/


### 🔧 Configuration
Modify backend/recommender.py if needed:
```bash
# === 2. GLOBAL DATA LOADING ===
olumns_of_interest_books = ['book_id', 'title', 'average_rating', 'ratings_count','description', 'num_pages', 'popular_shelves','image_url','authors']
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
```

