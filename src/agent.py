"""
Agent module for EECT - Handles different model endpoints with timeout/retry support.
Adapted from the CDCT framework.
"""
import os
import json
from abc import ABC, abstractmethod
from openai import AzureOpenAI, OpenAI
from threading import Lock

# Placeholder for Anthropic Foundry SDK
try:
    from anthropic import AnthropicFoundry, AnthropicVertex
    ANTHROPIC_FOUNDRY_AVAILABLE = True
except ImportError:
    ANTHROPIC_FOUNDRY_AVAILABLE = False

# Import requests for Bedrock ABSK auth
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from src.retry_handler import RetryConfig, call_with_retry

class Agent(ABC):
    """Abstract base class for a model agent."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def chat(self, messages: list) -> str:
        """Sends a list of messages and returns the response."""
        pass

# --- Client Caching Pools (omitted for brevity, no changes) ---

# --- Agent Implementations ---

class AzureOpenAIAgent(Agent):
    """Agent for Azure OpenAI native models."""
    def __init__(self, model_name: str, deployment_name: str, azure_endpoint: str, azure_api_key: str, api_version: str, retry_config: RetryConfig = None):
        super().__init__(model_name)
        self.client = get_azure_openai_client(azure_api_key, azure_endpoint, api_version)
        self.deployment_name = deployment_name
        self.retry_config = retry_config or RetryConfig()

    def chat(self, messages: list) -> str:
        def _call():
            response = self.client.chat.completions.create(
                model=self.deployment_name, 
                messages=messages,
                timeout=300
            )
            return response.choices[0].message.content
        return call_with_retry(_call, self.retry_config, log_prefix=f"[{self.model_name}]")

class AzureAIAgent(Agent):
    """Agent for Azure AI Foundry models."""
    def __init__(self, model_name: str, deployment_name: str, azure_endpoint: str, azure_api_key: str, retry_config: RetryConfig = None):
        super().__init__(model_name)
        self.client = get_openai_client(azure_endpoint, azure_api_key)
        self.deployment_name = deployment_name
        self.retry_config = retry_config or RetryConfig()

    def chat(self, messages: list) -> str:
        def _call():
            response = self.client.chat.completions.create(
                model=self.deployment_name, 
                messages=messages, 
                temperature=0.0,
                timeout=300
            )
            return response.choices[0].message.content
        return call_with_retry(_call, self.retry_config, log_prefix=f"[{self.model_name}]")

class AzureAnthropicAgent(Agent):
    """Agent for Azure Anthropic (Claude) models."""
    def __init__(self, model_name: str, deployment_name: str, azure_endpoint: str, azure_api_key: str, retry_config: RetryConfig = None):
        super().__init__(model_name)
        self.client = get_azure_anthropic_client(azure_api_key, azure_endpoint)
        self.deployment_name = deployment_name
        self.retry_config = retry_config or RetryConfig()

    def chat(self, messages: list) -> str:
        def _call():
            response = self.client.messages.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=4096
            )
            return response.content[0].text
        return call_with_retry(_call, self.retry_config, log_prefix=f"[{self.model_name}]")

class BedrockAgent(Agent):
    """Agent for AWS Bedrock models using the Converse API with ABSK API key auth."""
    def __init__(self, model_name: str, model_id: str, api_key: str,
                 region: str = "us-east-1", max_tokens: int = 4096,
                 retry_config: RetryConfig = None):
        super().__init__(model_name)
        self.model_id = model_id
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/converse"
        self.retry_config = retry_config or RetryConfig()

    def chat(self, messages: list) -> str:
        def _call():
            import requests
            body = {
                "messages": [{"role": m["role"], "content": [{"text": m["content"]}]} for m in messages],
                "inferenceConfig": {"temperature": 0.0, "maxTokens": self.max_tokens},
            }
            resp = requests.post(
                self.url,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
                json=body, timeout=300,
            )
            resp.raise_for_status()
            content = resp.json()["output"]["message"]["content"]
            for block in content:
                if "text" in block:
                    return block["text"]
            return content[0].get("text", str(content))
        return call_with_retry(_call, self.retry_config, log_prefix=f"[{self.model_name}]")


# --- Factory Function ---

def create_agent(model_config: dict) -> Agent:
    """Factory function to create the appropriate agent based on model config."""
    provider = model_config.get("provider")
    model_name = model_config.get("model_name")
    api_key_env_var = model_config.get("api_key_env_var")
    api_key = os.getenv(api_key_env_var) if api_key_env_var else None

    deployment_name = model_config.get("deployment_name")
    endpoint_env_var = model_config.get("endpoint_env_var")
    api_version = model_config.get("api_version")

    endpoint = model_config.get("endpoint")
    if not endpoint and endpoint_env_var:
        endpoint = os.getenv(endpoint_env_var)
    
    
    if provider == "bedrock":
        model_id = model_config.get("model_id", deployment_name)
        region = model_config.get("region", "us-east-1")
        bedrock_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        if not bedrock_key:
            raise ValueError("AWS_BEARER_TOKEN_BEDROCK not set")
        return BedrockAgent(
            model_name=model_name,
            model_id=model_id,
            api_key=bedrock_key,
            region=region
        )

    # For other providers, the API key is required
    if not api_key:
        raise ValueError(f"API key environment variable '{api_key_env_var}' not set for model '{model_name}'")

    if not endpoint:
        raise ValueError(f"Endpoint environment variable '{endpoint_env_var}' not set for model '{model_name}'")

    if provider == "azure_openai":
        return AzureOpenAIAgent(
            model_name=model_name,
            deployment_name=deployment_name,
            azure_endpoint=endpoint,
            azure_api_key=api_key,
            api_version=api_version
        )
    elif provider == "azure_ai":
        return AzureAIAgent(
            model_name=model_name,
            deployment_name=deployment_name,
            azure_endpoint=endpoint,
            azure_api_key=api_key
        )
    elif provider == "azure_anthropic":
        return AzureAnthropicAgent(
            model_name=model_name,
            deployment_name=deployment_name,
            azure_endpoint=endpoint,
            azure_api_key=api_key
        )
    else:
        raise ValueError(f"Unknown or unsupported provider: {provider} for model {model_name}")

# Helper functions get_azure_openai_client etc. are omitted for brevity
def get_azure_openai_client(api_key, endpoint, api_version):
    return AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)

def get_openai_client(base_url, api_key):
    return OpenAI(base_url=base_url, api_key=api_key)

def get_azure_anthropic_client(api_key, base_url):
    if not ANTHROPIC_FOUNDRY_AVAILABLE:
        raise ImportError("Anthropic Foundry SDK not available.")
    return AnthropicFoundry(api_key=api_key, base_url=base_url)

