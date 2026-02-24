# EECT Framework API (FastAPI)

This document provides instructions for running the EECT Framework API using FastAPI.

## Setup

### Environment Variables

Ensure you have the following environment variables set in your `.env` file or exported in your shell:

```bash
AZURE_API_KEY=your_azure_api_key
AZURE_OPENAI_API_ENDPOINT=https://your-endpoint.openai.azure.com/
DDFT_MODELS_ENDPOINT=https://your-foundry-endpoint.v1.azure.com/
```

### Installation

Install dependencies:

```bash
pip install fastapi uvicorn
```

### Starting the Server

Run the FastAPI server using uvicorn:

```bash
uvicorn eect_api:app --reload --host 0.0.0.0 --port 8003
```

Or run the script directly:

```bash
python eect_api.py
```

## API Endpoints

### 1. `GET /score/{model_name}`

Returns aggregated metrics for a model. If scores do not exist yet, it starts the full diagnostic battery in the background.

### 2. `POST /experiment`

Starts the full diagnostic battery for a model.

**Request Body**

```json
{
  "model_name": "Phi-4"
}
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
