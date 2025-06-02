import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from prompts.sql_generation_prompt import sql_generation_prompt_template
from sql_examples import few_shot_examples
from src.query_validation_agent import query_validator_agent
from src.utils import llm


class SQLQueryGenerator(BaseModel):
	query: str = Field(
		"ONLY GENERATE THE SQL QUERY IN 'query' JSON KEY. NEVER EVER PROVIDE ADDITIONAL TEXT OR INFORMATION."
	)


# SQL generation function with enhanced prompt template for SQLite
def generate_sql_query(
	user_question: str, table_info: str, chat_history: list, dialect: str = "sqlite"
) -> str:
	"""Generate SQL query from user question for SQLite, considering conversation history."""

	# Include the conversation history as context in the prompt
	conversation_context = "\n".join(
		[
			f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}"
			for msg in chat_history
		]
	)

	# Example scenarios to guide the model
	example_scenarios = few_shot_examples()

	parser = JsonOutputParser(pydantic_object=SQLQueryGenerator)
	prompt_template = PromptTemplate(
		input_variables=["dialect", "table_info", "user_question", "example_scenarios"],
		template=sql_generation_prompt_template(),
		partial_variables={"format_instructions": parser.get_format_instructions()},
	)

	# Initialize The Chain
	chain = prompt_template | llm | parser
	response = chain.invoke(
		{
			"dialect": dialect,
			"table_info": table_info,
			"user_question": user_question,
			"example_scenarios": example_scenarios,
		}
	)

	result = response["query"]
	validated_query = query_validator_agent(result, table_info)
	# st.sidebar.markdown(f'<div class="custom-code">{validated_query}</div>', unsafe_allow_html=True)
	st.sidebar.markdown(f"**Generated SQL Query:**\n```sql\n{validated_query}\n```")
	return validated_query
