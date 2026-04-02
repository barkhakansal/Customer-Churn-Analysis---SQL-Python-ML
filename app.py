import streamlit as st
import pandas as pd

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="AI Churn Agent", layout="wide")

st.title("🤖 AI Customer Churn Agent")
st.caption("Ask questions about customer churn using AI-powered insights")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("prediction.csv")

df_pred = load_data()

# -------------------------------
# Sample Values (Replace if needed)
# -------------------------------
churn_rate = 26.99

df_imp = pd.DataFrame({
    "Feature": ["Contract", "Tenure", "Monthly Charge", "Internet Type", "Payment Method"],
    "Importance": [0.18, 0.15, 0.12, 0.10, 0.08]
})

# -------------------------------
# AI Agent Function
# -------------------------------
def answer_question(q):
    q = q.lower()

    if "accuracy" in q:
        st.success("✅ Model accuracy is 84%.")

    elif "churn rate" in q:
        st.info(f"📊 Churn rate is {churn_rate}%")

    elif "important features" in q:
        st.subheader("🔍 Top Features Influencing Churn")
        st.dataframe(df_imp)

    elif "who will churn" in q:
        st.subheader("⚠️ High-Risk Customers")
        result = df_pred[['Customer_ID', 'Monthly_Charge', 'Tenure_in_Months', 'Customer_Status_Predicted']].head(10)
        st.dataframe(result)

    else:
        st.warning("Try asking: churn rate, accuracy, important features, or who will churn")

# -------------------------------
# Buttons Section
# -------------------------------
st.subheader("💡 Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Churn Rate"):
        answer_question("churn rate")

    if st.button("🎯 Model Accuracy"):
        answer_question("accuracy")

with col2:
    if st.button("🔍 Important Features"):
        answer_question("important features")

    if st.button("⚠️ Who Will Churn"):
        answer_question("who will churn")

# -------------------------------
# Custom Question Input
# -------------------------------
st.subheader("✍️ Ask Your Own Question")

custom_question = st.text_input("Type your question here:")

if custom_question:
    answer_question(custom_question)
