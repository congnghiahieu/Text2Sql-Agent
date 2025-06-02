import sqlite3

import pandas as pd
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase

from chart_generation.chart_generation import generate_chart
from src.sql_generation_agent import generate_sql_query

# Set the page title and subheader
st.title("Text2SQL Chatbot")

# st.subheader("Interact with a powerful SQL-driven assistant to query and explore data seamlessly!")
# Sidebar for displaying the table schema
# st.sidebar.header("Charts Preview ⚙️")

# Initialize the SQLite database connection
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
engine = sqlite3.connect("Chinook.db")
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
def chatbot(
	user_question: str,
	engine,
	table_info: str,
	chat_messages: list,
):
	sql_query = generate_sql_query(user_question, table_info, chat_messages)
	query_result = execute_sql_query(sql_query, engine)
	# summary_response = generate_summary(query_result, user_question)

	result_str = query_result.to_csv(index=False)
	chat_messages.append({"role": "user", "content": user_question})
	chat_messages.append({"role": "assistant", "content": [sql_query, result_str]})

	# return result_str, query_result, summary_response
	return result_str, query_result


# Initialize session state for chat messages if not already present
if "messages" not in st.session_state:
	st.session_state.messages = [
		{
			"role": "assistant",
			"content": "Hi there! Ask me any question related to your database.",
		}
	]


# Handle user input using chat_input
if prompt := st.chat_input("Ask a question about the data:"):
	st.session_state.messages.append({"role": "user", "content": prompt})

	plot_flag = any(keyword in prompt.lower() for keyword in ["plot", "chart", "bar", "visualize"])

	# Get the response, query result, and summary from the chatbot
	# response, query_result, summary = chatbot(
	# 	user_question=prompt,
	# 	engine=engine,
	# 	table_info=table_info,
	# 	chat_messages=st.session_state.messages,
	# )
	response, query_result = chatbot(
		user_question=prompt,
		engine=engine,
		table_info=table_info,
		chat_messages=st.session_state.messages,
	)

	# Convert the query result to markdown format
	markdown_table = df_to_markdown(query_result)

	# Generate the chart if plot_flag is True
	if plot_flag:
		chart = generate_chart(query_result, prompt)

		# # If chart is generated, render it in the sidebar
		# if chart:
		# 	st.sidebar.plotly_chart(chart)

	# Append the table and summary to the messages and chat messages
	st.session_state.messages.append({"role": "assistant", "content": markdown_table})
	# st.session_state.messages.append(
	# 	{"role": "assistant", "content": f"Here is the Data Summary:\n{summary}"}
	# )


# Render chat messages
for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		if isinstance(message["content"], str):
			st.markdown(message["content"])  # Display string content as markdown
		elif isinstance(message["content"], pd.DataFrame):
			st.dataframe(message["content"])  # Display DataFrame as a table
