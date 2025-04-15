import re
import ipaddress
import requests

def is_valid_ip(ip):
    """
    Validate an IP address (IPv4 and IPv6).
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_domain(domain):
    """
    Validate a domain name.
    """
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9]'    # First character of the domain
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'  # Sub domain + hostname
        r'[a-zA-Z]{2,}$'  # First level TLD
    )
    return bool(domain_regex.match(domain))

def is_valid_email(email):
    """
    Validate an email address.
    """
    email_regex = re.compile(
        r'^[\w\.-]+@[\w\.-]+\.\w+$'
    )
    return bool(email_regex.match(email))

def is_valid_hash(hash_string):
    """
    Validate a hash (MD5, SHA1, SHA256).
    """
    if re.fullmatch(r"[a-fA-F\d]{32}", hash_string):
        return "MD5"
    elif re.fullmatch(r"[a-fA-F\d]{40}", hash_string):
        return "SHA1"
    elif re.fullmatch(r"[a-fA-F\d]{64}", hash_string):
        return "SHA256"
    else:
        return None

def validate_ioc(ioc):
    """
    General function to validate what type of IOC it is.
    """
    if is_valid_ip(ioc):
        return "IP Address"
    elif is_valid_domain(ioc):
        return "Domain"
    elif is_valid_email(ioc):
        return "Email"
    elif is_valid_hash(ioc):
        return f"Hash ({is_valid_hash(ioc)})"
    else:
        return None

def check_virustotal(ioc, api_key):
    """
    Check if an IOC (IP, domain, hash) is listed in VirusTotal.
    """
    url = f"https://www.virustotal.com/api/v3/files/{ioc}"  # Change this for IP or domain checks
    
    # Use the appropriate endpoint for the type of IOC
    # For IPs: https://www.virustotal.com/api/v3/ips/{ioc}
    # For domains: https://www.virustotal.com/api/v3/domains/{ioc}
    # For hashes: https://www.virustotal.com/api/v3/files/{ioc}
    
    headers = {
        "x-apikey": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Check for data in the response
        if 'data' in data:
            return data['data']
        else:
            return None
    else:
        return None
