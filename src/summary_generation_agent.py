from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from prompts.summary_generation_prompt import summary_generation_prompt_template
from src.utils import llm


def generate_summary(query_result, user_question: str) -> str:
    # Initialize the StrOutput parser
    parser = StrOutputParser()

    # Create the prompt template
    prompt_template = PromptTemplate(
        input_variables=["query_result", "user_question"],
        template=summary_generation_prompt_template(),
    )

    # Initialize The Chain
    chain = prompt_template | llm | parser
    response = chain.invoke(
        {
            "query_result": query_result,
            "user_question": user_question,
        }
    )

    return response
