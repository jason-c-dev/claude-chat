# claude_speech_chat.py
import asyncio
import re
import logging
from config import Config
from history import History
from claude_client import ClaudeClient
from text_to_speech import TextToSpeech
from command_handler import CommandHandler

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class ClaudeSpeechChat:
    def __init__(self, api_key):
        self.config = Config()
        self.history = History()
        self.claude_client = ClaudeClient(api_key, self.config.model)
        self.tts = TextToSpeech()
        self.command_handler = CommandHandler(self.config, self.history)

    async def process_response(self, user_input):
        if not user_input.strip():
            print("Empty input. Please type something.")
            return

        self.history.add_message("user", user_input)
        messages = self.history.get_messages_for_api()
        
        logger.debug(f"Messages to send to API: {messages}")

        full_response = ""
        current_sentence = ""
        sentence_queue = asyncio.Queue()
        audio_queue = asyncio.Queue()

        async def prepare_audio():
            while True:
                sentence = await sentence_queue.get()
                if sentence is None:
                    await audio_queue.put(None)
                    break
                audio_file = await self.tts.convert_to_speech(sentence)
                await audio_queue.put(audio_file)
                sentence_queue.task_done()

        async def play_audio():
            while True:
                audio_file = await audio_queue.get()
                if audio_file is None:
                    break
                await asyncio.to_thread(self.tts.play_audio, audio_file)
                audio_queue.task_done()

        audio_preparer = asyncio.create_task(prepare_audio())
        audio_player = asyncio.create_task(play_audio())

        try:
            async for chunk in self.claude_client.get_response(messages, self.config.system_prompt):
                print(chunk, end='', flush=True)
                full_response += chunk
                current_sentence += chunk

                sentences = self.split_sentences(current_sentence)
                for sentence in sentences[:-1]:
                    if sentence.strip():
                        await sentence_queue.put(sentence.strip())
                
                current_sentence = sentences[-1] if sentences else ""

            if current_sentence.strip():
                await sentence_queue.put(current_sentence.strip())
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            full_response = "I'm sorry, but I encountered an error. Could you please try again?"

        await sentence_queue.put(None)
        await audio_preparer
        await audio_player

        print("\n")

        if full_response.strip():
            self.history.add_message("assistant", full_response)
        await self.history.save_history()
        
        logger.debug(f"Updated history after processing: {self.history.messages}")

    def split_sentences(self, text):
        splits = re.split(r'([.!?])', text)
        sentences = []
        current = ""
        for i, split in enumerate(splits):
            current += split
            if i % 2 == 1 and split in ['.', '!', '?']:
                sentences.append(current.strip())
                current = ""
        if current:
            sentences.append(current.strip())
        return sentences

    async def run(self):
        await self.history.load_history()
        print("Welcome to Claude Speech Chat!")
        print("Type 'help' to see available commands.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                print("Empty input. Please type something.")
                continue
            if self.command_handler.handle_command(user_input):
                continue
            print("Claude is thinking...")
            await self.process_response(user_input)
        print("Thank you for using Claude Speech Chat. Goodbye!")