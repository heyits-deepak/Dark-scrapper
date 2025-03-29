import re
import json
from bs4 import BeautifulSoup

def extract_leaks_from_html(html_file):
    """
    Extracts potential leaks (emails, credentials, IPs, domains, credit card numbers) from HTML.
    """
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text_content = soup.get_text(separator="\n")  # Convert HTML to text

    leaks = {
        "emails": re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_content),
        "credentials": re.findall(r"\b[a-zA-Z0-9._%+-]+:[a-zA-Z0-9!@#$%^&*()_+=-]{6,}\b", text_content),  # Fix regex
        "ip_addresses": re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text_content),
        "domains": re.findall(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", text_content),
        "credit_cards": re.findall(r"\b(?:\d[ -]*?){13,16}\b", text_content)
    }

    return leaks

if __name__ == "__main__":
    extracted_data = extract_leaks_from_html("scraped_page.html")

    # Save extracted data to a JSON file
    with open("extracted_leaks.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print("\n✅ Data leaks extracted and saved to `extracted_leaks.json`")
