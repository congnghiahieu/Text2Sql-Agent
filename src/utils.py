from langchain_openai import ChatOpenAI

from src.settings import SETTINGS

llm = ChatOpenAI(
	api_key=SETTINGS.LLM_API_KEY,
	base_url=SETTINGS.LLM_BASE_URL,
	model=SETTINGS.LLM_MODEL_NAME,
	temperature=0,
)
