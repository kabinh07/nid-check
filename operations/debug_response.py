"""Debug the actual response from Gemini."""

import base64
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GEMINI_API_KEY

# Get first front image
front_images = list(Path("../data/images/nid_front_image").glob("*.jpg"))
image_path = front_images[0]

print(f"Testing with image: {image_path.name}")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1,
)

# Encode image
with open(image_path, "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

prompt = """Return ONLY valid JSON:
{
    "test": "value"
}"""

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

print("Sending request...")
response = llm.invoke([message])

print(f"\nResponse type: {type(response)}")
print(f"Response: {response}")
print(f"\nresponse.content type: {type(response.content)}")
print(f"response.content: {response.content}")

if isinstance(response.content, list):
    print(f"\nIs list with {len(response.content)} items:")
    for i, item in enumerate(response.content):
        print(f"  Item {i} type: {type(item)}")
        print(f"  Item {i}: {item}")
