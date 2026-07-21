import os
import re
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client


load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_embedding(text):
    return get_model().encode(text).tolist()


def get_exchange_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/ILS")
        rates = response.json()["rates"]
        return {
            "USD": 1 / rates["USD"],
            "EUR": 1 / rates["EUR"],
            "GBP": 1 / rates["GBP"],
            "NIS": 1.0,
        }
    except:
        return {"USD": 3.7, "EUR": 4.0, "GBP": 4.7, "NIS": 1.0}


def detect_currency(text, history):
    full_text = text
    for msg in history:
        full_text += " " + msg.get("content", "")
    full_text = full_text.lower()

    rates = get_exchange_rates()

    if "$" in full_text or "dollar" in full_text or "usd" in full_text:
        return "USD", rates["USD"]
    elif "€" in full_text or "euro" in full_text or "eur" in full_text:
        return "EUR", rates["EUR"]
    elif "£" in full_text or "pound" in full_text or "gbp" in full_text:
        return "GBP", rates["GBP"]
    else:
        return "NIS", 1.0


def extract_budget(question, history):
    full_text = question
    for msg in history:
        full_text += " " + msg.get("content", "")

    currency, rate = detect_currency(full_text, [])

    patterns = [
        r"\$(\d+)",
        r"€(\d+)",
        r"£(\d+)",
        r"(\d+)\s*(?:dollars?|usd)",
        r"(\d+)\s*(?:euros?|eur)",
        r"(\d+)\s*(?:pounds?|gbp)",
        r"(\d+)\s*(?:nis|shekel|₪)",
        r"(\d+)\s*(?:budget|per night)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, full_text.lower())
        if matches:
            amount = int(matches[-1])
            return int(amount * rate)

    if any(word in full_text.lower() for word in ["cheap", "budget", "affordable"]):
        return 400

    return None


def search_hotels(query, n_results=3):
    embedding = get_embedding(query)

    result = supabase.rpc(
        "search_hotels", {"query_embedding": embedding, "match_count": n_results}
    ).execute()

    return result.data if result.data else []


def format_hotels(hotels):
    docs = []
    for hotel in hotels:
        doc = f"""
Hotel: {hotel['name']}
Location: {hotel['location']}
Neighborhood: {hotel['neighborhood']}
Stars: {hotel['stars']}
Price: {hotel['price_min']}-{hotel['price_max']} NIS per night
Amenities: {hotel['amenities']}
Nearby: {hotel['nearby']}
Description: {hotel['description']}
        """.strip()
        docs.append(doc)
    return docs


def search_documents(query, n_results=3):
    hotels = search_hotels(query, n_results)
    return format_hotels(hotels)


def search_documents_with_budget(query, history=[], n_results=3):
    budget = extract_budget(query, history)
    hotels = search_hotels(query, n_results * 2)

    if budget:
        filtered = [h for h in hotels if h.get("price_min", 0) <= budget]
        hotels = filtered if filtered else hotels
        print(f"Budget filter: {budget} NIS → {len(hotels)} hotels match")

    return format_hotels(hotels[:n_results])