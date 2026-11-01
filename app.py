import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

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
    openai_key = os.getenv("OPENAI_API_KEY")
    if not tavily_key or not openai_key:
        return {"error": "Search service अभी configure नहीं है। Owner को API keys जोड़नी होंगी।"}
    r = requests.post("https://api.tavily.com/search", json={
        "api_key": tavily_key, "query": req.query, "search_depth": "advanced",
        "max_results": 5, "include_answer": False
    }, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return {"answer": "इस सवाल के लिए उपयोगी स्रोत नहीं मिले।", "sources": []}
    source_text = "\n\n".join(
        f"[{i+1}] {x.get('title','')}\nURL: {x.get('url','')}\n{x.get('content','')}"
        for i, x in enumerate(results)
    )
    lang = {"hi": "Hindi", "en": "English", "auto": "the same language as the question"}.get(req.language, "the same language as the question")
    client = OpenAI(api_key=openai_key)
    out = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=f"""You are Vikky AI Search. Answer in {lang}. Use only these web results,
cite factual claims as [1], [2], and say when evidence is insufficient.
Question: {req.query}\n\nWeb results:\n{source_text}"""
    )
    return {"answer": out.output_text, "sources": [
        {"title": x.get("title","Source"), "url": x.get("url",""), "snippet": x.get("content","")}
        for x in results
    ]}
