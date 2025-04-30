from bs4 import BeautifulSoup
import re

def extract_leaks_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    text = soup.get_text()

    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    domains = re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", text)
    credit_cards = re.findall(r"\b(?:\d[ -]*?){13,16}\b", text)
    credentials = re.findall(r"([a-zA-Z0-9_.+-]+):([^\s]+)", text)

    return {
        "summary": {
            "total_emails": len(emails),
            "total_credentials": len(credentials),
            "total_ips": len(ips),
            "total_domains": len(domains),
            "total_credit_cards": len(credit_cards),
        },
        "threats": {},
        "leaks": {
            "emails": emails,
            "credentials": credentials,
            "ip_addresses": ips,
            "domains": domains,
            "credit_cards": credit_cards
        }
    }
