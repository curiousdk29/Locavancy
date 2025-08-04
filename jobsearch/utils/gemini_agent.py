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
    prompt = f"""Extract the job role and location from this sentence:
    "{user_input}"

    Return a JSON with keys: "role" and "location".
    If either is missing, return it as an empty string.
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Clean the Markdown code block if present
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()

        print("Gemini raw response:", repr(content))  # For debugging

        import json
        return json.loads(content)

    except Exception as e:
        print("Gemini extraction error:", e)
        return {"role": "", "location": ""}

