def openrouter_chat(messages, model="mistralai/mistral-7b-instruct"): 
	"""
	Use OpenRouter.ai's OpenAI-compatible endpoint for chat completion.
	messages: list of dicts, e.g. [{"role": "user", "content": "..."}]
	model: model string, default is mistralai/mistral-7b-instruct
	Returns the response text or error message.
	"""
	import os
	from openai import OpenAI
	from dotenv import load_dotenv
	load_dotenv()
	client = OpenAI(
		base_url="https://openrouter.ai/api/v1",
		api_key=os.environ.get("OPENROUTER_API_KEY")
	)
	try:
		completion = client.chat.completions.create(
			model=model,
			messages=messages,
		)
		return completion.choices[0].message.content
	except Exception as e:
		return f"Request failed: {e}"
def hf_openai_chat(messages, model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"): 
	"""
	Use Hugging Face's OpenAI-compatible endpoint for chat completion.
	messages: list of dicts, e.g. [{"role": "user", "content": "..."}]
	model: model string, default is Mistral-7B-Instruct-v0.2:featherless-ai
	Returns the response text or error message.
	"""
	import os
	from openai import OpenAI
	from dotenv import load_dotenv
	load_dotenv()
	client = OpenAI(
		base_url="https://router.huggingface.co/v1",
		api_key=os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY")
	)
	try:
		completion = client.chat.completions.create(
			model=model,
			messages=messages,
		)
		return completion.choices[0].message.content
	except Exception as e:
		return f"Request failed: {e}"
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY")
BOOKING_COM_API_KEY = os.getenv("BOOKING_COM_API_KEY")
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")
OPENTRIPMAP_KEY = os.getenv("OPENTRIPMAP_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

import requests
def hf_llama2_generate(prompt, model="mistralai/Mistral-7B-Instruct-v0.2", max_tokens=256):
	"""
	Generate text using Hugging Face Inference API (Mistral-7B-Instruct-v0.2 by default).
	Returns the generated text or error message.
	"""
	api_url = f"https://api-inference.huggingface.co/models/{model}"
	headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
	payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
	try:
		response = requests.post(api_url, headers=headers, json=payload, timeout=60)
		response.raise_for_status()
		data = response.json()
		if isinstance(data, dict) and data.get("error"):
			return f"Error: {data['error']}"
		# Some models return a list of dicts with 'generated_text'
		if isinstance(data, list) and "generated_text" in data[0]:
			return data[0]["generated_text"]
		# Some models return a list of dicts with 'generated_text' inside 'generated_texts'
		if isinstance(data, list) and "generated_texts" in data[0]:
			return data[0]["generated_texts"][0]
		return str(data)
	except Exception as e:
		return f"Request failed: {e}"