from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	LLM_API_KEY: str
	LLM_BASE_URL: str
	LLM_MODEL_NAME: str

	model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "allow"}


SETTINGS = Settings()
