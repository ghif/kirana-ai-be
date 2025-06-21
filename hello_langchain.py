import getpass
import os

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")

print(model.invoke("Hello, world!"))