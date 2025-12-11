"""Module for extracting contact information from text."""
import re
from typing import List, Dict

class ContactExtractor:
    def __init__(self):
        """Initialize contact patterns."""
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'address': r'\d+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Trail|Trl|Way|Place|Pl|Square|Sq)[,\s]+[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?',
            'linkedin': r'linkedin\.com/in/[\w-]+'
        }

    def extract_contact_info(self, text: str) -> Dict[str, List[str]]:
        """
        Extract contact information from text.

        Args:
            text (str): Text to extract contact information from

        Returns:
            Dict[str, List[str]]: Dictionary of contact information by type
        """
        contact_info = {
            'email': [],
            'phone': [],
            'address': [],
            'linkedin': []
        }

        # Process each line to maintain context
        lines = text.split('\n')
        for line in lines:
            for contact_type, pattern in self.patterns.items():
                matches = re.findall(pattern, line, re.IGNORECASE)
                if matches:
                    contact_info[contact_type].extend(matches)

        # Remove duplicates while preserving order
        for key in contact_info:
            contact_info[key] = list(dict.fromkeys(contact_info[key]))

        return contact_info