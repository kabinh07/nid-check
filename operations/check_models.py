"""Check available Gemini models."""

from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY
import google.generativeai as genai

print("Checking available models...")

# Configure genai to list models
genai.configure(api_key=GEMINI_API_KEY)

try:
    models = genai.list_models()
    print("\nAvailable models:")
    for model in models:
        if "generateContent" in model.supported_generation_methods:
            print(f"  - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")

# Try with gemini-1.5-pro
print("\n" + "="*60)
print("Testing with gemini-1.5-pro...")
print("="*60)

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=GEMINI_API_KEY,
        temperature=0.1,
    )
    response = llm.invoke("Hello, return just JSON: {\"test\": \"ok\"}")
    print(f"✓ gemini-1.5-pro works!")
    print(f"Response: {response.content[:100]}")
except Exception as e:
    print(f"✗ Error: {str(e)[:200]}")

# Try with gemini-pro-vision
print("\n" + "="*60)
print("Testing with gemini-pro-vision...")
print("="*60)

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-vision",
        google_api_key=GEMINI_API_KEY,
        temperature=0.1,
    )
    response = llm.invoke("Hello, return just JSON: {\"test\": \"ok\"}")
    print(f"✓ gemini-pro-vision works!")
    print(f"Response: {response.content[:100]}")
except Exception as e:
    print(f"✗ Error: {str(e)[:200]}")
