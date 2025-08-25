import os, json, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY  = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def llm_json(messages, max_retries=2, temperature=0):
    for attempt in range(max_retries+1):
        resp = client.chat.completions.create(
            model=MODEL,
            response_format={"type":"json_object"},
            temperature=temperature,
            messages=messages
        )
        try:
            return json.loads(resp.choices[0].message.content)
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(0.8)

