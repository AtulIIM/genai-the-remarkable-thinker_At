from operator import itemgetter

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


os.environ["OPENAI_API_KEY"] = key

loader = PyPDFLoader("uploads\w27392.pdf")

pages = loader.load_and_split()

vectorstore = FAISS.from_documents(
    pages, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Answer the Question for given resume based only on the following context
#Generate the MS SQl query based only on the following context

template = """You will be provided document context 
                and your task is to give the topic for it in single line also give the summary in nine to ten line.:
{context}


Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()


chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

answer = chain.invoke("please give the topic for it in single line also give the summary in nine to ten line.")
print(answer)






