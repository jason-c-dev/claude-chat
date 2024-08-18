import os
import asyncio
from dotenv import load_dotenv
from claude_speech_chat import ClaudeSpeechChat

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("ANTHROPIC_API_KEY")
    chat = ClaudeSpeechChat(api_key)
    asyncio.run(chat.run())