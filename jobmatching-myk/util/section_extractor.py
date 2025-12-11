"""Module for extracting and identifying different resume sections."""
import re
from typing import Dict, List, Optional

class SectionExtractor:
    """Handles identification and extraction of resume sections."""

    def __init__(self):
        """Initialize section patterns and keywords."""
        self.section_patterns = {
            'summary': [
                r'(?i)^(?:professional\s+)?summary',
                r'(?i)^(?:career\s+)?objective',
                r'(?i)^profile',
                r'(?i)^about'
            ],
            'education': [
                r'(?i)^education(?:al)?(?:\s+background)?',
                r'(?i)^academic(?:s|al)?(?:\s+background)?',
                r'(?i)^qualifications?'
            ],
            'experience': [
                r'(?i)^(?:work\s+)?experience',
                r'(?i)^employment(?:\s+history)?',
                r'(?i)^work\s+history',
                r'(?i)^career(?:\s+history)?'
            ],
            'skills': [
                r'(?i)^(?:technical\s+)?skills',
                r'(?i)^competencies',
                r'(?i)^expertise',
                r'(?i)^technologies'
            ],
            'projects': [
                r'(?i)^projects?(?:\s+experience)?',
                r'(?i)^portfolio'
            ],
            'certifications': [
                r'(?i)^certifications?',
                r'(?i)^certificates?',
                r'(?i)^accreditations?'
            ]
        }

        # Compile patterns for better performance
        self.compiled_patterns = {
            section: [re.compile(pattern) for pattern in patterns]
            for section, patterns in self.section_patterns.items()
        }

    def _identify_section(self, line: str) -> Optional[str]:
        """
        Identify which section a line belongs to.

        Args:
            line (str): Line of text to analyze

        Returns:
            Optional[str]: Section name if identified, None otherwise
        """
        for section, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.match(line):
                    return section
        return None

    def extract_sections(self, text: str) -> Dict[str, List[str]]:
        """
        Identify and extract different sections from the resume.

        Args:
            text (str): Resume text content

        Returns:
            Dict[str, List[str]]: Sections and their content
        """
        sections: Dict[str, List[str]] = {}
        current_section: Optional[str] = None
        current_content: List[str] = []

        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a section header
            section = self._identify_section(line)

            if section:
                # Save previous section content
                if current_section and current_content:
                    sections[current_section] = current_content

                # Start new section
                current_section = section
                current_content = []
            elif current_section:
                current_content.append(line)

        # Add last section
        if current_section and current_content:
            sections[current_section] = current_content

        return sections