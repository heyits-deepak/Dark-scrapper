import json

def generate_report():
    """
    Generates a final threat report combining extracted leaks and MITRE ATT&CK mapping.
    """
    with open("extracted_leaks.json", "r") as leaks_file:
        leaks = json.load(leaks_file)

    with open("threat_mapping.json", "r") as threats_file:
        threat_mapping = json.load(threats_file)

    report = {
        "summary": {
            "total_emails": len(leaks["emails"]),
            "total_credentials": len(leaks["credentials"]),
            "total_ips": len(leaks["ip_addresses"]),
            "total_domains": len(leaks["domains"]),
            "total_credit_cards": len(leaks["credit_cards"]),
        },
        "threats": threat_mapping,
        "leaks": leaks
    }

    with open("final_report.json", "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    print("\n✅ Final report generated and saved as `final_report.json`")

if __name__ == "__main__":
    generate_report()
