from services.gemini_service import GeminiService


service = GeminiService()

prompt = """
You are a Business Intelligence Assistant.

A company experienced a revenue drop because of inventory shortage.

Provide a short executive summary in less than 80 words.
"""

response = service.generate(prompt)

print("\n")
print("=" * 60)
print(response)
print("=" * 60)