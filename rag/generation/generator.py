"""LLM generation: produce answers from retrieved context."""

from __future__ import annotations

from ..config import config


class Generator:
    """Generate answers using Claude API with retrieved context."""

    def __init__(self, model: str | None = None):
        self.model = model or config.generation.model
        self.max_tokens = config.generation.max_tokens
        self.temperature = config.generation.temperature
        self._client = None

    def _get_client(self):
        """Lazy-initialize Anthropic client."""
        if self._client is not None:
            return self._client

        import anthropic
        self._client = anthropic.Anthropic()
        return self._client

    def generate(
        self,
        system_prompt: str,
        context_text: str,
        user_message: str,
        stream: bool = False,
    ) -> str | None:
        """Generate a response using the LLM.

        Args:
            system_prompt: System-level instructions
            context_text: Retrieved context blocks
            user_message: The user's question
            stream: If True, yields chunks (for CLI streaming)

        Returns:
            Generated response text, or None if streaming.
        """
        client = self._get_client()

        # Build messages
        messages = [
            {
                "role": "user",
                "content": (
                    f"Here is the relevant context from the research corpus:\n\n"
                    f"<context>\n{context_text}\n</context>\n\n"
                    f"Question: {user_message}"
                ),
            }
        ]

        if stream:
            return self._stream_response(client, system_prompt, messages)

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=messages,
        )

        return response.content[0].text

    def _stream_response(self, client, system_prompt: str, messages: list) -> str:
        """Stream response tokens and return full text."""
        full_text = ""

        with client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_text += text

        print()  # newline after stream
        return full_text
