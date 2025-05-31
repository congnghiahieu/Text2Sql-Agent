import openai
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.utils import llm


class ChartGenerationFormat(BaseModel):
    """Generated SQL query."""

    chart_code: str = Field(..., description="Syntactically correct python chart code.")


def generate_chart(result_str, user_question, plot_flag):
    chart_generation_prompt_template = """
    You are an advanced Chart Code creator. You will provided a comma separated data, and also the user question. Based on teh question,
    you will intelligently give a ALWAYS CORRECT python code using plotly to generate a chart code, which I will execute to get the plot object
    The Code should be 100% correct.

    Input Data:
    {result_str}

    User_question:
    {user_question}

    Generate the Chart Code only without any additional text or explanation in JSON format only in 'chart_code' key.
    Output Format:

        "chart_code": "YOUR_CHART_CODE_HERE"

    \n{format_instructions}\n
    """

    parser = JsonOutputParser(pydantic_object=ChartGenerationFormat)
    prompt = PromptTemplate(
        template=chart_generation_prompt_template,
        input_variables=["result_str", "user_question"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    response = chain.invoke({"result_str": result_str, "user_question": user_question})

    # Instead of using exec, parse and evaluate the code to generate the chart object directly
    chart_code = response["chart_code"]

    # Ensure the generated code does not include any `show()` or similar display calls.
    if "fig.show()" in chart_code:
        chart_code = chart_code.replace("fig.show()", "")  # Remove any show() calls

    try:
        exec_locals = {}
        exec(chart_code, {}, exec_locals)
        chart = exec_locals.get(
            "fig"
        )  # Assuming 'fig' is the chart object created by the chart code
    except Exception as e:
        st.error(f"Error generating chart: {e}")
        return None

    # Render the chart in Streamlit
    return chart
