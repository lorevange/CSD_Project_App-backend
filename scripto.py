import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)
models = list(client.models.list())
print(f"Models returned: {len(models)}")
for model in models:
    methods = getattr(model, "supported_generation_methods", None)
    print(f"{model.name} -> supported_generation_methods={methods}")
