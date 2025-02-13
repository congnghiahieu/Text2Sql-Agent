import streamlit as st
import pandas as pd
from langchain.memory import ConversationBufferMemory
from chart_generation.chart_generation import generate_chart
from src.sql_generation_agent import generate_sql_query
from src.summary_generation_agent import generate_summary
from langchain.sql_database import SQLDatabase
import sqlite3
import json
import pandas as pd

# Set the page title and subheader
st.title("Text2SQL Chatbot")
st.subheader("Interact with a powerful SQL-driven assistant to query and explore data seamlessly!")
# Sidebar for displaying the table schema
st.sidebar.header("Charts Preview ⚙️")

# Initialize memory to store chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chat_history = memory.load_memory_variables({})["chat_history"]

# Initialize the SQLite database connection
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
engine = sqlite3.connect('Chinook.db')
table_info = db.table_info


# Execute SQL query
def execute_sql_query(query: str, engine) -> pd.DataFrame:
    """Execute the generated SQL query and return the results."""
    return pd.read_sql_query(query, con=engine)

# Function to convert DataFrame to markdown table
def df_to_markdown(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a markdown-formatted table."""
    markdown = "| " + " | ".join(df.columns) + " |\n"
    markdown += "|---" * len(df.columns) + "|\n"
    for index, row in df.iterrows():
        markdown += "| " + " | ".join(map(str, row)) + " |\n"
    return markdown


# Define the chatbot logic
def chatbot(user_question: str, engine, table_info: str, chat_history: list, plot_flag: bool = False):
    """Handle user input, generate SQL query, execute it, and maintain chat history."""
    sql_query = generate_sql_query(user_question, table_info,chat_history)
    query_result = execute_sql_query(sql_query, engine)
    summary_response = generate_summary(query_result,user_question)
    
    result_str = query_result.to_csv(index=False)
    chat_history.append({"role": "user", "content": user_question})
    chat_history.append({"role": "assistant", "content": [sql_query, result_str]})
    
    return result_str, query_result,summary_response


# Initialize session state for chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! Ask me any question related to your database."}]
    st.session_state.chat_history = []  # Initialize chat history to preserve context


# Handle user input using chat_input
if prompt := st.chat_input("Ask a question about the data:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    plot_flag = any(keyword in prompt.lower() for keyword in ["plot", "chart", "bar","visualize"])
    
    # Get the response, query result, and summary from the chatbot
    response, query_result, summary = chatbot(user_question=prompt, engine=engine, table_info=table_info, chat_history=st.session_state.chat_history)
    
    # Convert the query result to markdown format
    markdown_table = df_to_markdown(query_result)

    # Generate the chart if plot_flag is True
    if plot_flag:
        chart = generate_chart(query_result, prompt, plot_flag=True)

        # If chart is generated, render it in the sidebar
        if chart:
            st.sidebar.plotly_chart(chart)

    
    # Append the table and summary to the messages and chat history
    st.session_state.messages.append({"role": "assistant", "content": markdown_table})
    st.session_state.messages.append({"role": "assistant", "content": f"Here is the Data Summary:\n{summary}"})
    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": markdown_table})
    st.session_state.chat_history.append({"role": "assistant", "content": f"Here is the Data Summary:\n{summary}"})


# Function to save the chat history in a JSON file
def save_chat_history():
    # Ensure the chat history is stored in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Convert messages to JSON format and save to a file
    with open('chat_history.json', 'w') as json_file:
        json.dump(st.session_state.messages, json_file)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):
            st.markdown(message["content"])  # Display string content as markdown
        elif isinstance(message["content"], pd.DataFrame):
            st.dataframe(message["content"])  # Display DataFrame as a table

save_chat_history()
