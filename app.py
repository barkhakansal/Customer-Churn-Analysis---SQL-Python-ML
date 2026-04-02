import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Churn Agent", layout="wide")

st.title("🤖 AI Customer Churn Agent")
st.caption("Ask questions about customer churn using AI-powered insights")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def load_data():
    return pd.read_csv("prediction.csv")

df = load_data()

def ai_answer(question):
    data_sample = df.head(20).to_string(index=False)

    prompt = f"""
You are a data analyst.

Here is a sample of the customer churn dataset:
{data_sample}

Answer the user's question clearly based on this dataset.
If the question asks about customers likely to churn, refer to the rows shown in the dataset.
Question: {question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

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
