"""
EECT Models Configuration
Maps each subject model and jury model to its provider, endpoint, and authentication method.
Adapted from the CDCT framework.
"""

# Environment variable names for AWS Bedrock
AWS_REGION_NAME_ENV_VAR = "AWS_REGION" # Environment variable to store AWS region

# Models to be evaluated in EECT
SUBJECT_MODELS_CONFIG = [
    {
        "model_name": "azure-gpt-5", # Azure OpenAI model name
        "deployment_name": "gpt-5.1", # Azure OpenAI deployment name
        "provider": "azure_openai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "AZURE_OPENAI_API_ENDPOINT",
        "api_version": "2025-03-01-preview", # Example API version
    },
    {
        "model_name": "deepseek-v3.1",
        "deployment_name": "deepseek-v3.1",
        "provider": "azure_ai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "DDFT_MODELS_ENDPOINT",
    },
    {
        "model_name": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "deployment_name": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "provider": "azure_ai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "DDFT_MODELS_ENDPOINT",
    },
    {
        "model_name": "Grok-4-Fast-Non-Reasoning",
        "deployment_name": "Grok-4-Fast-Non-Reasoning",
        "provider": "azure_ai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "DDFT_MODELS_ENDPOINT",
    },
    {
        "model_name": "Phi-4",
        "deployment_name": "Phi-4",
        "provider": "azure_ai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "DDFT_MODELS_ENDPOINT",
    },
    {
        "model_name": "o3",
        "deployment_name": "o3",
        "provider": "azure_openai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "AZURE_OPENAI_API_ENDPOINT",
        "api_version": "2025-03-01-preview",
    },
    {
        "model_name": "o4-mini",
        "deployment_name": "o4-mini",
        "provider": "azure_openai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "AZURE_OPENAI_API_ENDPOINT",
        "api_version": "2025-03-01-preview",
    },
    # {
    #     "model_name": "gemini-3-pro-preview",
    #     "provider": "vertex_ai",
    #     "vertex_ai_model_name": "gemini-3-pro-preview",
    #     "api_key_env_var": "GOOGLE_CLOUD_API_KEY",
    # },
]

# Models to be used in the EECT LLM Jury
JURY_MODELS_CONFIG = [
    {
        "model_name": "gpt-5.1",
        "deployment_name": "gpt-5.1",
        "provider": "azure_openai",
        "api_key_env_var": "AZURE_API_KEY",
        "endpoint_env_var": "AZURE_OPENAI_API_ENDPOINT",
        "api_version": "2025-03-01-preview",
    },
    # {
    #     "model_name": "claude-opus-4-1-2",
    #     "deployment_name": "claude-opus-4-1-2",
    #     "provider": "azure_anthropic",
    #     "api_key_env_var": "AZURE_API_KEY",
    #     "endpoint_env_var": "AZURE_ANTHROPIC_API_ENDPOINT",
    # },
    # {
    #     "model_name": "deepseek-v3.1",
    #     "deployment_name": "deepseek-v3.1",
    #     "provider": "azure_ai",
    #     "api_key_env_var": "AZURE_API_KEY",
    #     "endpoint_env_var": "DDFT_MODELS_ENDPOINT",
    # },
]

