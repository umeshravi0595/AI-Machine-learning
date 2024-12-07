import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🗄️")
st.title("🗄️ LangChain: Chat with SQL DB")

MYSQL="USE_MYSQL"
radio_option=["Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_option)

if selected_opt:
    db_uri=MYSQL
    server_name=st.sidebar.text_input("Provide your Server name")
    database_name=st.sidebar.text_input("Provide your Database name")


# api_key=st.sidebar.text_input(label="GRoq API Key",type="password")

if not server_name:
    st.error("Please enter the server name")

# if not api_key:
#     st.error("Please enter API key")

if not database_name:
    st.error("please enter database")

llm=ChatGroq(model_name="gemma2-9b-it",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(dbi_uri,server_name=None,database_name=None):
    if dbi_uri=="MYSQL":
      if not(server_name and database_name):
          st.error("Please provide all MySQL connection details.")
          st.stop()
    connection_string = f"mssql+pyodbc://@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"
    return SQLDatabase(create_engine(connection_string))
      
if db_uri==MYSQL:
    db=configure_db(db_uri,server_name,database_name)

toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)