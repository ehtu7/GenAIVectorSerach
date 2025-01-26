import os
from dotenv import load_dotenv
import streamlit as st

from db_reader_writer_service import readDataFromDB
from fileUploader import upload_File

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")



st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response=readDataFromDB(prompt)
    msg=response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


st.sidebar.title("Upload Section")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["pdf"])
if uploaded_file is not None:
    st.sidebar.write("### Uploaded File Details")
    st.sidebar.write("**File Name:**", uploaded_file.name)
    st.sidebar.write("**File Type:**", uploaded_file.type)
    st.sidebar.write("**File Size:**", uploaded_file.size, "bytes")
    
    # Handle and display the content based on file type
   
    
    if uploaded_file.type == "application/pdf":
        upload_File(uploaded_file)

    else:
        st.sidebar.write("Please upload in PDF format")
else:
    st.sidebar.write("Upload a file using the sidebar!")