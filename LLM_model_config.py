#This script is used for defining a dictionnary of LLM models to connect with API
from huggingface_hub import InferenceClient
import openai
import anthropic

# API Keys (Should be securely stored, e.g., environment variables), fill them in to use your own API
api_key_hug = "-"
api_key_gpt = "-"
api_key_gem = "-"
api_key_ant = "-"

base_url_gem = "https://generativelanguage.googleapis.com/v1beta/openai/"
# Dictionary to store model configurations
MODEL_CONFIGS = {
    "Deepseek": {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "api_key": api_key_hug,
        "provider": "novita",
        "client": lambda api_key, provider: InferenceClient(model="meta-llama/Llama-3.3-70B-Instruct", provider =provider,  api_key=api_key),
    },
    "Llama_70b": {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "api_key": api_key_hug,
        "provider": "novita",
        "client": lambda api_key, provider: InferenceClient(model="meta-llama/Llama-3.3-70B-Instruct", provider =provider,  api_key=api_key),
    },
    "CHAT_GPT_4o": {
        "model": "gpt-4o",
        "api_key": api_key_gpt,
        "provider": 0,
        "client": lambda api_key: openai.OpenAI(api_key=api_key),
    },
    "CHAT_GPT_o3_mini": {
        "model": "o3‑mini‑high",
        "api_key": api_key_gpt,
        "provider": 0,
        "client": lambda api_key: openai.OpenAI(api_key=api_key),
    },    
    "Gemini_2_5": {
        "model": "gemini-2.5-pro-preview-03-25",
        "api_key": api_key_gem,
        "provider": 0,
        "client": lambda api_key: openai.OpenAI(api_key=api_key, base_url = base_url_gem),
    },
    "Sonnet_3_7": {
        "model": "claude-3-7-sonnet-20250219",
        "api_key": api_key_ant,
        "provider": 0,
        "client": lambda api_key: anthropic.Anthropic(api_key = api_key),
    },    
}
