import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.metrics.distance import jaccard_distance
import re
from urllib.parse import urljoin

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Configuration
WEBSITE_URLS = [
"https://iitju.edu.bd/programs/pgdit",
"https://iitju.edu.bd/programs/pmit",
"https://iitju.edu.bd/programs/graduate",
"https://iitju.edu.bd/programs/undergraduate",
"https://iitju.edu.bd/research",
"https://iitju.edu.bd/programs",
"https://iitju.edu.bd/student-activities",
"https://iitju.edu.bd/",
"https://skill.iitju.edu.bd/",
"https://iitju.edu.bd/news-events"
]  # Replace with your target websites' knowledge base URLs
STOP_WORDS = set(stopwords.words('english'))

# Fetch and parse content from a single website
def fetch_website_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from FAQ or knowledge base sections
        content = soup.find_all(['h1', 'h2', 'h3', 'p'])
        return [(tag.get_text().strip(), tag.name, url) for tag in content if tag.get_text().strip()]
    except requests.RequestException as e:
        return [(f"Error fetching content from {url}: {str(e)}", "error", url)]

# Fetch content from multiple websites
def fetch_all_content(urls):
    all_content = []
    for url in urls:
        content = fetch_website_content(url)
        all_content.extend(content)
    return all_content

# Process content into a knowledge base
def build_knowledge_base(content):
    knowledge_base = []
    current_section = None
    current_url = None
    for text, tag, url in content:
        if tag in ['h1', 'h2', 'h3']:
            current_section = text
            current_url = url
        elif tag == 'p' and current_section:
            knowledge_base.append({
                "question": current_section,
                "answer": text,
                "source": current_url
            })
    return knowledge_base

# Tokenize and clean text for matching
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in STOP_WORDS]
    return set(tokens)

# Find best matching answer
def find_best_match(user_input, knowledge_base):
    user_tokens = preprocess_text(user_input)
    best_match = None
    best_score = float('inf')
    
    for item in knowledge_base:
        question_tokens = preprocess_text(item["question"])
        score = jaccard_distance(user_tokens, question_tokens)
        if score < best_score:
            best_score = score
            best_match = {"answer": item["answer"], "source": item["source"]}
    
    if best_score < 0.8:
        return f"{best_match['answer']} (Source: {best_match['source']})"
    return "Sorry, I couldn't find a relevant answer. Try rephrasing your question."

# Main chatbot function
def get_response(user_input, knowledge_base):
    if not knowledge_base:
        return "No knowledge base available. Please check the website URLs."
    return find_best_match(user_input, knowledge_base)

# Initialize chatbot
all_content = fetch_all_content(WEBSITE_URLS)
knowledge_base = build_knowledge_base(all_content)

# Example interaction loop (for testing)
# if __name__ == "__main__":
#     print("KnowledgeBot: Ask me anything from the websites' knowledge bases! Type 'exit' to quit.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             print("KnowledgeBot: Goodbye!")
#             break
#         response = get_response(user_input, knowledge_base)
#         print(f"KnowledgeBot: {response}")
