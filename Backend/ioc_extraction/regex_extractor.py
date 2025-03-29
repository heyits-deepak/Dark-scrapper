import re

def extract_iocs(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
    return {"emails": emails, "ips": ips}

# Example post
post = "Contact hacker via badguy@darkmail.com. IP: 192.168.1.1"
extracted_iocs = extract_iocs(post)
print(f"🔹 Extracted IOCs: {extracted_iocs}")
