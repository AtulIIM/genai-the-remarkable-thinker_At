from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from key import *

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from langchain_community.document_loaders import PyPDFLoader

import streamlit as st

openai_api_key = key
os.environ["OPENAI_API_KEY"] = key

st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="📖")
st.title("📖 Welcome to Custom Document chat")

"""
A basic example of using StreamlitChatMessageHistory to help LLMChain remember messages in a conversation.
The messages are stored in Session State across re-runs automatically. You can view the contents of Session State
in the expander below. View the
[source code for this app](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py).
"""

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you! With this document?")

view_messages = st.expander("View the message contents in session state")

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
    
    page_contents = []

    page_contents = ""

    for page in pages:
        page_contents += page.page_content + "\n"  # Add page content with a newline separator
        
    # vectorstore = FAISS.from_documents(pages, embedding=OpenAIEmbeddings()) 
    # retriever = vectorstore.as_retriever()
    # context = retriever.invoke(pages)
    return page_contents

st.sidebar.title("Upload Your Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF file", type=["pdf"])


# Get an OpenAI API Key before continuing
if uploaded_file:
    st.sidebar.success('file uploaded sucessfully!')
    save_uploaded_file(uploaded_file)
    
else:
    st.sidebar.warning('Please upload file')
if not uploaded_file:
    st.info("Please Upload a .pdf to make a start")
    st.stop()
    


# Set up the LangChain, passing in Message History

doc_context = getVectorstore("uploads\{}".format(uploaded_file.name))


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human regarding document context, Human can ask you question based on document context. following is the document context:"+doc_context),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI(api_key=openai_api_key)
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": prompt}, config)
    st.chat_message("ai").write(response.content)

# Draw the messages at the end, so newly generated ones show up immediately
with view_messages:
    """
    Message History initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)