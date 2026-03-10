import httpx
from config.settings import settings

class AIService:
    @staticmethod
    async def get_response(prompt: str, system_message: str = "You are a professional AI sales voice assistant for GenLab. IMPORTANT: Write ALL responses in ROMANIZED TAMIL (Tamil words spelled in English letters, also called Tanglish). Do NOT use Tamil script. Do NOT use Unicode Tamil characters. Example: say 'Vanakkam' not 'வணக்கம்'."):
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
        system_msg = "You are a professional AI sales voice assistant for GenLab. IMPORTANT: Write ALL responses using ROMANIZED TAMIL only (Tamil words in English letters / Tanglish). Do NOT use Tamil script or Unicode Tamil characters. Example style: 'Vanakkam! Naan GenLab-in AI assistant. Ungal thozhilil engal AI thozhilnuttpam ethuvum udavathu?"
        prompt = f"""
        A potential customer named {customer_name} just requested a call from our website.
        Greet them warmly and introduce GenLab as an AI automation company.
        Ask how you can help their business today.
        Write ONLY in Romanized Tamil (Tanglish) - Tamil words spelled in English letters.
        Keep it under 40 words.
        """
        return await AIService.get_response(prompt, system_msg)
