import os
from dotenv import load_dotenv
from google import genai


def get_gemini_client():
    """
    Creates and returns a Gemini client.
    This function centralizes API configuration.
    """

    # Load environment variables from .env
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

    return genai.Client(api_key=api_key)
