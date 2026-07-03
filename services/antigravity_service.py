import os
import traceback

from dotenv import load_dotenv
from google import genai

load_dotenv()


class AntigravityService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        print("Loaded API Key:", api_key[:10] + "..." if api_key else "None")

        if not api_key:
            raise Exception("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-2.5-flash"

    def generate_executive_briefing(
        self,
        business_summary
    ):

        prompt = f"""
You are the Chief Strategy Officer of a Fortune 500 Retail Company.

Below is today's business intelligence summary generated from our AI Monitoring Platform.

{business_summary}

Create an Executive Business Briefing.

The report must contain ONLY these sections:

Executive Summary

Top Business Risks

Business Impact

Recommended Actions

Priority Level

Requirements:
- Professional consulting style
- Similar to McKinsey/Bain/Deloitte
- Maximum 350 words
- No markdown
- Clear executive language
"""

        try:

            print("\nCalling Gemini API...")
            print(f"Model: {self.model}")
            print(f"Prompt Length: {len(prompt)}")

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            print("Gemini API call successful.")

            if response is None:
                raise Exception("Gemini returned None")

            if not hasattr(response, "text"):
                print(response)
                raise Exception("Gemini response has no text attribute.")

            return response.text.strip()

        except Exception as e:

            print("\n" + "=" * 70)
            print("GEMINI API ERROR")
            print("=" * 70)

            print(type(e).__name__)
            print(str(e))

            traceback.print_exc()

            print("=" * 70)

            raise