import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI


from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_community.vectorstores import FAISS
from key import *
from langchain_community.document_loaders import PyPDFLoader

import getpass
import os

from key import *

os.environ["OPENAI_API_KEY"] = key

# Load version history from the text file
def load_version_history():
    with open("version_history.txt", "r") as file:
        return file.read()
   
    
# Save uploaded file locally.
def save_uploaded_file(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return


def getVectorstore(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
        
    vectorstore = FAISS.from_documents(pages, embedding=OpenAIEmbeddings()) 
    # retriever = vectorstore.as_retriever()
    return vectorstore

llm = ChatOpenAI()


# Sidebar section for uploading files and providing a YouTube URL
with st.sidebar:
    uploaded_files = st.file_uploader("Please upload your files", accept_multiple_files=False, type=["pdf"])
    
    # Create an expander for the version history in the sidebar
    with st.sidebar.expander("**Version History**", expanded=False):
        st.write(load_version_history())

# Check if files are uploaded or YouTube URL is provided
if uploaded_files:
    st.success('Your Document successfully recieved.', icon="✅")
    save_uploaded_file(uploaded_files)
    vectorstore = getVectorstore("uploads\{}".format(uploaded_files.name))
    
    
    # Store the processed data in session state for reuse
    st.session_state.processed_data = {
        # "document_chunks": document_chunks,
        "vectorstore": vectorstore,
    }

    # Initialize Langchain's QA Chain with the vectorstore
    qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())


# Initialize chat history
if "messages" not in st.session_state:
    st.write("done")
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Accept user input
if prompt := st.chat_input("Ask your questions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Query the assistant using the latest chat history
    history = [
        f"{message['role']}: {message['content']}" 
        for message in st.session_state.messages
    ]

    # Convert the history to a list of strings
    history_strings = [message["content"] for message in st.session_state.messages]


    result = qa({
        "question": prompt, 
        "chat_history": history_strings
    })
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = result["answer"]
        message_placeholder.markdown(full_response + "|")
    message_placeholder.markdown(full_response)    
    print(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    
        
