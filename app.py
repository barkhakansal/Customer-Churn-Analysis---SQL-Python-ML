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
    # 1. Give it the "Big Picture" (Math summary of the whole file)
    full_stats = df.describe(include='all').to_string()
    
    # 2. Give it a look at the actual data (first 15 rows)
    data_sample = df.head(15).to_string(index=False)
    
    # 3. The 'System' Instructions
    prompt = f"""
ROLE: You are an expert Retention Strategist and Data Scientist.

CONTEXT:
- Total high-risk customers: {len(df)}
- Below is the statistical summary of the ENTIRE churn dataset:
{full_stats}

- Here are the specific details for the first 15 customers:
{data_sample}

INSTRUCTIONS:
1. Use the 'Statistical Summary' to answer big-picture questions (averages, totals, trends).
2. Use the 'Sample Rows' only to give specific examples of customers.
3. If the answer is not in the data provided, say "I don't have enough data to answer that" instead of guessing.
4. Keep your answer professional, data-driven, and brief.

USER QUESTION: {question}
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
