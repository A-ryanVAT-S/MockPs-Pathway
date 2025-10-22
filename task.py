import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()
st.set_page_config(page_title="Financial Advisor", layout="wide", initial_sidebar_state="expanded")

class FinancialResponse(BaseModel):
    answer: str = Field(description="Clear and helpful financial answer")
    key_terms: list[str] = Field(description="List of key financial terms discussed,important ones")

google_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0.5
)

structured_llm = llm.with_structured_output(FinancialResponse, method="json_mode")

def get_financial_response(question):
    try:
        response = structured_llm.invoke(question)
        return response.answer, response.key_terms
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}", []

def save_conversation(question, answer, key_terms):
    file_exists = os.path.exists("financial_conversations.csv")
    
    new_id = 1
    if file_exists:
        try:
            df = pd.read_csv("financial_conversations.csv")
            if not df.empty:
                new_id = df['id'].max() + 1
        except:
            pass
    
    record = {
        "id": new_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "key_terms": ", ".join(key_terms) if key_terms else "None"
    }
    
    df_new = pd.DataFrame([record])
    
    if file_exists:
        df_new.to_csv("financial_conversations.csv", mode='a', header=False, index=False)
    else:
        df_new.to_csv("financial_conversations.csv", index=False)

st.title("Financial Advisory Service")

with st.sidebar:
    st.header("Service Information")
    st.markdown("""
    - Financial question answering
    - Key term extraction
    - Conversation history tracking
    - Immediate responses
    """)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

for msg in st.session_state.conversation_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg['content'])

if user_question := st.chat_input("Type your financial question here..."):
    st.session_state.conversation_history.append({"role": "user", "content": user_question})
    
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            answer, key_terms = get_financial_response(user_question)
            st.markdown(answer)
            
            st.session_state.conversation_history.append({"role": "assistant", "content": answer})
            
            save_conversation(user_question, answer, key_terms)

st.markdown("---")
st.markdown("You can ask about various financial topics including investments, savings, markets, and personal finance matters.")