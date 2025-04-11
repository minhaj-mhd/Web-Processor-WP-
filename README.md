# 🌐 Web Processor Service

This microservice is part of a FastAPI-based AI system - WEB PARSER. The **Web Processor Service** takes a URL as input, fetches and parses the webpage content using BeautifulSoup, and stores the extracted data into an SQLite database.

---

## 🚀 Features

- Accepts a URL via API
- Fetches HTML content from the URL
- Parses and cleans up relevant textual content using BeautifulSoup
- Stores the content in a local SQLite database
- Returns a content ID for future querying

---

## 🛠 Tech Stack

- FastAPI
- BeautifulSoup4
- Requests
- SQLite
- SQLAlchemy (for ORM)
- Uvicorn

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/minhaj-mhd/Web-Processor-WP-.git
cd your-repo/web_processor_service

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
