import boto3
from datetime import datetime
import aiofiles
from playsound import playsound
import os

class TextToSpeech:
    def __init__(self):
        self.polly_client = boto3.client('polly')

    async def convert_to_speech(self, text):
        response = self.polly_client.synthesize_speech(
            Engine='generative',
            Text=text,
            OutputFormat='mp3',
            VoiceId='Ruth'
            #VoiceId='Amy'
        )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        mp3_filename = f"speech_{timestamp}.mp3"

        async with aiofiles.open(mp3_filename, 'wb') as f:
            await f.write(response['AudioStream'].read())

        return mp3_filename

    def play_audio(self, filename):
        playsound(filename, True)
        os.remove(filename)