from pydantic_ai.models.openai import OpenAIModel
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Any
import logfire
import base64
import os

load_dotenv()

class Config(BaseSettings):

    MODELS: list[Any] = [
        # "claude-3-7-sonnet-20250219",
        # "deepseek:deepseek-reasoner",
        # "gemini-2.0-flash",
        # "xai:grok-2-latest",
        # "groq:llama-3.3-70b-versatile",
        # "openai:gpt-4o",
        # "openai:o3-mini",

    ]

    INTENDED: str = "Customer Support"
    # INTENDED: str = "Doctor's assistant"
    # INTENDED: str = "Python programmer assistant"

    NUMBER_OF_REPETITIONS: int = 1


    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_SECRET_KEY: str | None = None
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = "https://cloud.langfuse.com/api/public/otel"
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    XAI_API_KEY: str | None = None
    XAI_BASE_URL: str | None = "https://api.x.ai/v1"
    DEEPSEEK_API_KEY: str | None = None
    DEEPSEEK_BASE_URL: str | None = "https://api.deepseek.com"
    OLLAMA_BASE_URL: str | None = "http://localhost:11434/v1"

    def __init__(self, **kwargs):
        LANGFUSE_AUTH = base64.b64encode(f"{os.getenv("LANGFUSE_PUBLIC_KEY")}:{os.getenv("LANGFUSE_SECRET_KEY")}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

        logfire.configure(
            send_to_logfire = False
        )
        super().__init__(**kwargs)

    
    def get_model(self, model: str):
        company, _, model_name = model.partition(':')
        match company:
            case 'deepseek':
                return OpenAIModel(
                    model_name=model_name,
                    base_url=self.DEEPSEEK_BASE_URL,
                    api_key=self.DEEPSEEK_API_KEY
                )
            case 'ollama':
                return OpenAIModel(
                    model_name=model_name,
                    base_url=self.OLLAMA_BASE_URL
                )
            case 'xai':
                return OpenAIModel(
                    model_name=model_name,
                    base_url=self.XAI_BASE_URL,
                    api_key=self.XAI_API_KEY
                )
            
        return model

@lru_cache()
def get_config() -> Config:
    return Config()

config = get_config()
