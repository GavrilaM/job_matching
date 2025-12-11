"""Module for text processing utilities."""
from typing import List


class TextUtils:
    """Utility class for text processing operations."""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text content.

        Args:
            text (str): Raw text to clean

        Returns:
            str: Cleaned and normalized text
        """
        # Remove extra whitespace
        text = " ".join(text.split())

        # Normalize line breaks
        text = text.replace("\n\n", "\n")

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def split_into_sections(text: str) -> List[str]:
        """
        Split text into logical sections based on line breaks and indentation.

        Args:
            text (str): Text to split into sections

        Returns:
            List[str]: List of text sections
        """
        sections = []
        current_section = []

        for line in text.split('\n'):
            if not line.strip():
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            else:
                current_section.append(line)

        if current_section:
            sections.append('\n'.join(current_section))

        return sections