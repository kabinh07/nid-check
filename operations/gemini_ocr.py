"""Gemini OCR module using LangChain for extracting NID information from images."""

import base64
import json
import time
import re
from pathlib import Path
from typing import Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GEMINI_API_KEY


class GeminiOCR:
    """Handles OCR operations using Google's Gemini API via LangChain."""

    def __init__(self):
        """Initialize LangChain Gemini client."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.1,
        )
        self.request_count = 0
        self.last_request_time = 0
        self.requests_per_minute = 15  # Free tier limit
        self.max_retries = 3
        self.base_wait_time = 90  # 1.5 minutes

    def _extract_retry_delay(self, error_message: str) -> int:
        """Extract retry delay from error message."""
        match = re.search(r'(\d+(?:\.\d+)?)\s*s(?:ec)?', error_message)
        if match:
            delay = int(float(match.group(1))) + 5
            return min(delay, 600)
        return self.base_wait_time

    def _wait_for_rate_limit(self):
        """Implement rate limiting to avoid hitting quotas."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        # Reset counter every 60 seconds
        if time_since_last >= 60:
            self.request_count = 0

        # If we're approaching the rate limit, wait
        if self.request_count >= self.requests_per_minute - 1:
            wait_time = 60 - time_since_last + 1
            if wait_time > 0:
                print(f"\n⏳ Rate limit approaching, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = time.time()
        else:
            self.request_count += 1
            self.last_request_time = current_time

    def _invoke_with_retry(self, message: HumanMessage) -> dict:
        """
        Invoke LLM with retry logic for quota exhaustion.
        
        Args:
            message: The message to send to the LLM
            
        Returns:
            The response from the LLM
        """
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke([message])
                return response
            except Exception as e:
                error_str = str(e)
                
                if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                    if attempt < self.max_retries - 1:
                        wait_time = self._extract_retry_delay(error_str)
                        print(f"\n⚠️  Quota exceeded! Waiting {wait_time} seconds...")
                        
                        # Wait with countdown
                        for remaining in range(wait_time, 0, -1):
                            print(f"\r⏳ Waiting {remaining}s...", end="", flush=True)
                            time.sleep(1)
                        print("\n✓ Resuming...")
                        continue
                
                # If not quota error or last attempt, raise
                raise

    @staticmethod
    def encode_image(image_path: str) -> str:
        """Encode image to base64 for API transmission."""
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def extract_front_ocr(self, front_image_path: str) -> Dict[str, Optional[str]]:
        """
        Extract OCR data from NID front image.

        Returns fields:
        - english_name
        - bangla_name
        - father_name/spouse_name
        - mother_name
        - dob (yyyy-mm-dd format)
        - nid_no
        """
        prompt = """You are an expert at reading National ID (NID) documents from Bangladesh.
        
Analyze this NID front image and extract the following information in JSON format:
{
    "english_name": "the name in English",
    "bangla_name": "the name in Bengali script",
    "father_spouse_name": "father's name or spouse's name if present",
    "mother_name": "mother's name",
    "dob": "date of birth in yyyy-mm-dd format",
    "nid_no": "the NID number"
}

If any field is not visible or cannot be extracted, use empty string for that field.
Return ONLY valid JSON inside code blocks, no additional text."""

        try:
            # Apply rate limiting
            self._wait_for_rate_limit()

            image_data = self.encode_image(front_image_path)

            # Create message with image and text using LangChain
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

            response = self._invoke_with_retry(message)
            
            # Handle response content - could be string, list, or dict
            if isinstance(response.content, list):
                # Extract text from list of content blocks
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

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            # Extract JSON object from response
            # Find the first { and last } to extract JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}')
            
            if json_start != -1 and json_end != -1:
                result_text = result_text[json_start:json_end+1]

            result = json.loads(result_text)

            # Ensure all expected keys are present with empty strings as defaults
            expected_keys = [
                "english_name",
                "bangla_name",
                "father_spouse_name",
                "mother_name",
                "dob",
                "nid_no",
            ]
            for key in expected_keys:
                if key not in result:
                    result[key] = ""
                # Convert None to empty string
                if result[key] is None:
                    result[key] = ""

            return result

        except Exception as e:
            print(f"Error extracting front OCR from {front_image_path}: {str(e)}")
            return {
                "english_name": "",
                "bangla_name": "",
                "father_spouse_name": "",
                "mother_name": "",
                "dob": "",
                "nid_no": "",
            }

    def extract_back_ocr(self, back_image_path: str) -> Dict[str, Optional[str]]:
        """
        Extract OCR data from NID back image.

        Returns fields:
        - plain_address
        """
        prompt = """You are an expert at reading National ID (NID) documents from Bangladesh.
        
Analyze this NID back image and extract the following information in JSON format:
{
    "plain_address": "the complete address written on the back"
}

If the address field is not visible or cannot be extracted, use empty string.
Return ONLY valid JSON inside code blocks, no additional text."""

        try:
            # Apply rate limiting
            self._wait_for_rate_limit()

            image_data = self.encode_image(back_image_path)

            # Create message with image and text using LangChain
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

            response = self._invoke_with_retry(message)
            
            # Handle response content - could be string, list, or dict
            if isinstance(response.content, list):
                # Extract text from list of content blocks
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

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            # Extract JSON object from response
            # Find the first { and last } to extract JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}')
            
            if json_start != -1 and json_end != -1:
                result_text = result_text[json_start:json_end+1]

            result = json.loads(result_text)

            if "plain_address" not in result:
                result["plain_address"] = ""
            # Convert None to empty string
            if result["plain_address"] is None:
                result["plain_address"] = ""

            return result

        except Exception as e:
            print(f"Error extracting back OCR from {back_image_path}: {str(e)}")
            return {"plain_address": ""}

    def process_image_pair(
        self, front_image_path: str, back_image_path: str
    ) -> Dict[str, Optional[str]]:
        """
        Process a pair of front and back images and extract all OCR data.

        Returns combined dictionary with all fields.
        """
        front_data = self.extract_front_ocr(front_image_path)
        back_data = self.extract_back_ocr(back_image_path)

        # Ensure both are dictionaries
        if not isinstance(front_data, dict):
            front_data = {
                "english_name": "",
                "bangla_name": "",
                "father_spouse_name": "",
                "mother_name": "",
                "dob": "",
                "nid_no": "",
            }
        
        if not isinstance(back_data, dict):
            back_data = {"plain_address": ""}

        # Combine results
        combined_result = {**front_data, **back_data}

        return combined_result
