import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load the API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page setup
st.set_page_config(page_title="MediAI Assistant", page_icon="🩺")
st.title("🩺 AI Medical Assistant")

# --- Section 1: Analyze Symptoms ---
st.header("🧍 Analyze Patient Symptoms")
symptoms = st.text_area("Enter patient symptoms:", placeholder="e.g., fever, sore throat, joint pain")

if st.button("Analyze Symptoms"):
    if symptoms:
        with st.spinner("Analyzing symptoms..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful medical assistant. Analyze symptoms and suggest possible causes, "
                                "tests, and recommended next steps. Avoid making final diagnoses."
                            )
                        },
                        {"role": "user", "content": f"Symptoms: {symptoms}"}
                    ],
                    temperature=0.4
                )
                result = response['choices'][0]['message']['content']
                st.success("✅ Analysis complete.")
                st.markdown("### 🧠 AI Suggestion:")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter symptoms.")

# --- Section 2: Upload and Analyze Test Results ---
st.header("📄 Upload Test Results")

uploaded_file = st.file_uploader("Upload test results (CSV or TXT format):", type=["csv", "txt"])

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")

    if st.button("Analyze Test Results"):
        with st.spinner("Analyzing file..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert medical assistant. Given lab test results or reports, explain possible implications, "
                                "suggest additional tests if needed, and recommend next steps. Avoid giving a final diagnosis."
                            )
                        },
                        {"role": "user", "content": f"Lab/Test Results:\n{file_content}"}
                    ],
                    temperature=0.4
                )
                result = response['choices'][0]['message']['content']
                st.success("✅ Test analysis complete.")
                st.markdown("### 📋 AI Interpretation:")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error during test analysis: {e}")
