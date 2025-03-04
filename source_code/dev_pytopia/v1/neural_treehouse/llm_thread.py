import textwrap
from typing import Any, Dict, List, Union

from foundation.v1 import CustomLogger

logger = CustomLogger(log_level="INFO")


class LLMThread:
    COLORS = {
        "border": "\033[38;5;75m",
        "header": "\033[1;36m",
        "role": "\033[1;33m",
        "content": "\033[0;37m",
        "reset": "\033[0m",
    }

    def __init__(self) -> None:
        super().__init__()
        self.messages: List[Any] = []

    @classmethod
    def add_first_message(cls, role: Union[str, None], content: str) -> "LLMThread":
        instance = cls()
        instance.add_message(role, content)
        return instance

    @classmethod
    def add_first_message_with_image_data(
        cls, role: str, textual_prompt: str, image_data: Union[str, List[str]]
    ) -> "LLMThread":
        instance = cls()
        instance.add_message_with_images(role, textual_prompt, image_data)
        return instance

    def add_message(self, role: Union[str, None], content: str) -> None:
        self.messages.append({"role": role, "content": content} if role else {"content": content})

    def add_message_with_images(
        self,
        role: str,
        textual_prompt: str,
        image_data: Union[str, List[str]],
    ) -> None:
        content: List[Dict[str, Any]] = [{"type": "text", "text": textual_prompt}]
        content += [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in image_data
        ]
        self.messages.append({"role": role, "content": content})

    def get_printable_representation(self) -> str:
        width = 220
        border = "═" * (width - 2)

        lines = [
            f"{self.COLORS['border']}╭{border}╮{self.COLORS['reset']}",
            self._format_line(
                f"{self.COLORS['header']}LLM Thread ID: {'None'}{self.COLORS['reset']}",
                width,
            ),
            f"{self.COLORS['border']}├{border}┤{self.COLORS['reset']}",
            self._format_line(f"{self.COLORS['header']}Messages:{self.COLORS['reset']}", width),
            f"{self.COLORS['border']}├{border}┤{self.COLORS['reset']}",
        ]

        for i, msg in enumerate(self.messages, start=1):
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")

            lines.append(
                self._format_line(
                    f"{self.COLORS['header']}Message {i} | Role: {self.COLORS['role']}{role}{self.COLORS['reset']}",
                    width,
                )
            )
            lines.append(f"{self.COLORS['border']}├{border}┤{self.COLORS['reset']}")

            if isinstance(content, list):
                for item in content:
                    if item["type"] == "image_url":
                        lines.append(
                            self._format_line(
                                f"{self.COLORS['content']}[Image: Base64 encoded]{self.COLORS['reset']}",
                                width,
                            )
                        )
                    else:
                        lines.extend(self._format_text_content(item["text"], width))
            else:
                lines.extend(self._format_text_content(content, width))

            lines.append(f"{self.COLORS['border']}├{border}┤{self.COLORS['reset']}")

        lines[-1] = f"{self.COLORS['border']}╰{border}╯{self.COLORS['reset']}"
        return "\n".join(lines)

    def _format_text_content(self, text: str, width: int) -> List[str]:
        content_width = width - 4
        lines = []

        for raw_line in text.split("\n"):
            if not raw_line.strip():
                lines.append(self._format_line("", width))
                continue

            wrapped = textwrap.wrap(raw_line, width=content_width)
            if not wrapped:
                lines.append(self._format_line("", width))
            else:
                for wline in wrapped:
                    lines.append(
                        self._format_line(
                            f"{self.COLORS['content']}{wline}{self.COLORS['reset']}",
                            width,
                        )
                    )

        return lines

    @classmethod
    def _format_line(cls, line: str, width: int) -> str:
        visible_length = len(line) - len("".join(code for code in cls.COLORS.values() if code in line))
        padding = width - 4 - visible_length
        return f"{cls.COLORS['border']}│{cls.COLORS['reset']} {line}{' ' * padding} {cls.COLORS['border']}│{cls.COLORS['reset']}"

    def remove_last_message(self) -> Dict[str, Any]:
        if not self.messages:
            raise IndexError("Cannot remove last message from an empty thread")
        return self.messages.pop()

    def clear(self) -> None:
        """Clears all messages from the thread."""
        self.messages = []
