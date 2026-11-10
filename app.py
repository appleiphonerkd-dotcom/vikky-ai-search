import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Vikky AI Search")

app.mount("/static", StaticFiles(directory="static"), name="static")

class SearchRequest(BaseModel):
    query: str
    language: str = "auto"

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/api/search")
def search(req: SearchRequest):

    tavily_key = os.getenv("TAVILY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not tavily_key or not gemini_key:
        return {"error": "API keys configure nahi hain."}

    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_key,
                "query": req.query,
                "search_depth": "basic",
                "max_results": 5
            },
            timeout=30
        )
        r.raise_for_status()

        results = r.json().get("results", [])

        if not results:
            return {
                "answer": "Useful information nahi mili.",
                "sources": []
            }

        source_text = "\n\n".join(
            f"[{i+1}] {x.get('title','')}\n"
            f"URL: {x.get('url','')}\n"
            f"{x.get('content','')}"
            for i, x in enumerate(results)
        )

        lang = {
            "hi": "Hindi",
            "en": "English",
            "auto": "the same language as the question"
        }.get(req.language, "the same language as the question")

        client = genai.Client(api_key=gemini_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            You are Vikky AI Search.
            Answer in {lang}.
            Use only the web results below.
            Cite factual claims as [1], [2].
            If evidence is insufficient, say so.

            Question: {req.query}

            Web results:
            {source_text}
            """
        )

        return {
            "answer": response.text,
            "sources": [
                {
                    "title": x.get("title", "Source"),
                    "url": x.get("url", ""),
                    "snippet": x.get("content", "")
                }
                for x in results
            ]
        }

    except Exception as e:
        print("Search Error:", str(e))
        return {
            "error": "Search service mein problem hai. Please try again."
        }
