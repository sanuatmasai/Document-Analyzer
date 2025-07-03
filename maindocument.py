from fastmcp import FastMCP
from textblob import TextBlob
from textstat import flesch_reading_ease
import re
import uuid
from collections import Counter

# Initialize FastMCP
mcp = FastMCP("📄 Simple Document Analyzer MCP")

# In-memory document store
documents = {}

# ----------------------------- TOOLS ----------------------------- #

@mcp.tool
def add_document(document_data: dict) -> str:
    """
    Add a new document with metadata.
    Example input:
    {
        "title": "My Article",
        "author": "John",
        "content": "This is the document text."
    }
    """
    doc_id = str(uuid.uuid4())
    documents[doc_id] = document_data
    return f"Document added with ID: {doc_id}"

@mcp.tool
def get_sentiment(text: str) -> str:
    """
    Analyze sentiment of given text: positive, negative, or neutral.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

@mcp.tool
def extract_keywords(text: str, limit: int = 5) -> list:
    """
    Extract top keywords from text.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    common_words = set(['the', 'and', 'is', 'in', 'to', 'a', 'of', 'it', 'that', 'this'])
    filtered = [w for w in words if w not in common_words and len(w) > 2]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(limit)]

@mcp.tool
def analyze_document(document_id: str) -> dict:
    """
    Full analysis: sentiment, keywords, readability, and stats.
    """
    doc = documents.get(document_id)
    if not doc:
        return {"error": "Document not found"}
    
    text = doc.get("content", "")
    return {
        "title": doc.get("title"),
        "author": doc.get("author"),
        "sentiment": get_sentiment(text),
        "keywords": extract_keywords(text, 5),
        "readability_score": flesch_reading_ease(text),
        "word_count": len(text.split()),
        "sentence_count": len(re.findall(r'[.!?]', text))
    }

@mcp.tool
def search_documents(query: str) -> list:
    """
    Search documents by content keyword.
    """
    results = []
    for doc_id, doc in documents.items():
        if query.lower() in doc.get("content", "").lower():
            results.append({"id": doc_id, "title": doc.get("title")})
    return results

# --------------------------- RUN MCP ---------------------------- #

if __name__ == "__main__":
    mcp.run()
