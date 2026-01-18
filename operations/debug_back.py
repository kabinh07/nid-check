"""Debug script to check why back OCR isn't extracting data."""

import base64
import json
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GEMINI_API_KEY

# Get first back image
back_images = list(Path("../data/images/nid_back_image").glob("*.jpg"))
if not back_images:
    print("No back images found!")
    exit(1)

image_path = back_images[0]
print(f"Testing back image: {image_path.name}\n")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1,
)

# Encode image
with open(image_path, "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

prompt = """You are an expert at reading National ID (NID) documents from Bangladesh.
        
Analyze this NID back image and extract the following information in JSON format:
{
    "plain_address": "the complete address written on the back"
}

If the address field is not visible or cannot be extracted, use null.
Return ONLY valid JSON inside code blocks, no additional text."""

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

print("=" * 60)
print("Sending back image to Gemini...")
print("=" * 60)

try:
    response = llm.invoke([message])
    
    print(f"\nResponse type: {type(response)}")
    print(f"response.content type: {type(response.content)}")
    
    if isinstance(response.content, list):
        print(f"\nIs list with {len(response.content)} items:")
        for i, item in enumerate(response.content):
            print(f"\nItem {i}:")
            print(f"  Type: {type(item)}")
            if isinstance(item, dict):
                print(f"  Keys: {item.keys()}")
                if 'text' in item:
                    print(f"  Text (first 500 chars):\n{str(item['text'])[:500]}")
            else:
                print(f"  Value: {item}")
    else:
        print(f"\nContent: {response.content}")
    
    # Try to extract JSON
    print("\n" + "=" * 60)
    print("Attempting JSON extraction...")
    print("=" * 60)
    
    if isinstance(response.content, list):
        result_text = ""
        for item in response.content:
            if isinstance(item, dict):
                if 'text' in item:
                    result_text += str(item['text'])
                else:
                    result_text += str(item)
            else:
                result_text += str(item)
    else:
        result_text = str(response.content)
    
    result_text = result_text.strip()
    
    print(f"Extracted text (first 500 chars):\n{result_text[:500]}\n")
    
    # Remove markdown
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
        result_text = result_text.strip()
    
    # Extract JSON
    json_start = result_text.find('{')
    json_end = result_text.rfind('}')
    
    print(f"JSON start index: {json_start}")
    print(f"JSON end index: {json_end}")
    
    if json_start != -1 and json_end != -1:
        json_text = result_text[json_start:json_end+1]
        print(f"Extracted JSON:\n{json_text}\n")
        
        result = json.loads(json_text)
        print(f"Parsed JSON: {result}")
    else:
        print("Could not find JSON in response!")
        print(f"Full text:\n{result_text}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
