from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
# os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
GROQ_API_KEY="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"

model=ChatGroq(model="gemma2-9b-it")

generic_template="As a AI assistant translate the input text into given {language}"
prompt=ChatPromptTemplate.from_messages([("system",generic_template),("user","Question:{inputtext}")])
# result=prompt.invoke({"language":"Tamil","inputtext":"input_text"})

st.title("Sharon Language Translator")
text=st.text_input("Enter the text you want to translate")

parser=StrOutputParser()


chain=prompt|model|parser
if text:
  st.write(chain.invoke({"language":"Tamil","inputtext":text}))
