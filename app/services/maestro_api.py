import os
import requests
from smolagents import Model
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str
    content: str | list[dict[str, any]] | None = None

class MaestroModel(Model):
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        model: str = "anthropic.claude-3-haiku-20240307-v1:0", 
        max_tokens: int = 2024, 
        anthropic_version: str = "bedrock-2023-05-31"
    ):
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.max_tokens = max_tokens
        self.anthropic_version = anthropic_version

    def generate(self, messages, stop_sequences=["Task"]) -> str:
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        response = requests.post(
            self.endpoint,
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "max_tokens": self.max_tokens,
                "anthropic_version": self.anthropic_version,
                "messages": messages,
                "stop_sequences": stop_sequences
            }
        )
        response_data = response.json()
        if "error" in response_data:
            error_message = response_data["error"].get("message", "Unknown error")
            return f"Error: {error_message}"
        if "content" in response_data:
            text = []
            for message in response_data["content"]:
                if message.get("type") == "text":
                    text.append(message.get("text", ""))
            chat_message = ChatMessage(role="assistant", content=" ".join(text))
            return chat_message
        chat_message = ChatMessage(role="assistant", content=str(response_data))
        return chat_message

def get_maestro_data(message: str, route: str = "/bedrock-completion", environment: str = "dev") -> ChatMessage:
    endpoint = f"{os.getenv('MAESTRO_ENDPOINT')}/{environment}{route}"
    api_key = os.getenv("MAESTRO_API_KEY")
    if not endpoint or not api_key:
        raise ValueError("MAESTRO_ENDPOINT and MAESTRO_API_KEY must be set")
    maestro_model = MaestroModel(api_key, endpoint)
    return maestro_model.generate(message)