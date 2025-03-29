import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["DarkWebDB"]
collection = db["ThreatPosts"]

# Save extracted data
def save_to_db(posts):
    if posts:
        collection.insert_many(posts)
        print("[INFO] Data saved to MongoDB successfully!")
    else:
        print("[WARNING] No data to save.")

# Example Usage
extracted_posts = [{"title": "Selling zero-day exploits", "link": "http://example.onion/thread1"}]
save_to_db(extracted_posts)
