"""Debug script to check actual API response format."""

import base64
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GEMINI_API_KEY

def debug_api_response():
    """Test what the API actually returns."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.1,
    )
    
    # Simple text test first
    print("=" * 60)
    print("Test 1: Simple text request")
    print("=" * 60)
    
    try:
        response = llm.invoke("Return only valid JSON: {\"test\": \"value\"}")
        print(f"Type of response: {type(response)}")
        print(f"Type of response.content: {type(response.content)}")
        print(f"Response.content: {response.content}")
        print()
    except Exception as e:
        print(f"Error: {str(e)}\n")
    
    # Now test with an actual image
    print("=" * 60)
    print("Test 2: Image-based request")
    print("=" * 60)
    
    # Use first available front image
    front_images = list(Path("../data/images/nid_front_image").glob("*.jpg"))
    
    if front_images:
        image_path = front_images[0]
        print(f"Using image: {image_path.name}")
        
        # Encode image
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")
        
        prompt = 'Return only JSON: {"test": "value"}'
        
        message = HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}",
                    },
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        )
        
        try:
            response = llm.invoke([message])
            print(f"Type of response: {type(response)}")
            print(f"Type of response.content: {type(response.content)}")
            print(f"Response.content (first 500 chars): {str(response.content)[:500]}")
            print(f"Full response.content:\n{response.content}\n")
            
            # Show what we're getting
            if isinstance(response.content, list):
                print("Response is a LIST:")
                for i, item in enumerate(response.content):
                    print(f"  Item {i} (type: {type(item)}): {str(item)[:200]}")
            
        except Exception as e:
            print(f"Error: {str(e)}\n")
    else:
        print("No front images found!")

if __name__ == "__main__":
    debug_api_response()
