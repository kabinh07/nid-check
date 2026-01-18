"""Test script to verify Gemini API key validity using LangChain."""

from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY

def test_api_key():
    """Test if the API key is valid."""
    print(f"Testing API key: {GEMINI_API_KEY[:20]}...")
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=GEMINI_API_KEY,
        )
        
        # Try a simple text generation
        response = llm.invoke("Hello, just testing if this works.")
        print("✓ API Key is valid!")
        print(f"Response: {response.content[:100]}")
        return True
        
    except Exception as e:
        print(f"✗ API Key test failed!")
        print(f"Error: {str(e)}")
        print("\nPossible issues:")
        print("1. API key is invalid or revoked")
        print("2. API key doesn't have access to Gemini API")
        print("3. Project quota exceeded")
        print("4. API key has restrictions (IP, domain, etc.)")
        return False

if __name__ == "__main__":
    test_api_key()
