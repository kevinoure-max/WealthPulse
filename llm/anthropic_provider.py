import anthropic
import os
import json
from dotenv import load_dotenv

from llm.base import LLMProvider

load_dotenv()

MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


class AnthropicProvider(LLMProvider):
    def generate_analysis(self, stats: dict) -> str:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        prompt = f"""
You are a financial data analyst providing factual information about French savings products.

All data you need is provided below. Do not use any external knowledge.

Data:
{json.dumps(stats, indent=2)}

Instructions:
1. Write a brief factual summary of the real return situation.
2. Explain what the real return means in concrete euros for the investor.
3. If multiple assets are present in the data, compare their real returns factually.
4. The entire response before the disclaimer must not exceed five sentences.

Strict constraints:
- ONLY use numbers explicitly present in the data above.
- Do NOT recommend or suggest any action ("you should", "consider", "we recommend").
- Do NOT introduce products, rates or assumptions not present in the data.
- Do NOT infer or estimate missing values.
- Only compare assets explicitly included in the provided data.

End your response with exactly this disclaimer on a new line:
"This information is provided for educational purposes only and does not constitute financial advice."
"""
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text
