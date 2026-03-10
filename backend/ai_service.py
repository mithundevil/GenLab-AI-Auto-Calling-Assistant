import httpx
from config.settings import settings

class AIService:
    @staticmethod
    async def get_response(prompt: str, system_message: str = "You are a professional AI sales assistant for GenLab. Speak ONLY in TAMIL. DO NOT USE ENGLISH."):
        headers = {
            "Authorization": f"Bearer {settings.GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings.GROK_MODEL,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(settings.GROK_API_URL, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error calling AI API: {e}")
            return "மன்னிக்கவும், என்னால் இப்போது பதில் அளிக்க முடியவில்லை. (Sorry, I cannot reply right now.)"

    @staticmethod
    async def generate_intro(customer_name: str):
        system_msg = "You are a professional AI sales assistant for GenLab. Speak ONLY in TAMIL."
        prompt = f"""
        A potential customer named {customer_name} just requested a call.
        Introduce GenLab (AI automation experts) and ask how we can help their business today.
        Speak in fluent, professional Tamil. Keep it under 40 words.
        """
        return await AIService.get_response(prompt, system_msg)
