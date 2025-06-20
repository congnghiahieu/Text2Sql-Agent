def sql_generation_prompt_template():
	sql_generation_prompt = """
        Given the conversation context, create a syntactically correct {dialect} query to help find the answer to the user's question.
        If the user specifies a number of results, adjust the query accordingly.
        Limit the results to a maximum of 5 if not specified.
        <<MUST CRUCIAL INSTRUCTIONS>>
        - By Default Always use LIMIT 5 if the user does not specify the number of records for every question, unless the user mentions.
        - Only provide the SQL query inside the 'query' JSON key. Do not include any additional text or explanation.
        - Validate how many records the user is asking, and use `LIMIT` and `OFFSET` to approximate results, especially for cases like percentiles.

        **Important Notes for SQLite**:
        - Always limit your answer to only Top 10 records if the user does not specify the number of records.
        - SQLite does not support advanced functions like `PERCENTILE_CONT` or window functions.
        - Ensure any complex calculations or percentile calculations are replaced with SQLite-compatible logic (e.g., subqueries or custom aggregations).
        - Avoid using non-SQLite syntax or unsupported functions.

        **Table Schema**:
        {table_info}

        **Example Scenarios**:
        {example_scenarios}

        **Question**: {user_question}

        ##Output Format:
        Your response should be a JSON with only the SQL query in the 'query' key, as shown below:

            "query": "YOUR_SQL_QUERY_HERE"

        Do not include any additional text, explanation, or commentary. Just the query in the correct format.

        {format_instructions}
        """
	return sql_generation_prompt
