# EECT API Runner

This document provides instructions for running the EECT Framework as an API service.

## API Setup

The EECT API uses FastAPI and runs on port **8003**.

### Environment Variables

Ensure you have the following environment variables set in your `.env` file or exported in your shell:

```bash
AZURE_API_KEY=your_azure_api_key
AZURE_OPENAI_API_ENDPOINT=https://your-endpoint.openai.azure.com/
DDFT_MODELS_ENDPOINT=https://your-foundry-endpoint.v1.azure.com/
```

### Starting the Server

To start the API server, run:

```bash
./.venv/bin/python eect_api.py
```

## API Endpoints

### 1. GET `/score/{model_name}`

Retrieves the current metrics for a specific model.

- **If scores exist:** Returns a JSON array of metrics for each dilemma.
- **If scores don't exist:** If the model name is valid, it triggers a full diagnostic battery (Phase 1 and Phase 2) in the background and returns a `"status": "started"` message.

**Example Curl:**

```bash
curl http://localhost:8003/score/gpt-5
```

### 2. POST `/run_experiment`

Triggers a full diagnostic battery for a model.

- **Request Body:**
  ```json
  {
    "model_name": "Phi-4"
  }
  ```

**Example Curl:**

```bash
curl -X POST http://localhost:8003/run_experiment 
     -H "Content-Type: application/json" 
     -d '{"model_name": "Phi-4"}'
```

## Supported Models

The API supports the models configured in `src/models_config.py`.

### Contestants
- `gpt-5`
- `gpt-5.1`
- `o3`
- `o4-mini`
- `DeepSeek-v3.1`
- `Llama-4-Maverick-17B-128E-Instruct-FP8`
- `Phi-4`
- `grok-4-fast-non-reasoning`
- `mistral-medium-2505`
- `gpt-oss-120b`
- `Kimi-K2.5`

### Jury Models
- `gpt-5.2`
- `DeepSeek-v3.2`
