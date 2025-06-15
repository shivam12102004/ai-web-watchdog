from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from langdetect import detect
import tldextract

client = OpenAI(api_key="YOUR API KEY")  # Replace with your actual key

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_page():
    data = request.get_json()
    url = data.get('url')

    try:
        # Step 1: Scrape the content
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc and "content" in meta_desc.attrs else "No meta description"
        full_text = soup.get_text(separator=" ", strip=True)[:3000]

        # Step 2: Detect Language
        try:
            language = detect(full_text)
        except:
            language = "unknown"

        # Step 3: Extract Domain Information
        ext = tldextract.extract(url)
        main_domain = f"{ext.domain}.{ext.suffix}"
        subdomain = ext.subdomain

        # Step 4: GPT Deep Analysis with Tone Detection
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI content analyzer. Given a webpage's title, description, and content, "
                    "you will return a JSON object with:\n"
                    "- content_type (like blog, news, scam, e-commerce, phishing, etc.)\n"
                    "- is_phishing (true/false)\n"
                    "- confidence (0.0 to 1.0)\n"
                    "- summary\n"
                    "- keywords (as list of strings)\n"
                    "- tone (e.g., calm, fear, urgency, scam, informative)\n"
                    "Respond strictly in JSON."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Title: {title}\n"
                    f"Description: {description}\n"
                    f"Content:\n{full_text}"
                )
            }
        ]

        gpt_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        gpt_json = gpt_response.choices[0].message.content

        return jsonify({
            "url": url,
            "title": title,
            "meta_description": description,
            "content_preview": full_text[:300],
            "language": language,
            "domain_info": {
                "main_domain": main_domain,
                "subdomain": subdomain
            },
            "gpt_analysis": gpt_json,
            "summary": "Page analyzed successfully using GPT and enhanced tools"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
