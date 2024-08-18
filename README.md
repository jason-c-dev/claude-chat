# Claude Speech Chat

## Overview

Claude Speech Chat is a Python-based interactive chat application that combines the power of Anthropic's Claude AI model with Amazon Polly's text-to-speech functionality. This application allows users to have spoken conversations with an AI assistant, creating an engaging and accessible chat experience.

## Features

- Interactive text chat with Claude AI
- Text-to-speech conversion of AI responses using Amazon Polly
- Conversation history management
- Configurable system prompts and AI models
- Command system for various functions (help, history, clear, etc.)

## Requirements

- Python 3.7+
- An Anthropic API key
- AWS credentials configured for Amazon Polly access

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jason-c-dev/claude-chat.git
   cd claude-chat
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory with the following content:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

2. Ensure your AWS credentials are properly configured. You can do this by setting up the AWS CLI or by creating a `~/.aws/credentials` file.

## Usage

Run the application:
```
python main.py
```

Once the application starts, you can begin chatting with the AI. Type your messages and press Enter to send them. The AI's responses will be spoken aloud using text-to-speech.

### Available Commands

- `help`: Shows all available commands and their descriptions.
- `history`: Displays the conversation history.
- `clear`: Clears the conversation history.
- `system`: Shows the current system prompt.
- `system prompt: [new prompt]`: Updates the system prompt, clears history, and restarts.
- `model`: Displays the current Claude model.
- `model change: [model]`: Changes the Claude model.
- `exit` or `quit`: Exits the chat application.


## Customization

- You can modify the default system prompt in the `load_config` method of the `ClaudeSpeechChat` class.
- To change the voice used for text-to-speech, modify the `VoiceId` parameter in the `text_to_speech` method.

## Error Handling and Retries

The application implements retry logic for API errors when communicating with the Claude API. It will attempt to retry the request up to 5 times with exponential backoff before giving up.

## Asynchronous Operation

This application uses Python's `asyncio` for efficient handling of concurrent operations, particularly useful for managing the text-to-speech conversion and playback while continuing to process the AI's response.

## Cross-Platform Considerations

The current implementation of Claude Speech Chat uses the `playsound` library for audio playback, which has different behaviors across operating systems:

### macOS (Darwin)
The application is primarily tested on macOS. It should work out of the box on this platform.

### Windows
On Windows, you may need to install a specific version of `playsound`:

```
pip install playsound==1.2.2
```

Note: Later versions of `playsound` may have issues on Windows. If you encounter problems, try downgrading to version 1.2.2.

### Linux
For Linux systems, you'll need to install GStreamer and the Python GObject Introspection packages. On Ubuntu or Debian-based systems, you can do this with:

```
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
sudo apt-get install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
pip install pycairo
pip install PyGObject
pip install playsound
```

### Alternative Audio Playback Methods

If you encounter issues with `playsound` on your system, consider these alternatives:

1. **pydub**: A more robust cross-platform audio library.
   ```
   pip install pydub
   ```
   You'll also need to install FFmpeg on your system.

2. **pygame**: Another cross-platform option for audio playback.
   ```
   pip install pygame
   ```

To use these alternatives, you'll need to modify the `play_audio` method in the `ClaudeSpeechChat` class.

## Troubleshooting

- If you encounter issues with the Anthropic API, ensure your API key is correct and you have sufficient quota.
- For AWS Polly issues, verify that your AWS credentials are correctly configured and you have the necessary permissions.
- If you're having problems with audio playback:
  - Ensure that your system's audio output is properly configured.
  - Check that you have the necessary audio codecs installed for MP3 playback.
  - On Linux, make sure you have the required GStreamer plugins installed.
  - If issues persist, try one of the alternative audio playback methods mentioned above.

## Contributing

Contributions to improve Claude Speech Chat are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Disclaimer

This application is designed as a general-purpose AI chat tool with speech capabilities. It should not be used for critical decision-making or as a substitute for professional advice in any field.