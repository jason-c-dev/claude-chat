# history.py
import json
import aiofiles
import os
import logging

logger = logging.getLogger(__name__)

class History:
    def __init__(self, history_file="chat_history.json"):
        self.messages = []
        self.history_file = history_file

    async def load_history(self):
        if os.path.exists(self.history_file):
            async with aiofiles.open(self.history_file, mode='r') as f:
                self.messages = json.loads(await f.read())
        self.clean_history()

    async def save_history(self):
        self.clean_history()
        async with aiofiles.open(self.history_file, mode='w') as f:
            await f.write(json.dumps(self.messages))

    def add_message(self, role, content):
        if content.strip():  # Only add non-empty messages
            self.messages.append({"role": role, "content": content})

    def clear(self):
        self.messages.clear()

    def clean_history(self):
        self.messages = [msg for msg in self.messages if msg["content"].strip()]

    def get_messages_for_api(self):
        logger.debug(f"Original messages: {self.messages}")
        
        # Ensure the conversation always starts with a user message
        start_index = 0
        for i, msg in enumerate(self.messages):
            if msg["role"] == "user":
                start_index = i
                break
        
        logger.debug(f"Start index: {start_index}")

        # Ensure we have alternating user and assistant messages
        api_messages = []
        for msg in self.messages[start_index:]:
            if not api_messages or api_messages[-1]["role"] != msg["role"]:
                api_messages.append(msg)
            else:
                logger.debug(f"Skipping message due to consecutive roles: {msg}")

        # Ensure the last message is from the user
        if api_messages and api_messages[-1]["role"] == "assistant":
            logger.debug("Removing last assistant message")
            api_messages.pop()

        logger.debug(f"Final API messages: {api_messages}")
        return api_messages