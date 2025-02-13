from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from src.utils import llm


class QueryOutput(BaseModel):
    """Generated SQL query."""
    query: str = Field(..., description="ONLY provide the SQL Query in 'query' JSON key. No additional text or explanation.")

def query_validator_agent(sql_query, table_info):
    base_prompt_template = """
    You are a SQL query assistant. You will be provided with the table schema and a SQL Query. 
    Your task is to check if the SQL query is valid based on the schema and fix any issues that arise, 
    ensuring the query is compatible with SQLite.

    <CRUCIAL RULES>
    - Always provide a valid SQL query based on the schema provided. No additional text is allowed.
    - The SQL Query MUST BE COMPATIBLE WITH SQLITE. SQLite does not support advanced functions such as PERCENTILE_CONT.
    - If the query uses unsupported functions or features, replace them with SQLite-compatible alternatives.
    - Verify the columns and tables in the query.
    - If the query includes percentile calculations, use a workaround or remove them, as SQLite does not support `PERCENTILE_CONT`.

    Table Schema: 
    {SCHEMA}
    
    SQL QUERY:
    {SQL_QUERY}
    
    ##Output Format:
    Generate only the SQL Query in JSON Format. Never provide Additional Text or explanation as i am parsing only the SQL Query.
    \n{format_instructions}\n
    """

    parser = JsonOutputParser(pydantic_object=QueryOutput)
    prompt = PromptTemplate(
        template=base_prompt_template,
        input_variables=["SCHEMA", "SQL_QUERY"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser 
    response = chain.invoke({
        "SCHEMA": table_info,
        "SQL_QUERY": sql_query
    })
    
    # Return the fixed query if any changes are made
    return response['query']