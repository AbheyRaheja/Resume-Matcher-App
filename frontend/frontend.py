import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{BASE_URL}/resume/upload"

st.set_page_config(page_title="Resume Job Matcher", layout="wide")
st.title("📄 Resume Job Matcher")

st.markdown("""
Upload your resume and get job recommendations instantly! 
The backend will handle text extraction and find the best matching jobs.
""")

# Upload PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing your resume and fetching jobs..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(UPLOAD_ENDPOINT, files=files)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])

            st.markdown("### Recommended Jobs")
            if results:
                for job in results:
                    st.markdown(f"#### Role: {job['title']}")
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"**Job Preview:** {job['preview']}...")
                    st.markdown(f"[Apply Here]({job['link']})", unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No jobs found for this resume. Try another one!")

        except Exception as e:
            st.error(f"Failed to fetch recommendations: {e}")
