import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
load_dotenv()
# Configure your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini Pro model
model = genai.GenerativeModel("models/gemini-2.5-pro")

def extract_job_details(user_input):
    prompt = f"""
    Extract the job role and location from this sentence:
    "{user_input}"

    Respond strictly in JSON only:
    {{
      "role": "<role or empty string>",
      "location": "<location or empty string>"
    }}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        if response.candidates and response.candidates[0].content.parts:
            content = response.candidates[0].content.parts[0].text.strip()
            return json.loads(content)

        else:
            print("⚠️ Gemini returned no text:", response)
            return None

    except Exception as e:
        print("Gemini extraction error:", e)
        return None
