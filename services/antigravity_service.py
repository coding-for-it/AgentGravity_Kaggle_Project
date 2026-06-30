import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(api_key[:10])   # temporarily add this

client = genai.Client(api_key=api_key)

class AntigravityService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("GEMINI_API_KEY not found.")

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"

    def generate_executive_briefing(self, business_summary):

        prompt = f"""
You are the Chief Strategy Officer of a large retail company.

Below is today's business intelligence summary.

{business_summary}

Write a professional executive briefing.

The response must contain exactly these sections.

Executive Summary

Top Business Risks

Business Impact

Recommended Actions

Priority Level

Keep the response under 350 words.

Do not use markdown.

Write like a McKinsey / Deloitte consultant.
"""

        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt

        )

        return response.text.strip()