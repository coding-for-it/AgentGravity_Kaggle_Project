import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AntigravityService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(
            api_key=api_key
        )

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

Requirements

• Professional consulting style
• Similar to McKinsey/Bain/Deloitte
• Maximum 350 words
• No markdown
• No bullet nesting
• Clear executive language
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()