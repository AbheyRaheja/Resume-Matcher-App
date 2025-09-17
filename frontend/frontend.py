import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{BASE_URL}/resume/upload"

st.set_page_config(page_title="Resume Job Matcher", layout="wide")
st.title("📄 Resume Job Matcher")

st.markdown("""
Upload your resume and get job recommendations instantly!  
The backend will handle text extraction, predict your job category, and fetch matching jobs.
""")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing your resume and fetching jobs..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(UPLOAD_ENDPOINT, files=files)
            response.raise_for_status()
            data = response.json()

            # --- Show predictions ---
            preds = data.get("predictions", [])
            if preds:
                st.subheader("🔮 Predicted Categories")
                df = pd.DataFrame(preds)
                st.bar_chart(df.set_index("label")["probability"])
            else:
                st.warning("No predictions found.")

            # --- Show jobs ---
            jobs = data.get("jobs", [])
            st.subheader("💼 Recommended Jobs")
            if jobs:
                for job in jobs:
                    st.markdown(f"#### {job['title']}")
                    st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"[👉 Apply Here]({job['redirect_url']})", unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No jobs found for this resume. Try another one!")

        except Exception as e:
            st.error(f"Failed to fetch recommendations: {e}")
