import requests
from bs4 import BeautifulSoup
import json
import os
import re

CACHE_PATH = "core/knowledge_cache.json"


# cache load
def load_cache():

    if os.path.exists(CACHE_PATH):

        with open(CACHE_PATH, "r") as f:

            return json.load(f)

    return {}


# cache save
def save_cache(cache):

    with open(CACHE_PATH, "w") as f:

        json.dump(cache, f, indent=4)


# search links
def search_links(query):

    url = "https://html.duckduckgo.com/html/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "q": query
    }

    try:

        response = requests.post(
            url,
            data=data,
            headers=headers,
            timeout=8
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:

        print("DuckDuckGo timeout occurred")

        return []

    except requests.exceptions.RequestException as e:

        print(f"Search request failed: {e}")

        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = []

    seen = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "http" in href and "duckduckgo.com" not in href:

            if "uddg=" in href:

                href = href.split("uddg=")[-1]

            href = requests.utils.unquote(href)

            if href not in seen:

                seen.add(href)

                links.append(href)

        if len(links) >= 5:

            break

    return links


# fetch page text
def fetch_text(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        paragraphs = soup.find_all("p")

        text = " ".join(
            p.get_text()
            for p in paragraphs
        )

        return text.lower()

    except:

        return ""


# clean sentence
def clean_sentence(sent):

    sent = sent.strip()

    sent = re.sub(r"\s+", " ", sent)

    sent = sent.replace("\n", " ")

    return sent.capitalize()


# extract sections
def extract_sections(text):

    sentences = re.split(r"[.?!]", text)

    def is_valid(sent):

        bad_phrases = [

            "in this article",

            "you will learn",

            "this guide",

            "we will discuss",

            "learn how",

            "click here",

            "read more",

            "subscribe",

            "copyright"
        ]

        return not any(
            bp in sent
            for bp in bad_phrases
        )

    def score_sentence(sent, keywords):

        score = 0

        for k in keywords:

            if k in sent:

                score += 2

        if len(sent) > 80:

            score += 1

        return score

    def get_best_sentence(keywords):

        best_sent = ""

        best_score = 0

        for sent in sentences:

            sent = sent.strip()

            if len(sent) < 40:

                continue

            if not is_valid(sent):

                continue

            score = score_sentence(
                sent,
                keywords
            )

            if score > best_score:

                best_score = score

                best_sent = sent

        if best_sent:

            return clean_sentence(best_sent)

        return "Not clearly available"

    description = get_best_sentence([

        "disease",

        "symptom",

        "infection",

        "fungal",

        "bacterial",

        "leaf spot"
    ])

    cause = get_best_sentence([

        "caused by",

        "fungus",

        "bacteria",

        "virus",

        "pathogen"
    ])

    remedy = get_best_sentence([

        "treat",

        "control",

        "fungicide",

        "spray",

        "manage",

        "apply"
    ])

    prevention = get_best_sentence([

        "prevent",

        "avoid",

        "resistant",

        "spacing",

        "airflow",

        "rotation"
    ])

    return {

        "description": description,

        "cause": cause,

        "remedy": remedy,

        "prevention": prevention
    }


# main function
def get_disease_info(class_name):

    cache = load_cache()

    # use cache
    if class_name in cache:

        print("Loaded from cache")

        return cache[class_name]

    # normalize class name
    normalized = class_name.lower().replace(" ", "_")

    parts = normalized.split("_", 1)

    if len(parts) < 2:

        return {

            "description": "Not available",

            "cause": "Not available",

            "remedy": "Not available",

            "prevention": "Not available"
        }

    crop = parts[0].title()

    disease = parts[1].replace("_", " ").title()

    query = f"{crop} {disease} plant disease causes treatment prevention"

    print(f"\nSearching for: {query}\n")

    links = search_links(query)

    if not links:
        return {

        "crop": crop,

        "disease": disease,

        "description": "Internet knowledge temporarily unavailable.",

        "cause": "Not available",

        "remedy": "Not available",

        "prevention": "Not available"
    }

    full_text = ""

    # fetch text
    for link in links[:3]:

        text = fetch_text(link)

        if text:

            full_text += " " + text

    extracted = extract_sections(full_text)

    result = {

        "crop": crop,

        "disease": disease,

        "description": extracted["description"],

        "cause": extracted["cause"],

        "remedy": extracted["remedy"],

        "prevention": extracted["prevention"]
    }

    # save cache
    cache[class_name] = result

    save_cache(cache)

    return result