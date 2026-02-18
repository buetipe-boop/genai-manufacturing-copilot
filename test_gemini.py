import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a test prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain generative AI in manufacturing in 5 bullet points."
)

print(response.text)
