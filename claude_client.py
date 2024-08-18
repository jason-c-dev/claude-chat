from anthropic import AsyncAnthropic, APIStatusError, APITimeoutError, RateLimitError
import asyncio

class ClaudeClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    async def get_response(self, messages, system_prompt):
        max_retries = 5
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                async with AsyncAnthropic(api_key=self.api_key) as client:
                    stream = await client.messages.create(
                        model=self.model,
                        max_tokens=1024,
                        messages=messages,
                        system=system_prompt,
                        stream=True
                    )

                    async for event in stream:
                        if event.type == "content_block_delta":
                            yield event.delta.text

                return

            except (APIStatusError, APITimeoutError, RateLimitError) as e:
                if attempt < max_retries - 1:
                    print(f"Error occurred: {e}. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Max retries reached. Error: {e}")
                    yield "I'm sorry, but I'm having trouble connecting right now. Please try again later."
