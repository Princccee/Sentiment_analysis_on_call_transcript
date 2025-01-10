import streamlit as st
import requests

# Streamlit UI
st.title("Sentiment Analysis on Call Transcripts")

uploaded_file = st.file_uploader("Upload a call transcript (.txt)", type=["txt"])

if uploaded_file:
    # Display transcript content
    content = uploaded_file.read().decode("utf-8")
    st.text_area("Transcript Content", content, height=300)

    # Send transcript to backend
    if st.button("Analyze Sentiment"):
        files = {'file': uploaded_file}
        response = requests.post("http://127.0.0.1:5000/upload", files=files)

        if response.status_code == 200:
            result = response.json()['sentiment']
            st.write("Sentiment Analysis Results:")
            for r in result:
                st.write(f"- Label: {r['label']}, Score: {r['score']:.2f}")
        else:
            st.error("Error analyzing sentiment!")
