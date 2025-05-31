def summary_generation_prompt_template() -> str:
    """Generate a prompt template for summary generation."""
    return """
    You are an expert data analyst. Given the following table and user question, generate a concise summary in markdown format.
    Summary should describe teh insights of the tabular data and answer the user question. Also explain the records to the user.
    - The summary only explains teh answers, not the questions. It will just explain teh answer in form of answering the question.
    Table:
    {query_result}

    User Question:
    {user_question}

    Summary:
    """
