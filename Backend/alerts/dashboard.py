import streamlit as st
import pymongo

st.title("Dark Web Threat Intelligence Dashboard")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["DarkWebDB"]
collection = db["ThreatPosts"]

data = list(collection.find().limit(20))

for item in data:
    st.write(f"🔹 **{item['title']}**")
