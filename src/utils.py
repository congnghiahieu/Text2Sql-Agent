
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
import openai
import sqlite3

openai.organization = "<masked>"
openai.api_key ="<masked>"
############OpenAI Chat Instance #######################
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,openai_api_key=openai.api_key)

