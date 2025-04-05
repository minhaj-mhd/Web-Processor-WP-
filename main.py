from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import uuid
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = "content.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def setup_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_content (
                id TEXT PRIMARY KEY,
                url TEXT,
                title TEXT,
                text TEXT
            )
        """)
        conn.commit()

setup_database()

class UrlRequest(BaseModel):
    url: str

@app.post("/process_url")
async def process_url(url_request: UrlRequest):
    try:
        # Fetch the webpage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url_request.url, headers=headers)
        response.raise_for_status()

        # Parse content
        soup = BeautifulSoup(response.content, "html.parser")
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        content = {
            "title": soup.title.string if soup.title else "No Title",
            "text": soup.get_text(separator=" ", strip=True)
        }

        content_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO processed_content (id, url, title, text) VALUES (?, ?, ?, ?)",
                (content_id, url_request.url, content["title"], content["text"])
            )
            conn.commit()

        return {"content_id": content_id, "title": content["title"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/content/{content_id}")
def get_content_info(content_id: str):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT url, title FROM processed_content WHERE id = ?", (content_id,)
            )
            result = cursor.fetchone()

        if result:
            return {"url": result[0], "title": result[1]}
        else:
            raise HTTPException(status_code=404, detail="Content not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
