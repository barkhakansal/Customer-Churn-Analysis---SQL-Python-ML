import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Churn Agent", layout="wide")

st.title("🤖 AI Customer Churn Agent")
st.caption("Ask questions about customer churn using AI-powered insights")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

@st.cache_data
def load_data():
    return pd.read_csv("prediction.csv")

df = load_data()

def ai_answer(question):
    data_sample = df.head(20).to_string(index=False)

    prompt = f"""
You are a helpful data analyst.

Here is a sample of a customer churn dataset:
{data_sample}

Answer the user's question clearly and briefly based on this dataset.
If the user asks who is likely to churn, use the rows shown in the dataset sample.
Question: {question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini error: {str(e)}"

st.subheader("💡 Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Churn Summary"):
        st.write(ai_answer("Summarize churn trends in this dataset."))

    if st.button("⚠️ Who Will Churn"):
        st.write(ai_answer("Which customers are likely to churn?"))

with col2:
    if st.button("💵 High Charges"):
        st.write(ai_answer("Which customers have high monthly charges?"))

    if st.button("📈 Key Patterns"):
        st.write(ai_answer("What important patterns do you see in this dataset?"))

st.subheader("✍️ Ask Your Own Question")
question = st.text_input("Type your question here:")

if question:
    st.write(ai_answer(question))
