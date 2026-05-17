import streamlit as st
import requests

API_URL = "http://localhost:8002/scan-book"  # change if needed


def scan_book(isbn: str):
    payload = {"isbn": isbn}
    response = requests.post(API_URL, json=payload)

    try:
        return response.json()
    except Exception:
        return {"error": "Invalid response from API"}

st.set_page_config(page_title="SafeRead AI Tester", layout="centered")

st.title("📚 SafeRead AI - Book Scanner Tester")

st.write("Enter an ISBN to test your FastAPI backend")

# Input box
isbn = st.text_input("Enter ISBN (e.g. 9783161484100)")

# Button
if st.button("Scan Book"):

    if not isbn:
        st.warning("Please enter an ISBN")
    else:
        with st.spinner("Calling backend API..."):
            result = scan_book(isbn)

        # ❌ Error handling
        if "error" in result:
            st.error(result["error"])

        else:
            st.success(result.get("message", "Done"))

            st.subheader("📖 Book Info")
            st.write("**Title:**", result.get("title"))
            st.write("**Authors:**", result.get("authors"))

            if result.get("cover_image"):
                st.image(result["cover_image"], width=200)

            st.subheader("🎯 Age Recommendation")
            st.write(result.get("age_recommendation"))

            st.subheader("📊 Overall Score")
            st.json(result.get("overall_score"))

            st.subheader("🧠 AI Insights")
            st.json(result.get("ai_insights"))