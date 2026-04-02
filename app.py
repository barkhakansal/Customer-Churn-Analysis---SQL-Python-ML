import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Churn Agent", layout="wide")

st.title("🤖 AI Customer Churn Agent")
st.caption("Ask questions about customers predicted to churn in the future.")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

@st.cache_data
def load_data():
    return pd.read_csv("prediction.csv")

df = load_data()

def ai_answer(question):
    data_sample = df.head(20).to_string(index=False)
    summary = f"Total predicted churn customers: {len(df)}"

    prompt = f"""
You are a helpful data analyst.

This dataset contains customers predicted to churn in the future.
It is not the full customer dataset. It is only the model output of high-risk customers.

{summary}

Sample rows from the predicted churn dataset:
{data_sample}

Answer the user's question clearly and briefly based only on this predicted churn dataset.
If the user asks who will churn, refer to these predicted high-risk customers.
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
        st.write(ai_answer("Summarize the predicted churn customer trends in this dataset."))

    if st.button("⚠️ Who Will Churn"):
        st.write(ai_answer("Which customers are predicted to churn?"))

with col2:
    if st.button("💵 High Charges"):
        st.write(ai_answer("Which predicted churn customers have high monthly charges?"))

    if st.button("📈 Key Patterns"):
        st.write(ai_answer("What important patterns do you see among the predicted churn customers?"))

st.subheader("✍️ Ask Your Own Question")
question = st.text_input("Type your question here:")

if question:
    st.write(ai_answer(question))
