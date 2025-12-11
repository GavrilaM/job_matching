"""Module for extracting education information from resume text."""
import re
from typing import List, TypedDict

class EducationInfo(TypedDict):
    """Type definition for education information."""
    degree: str | None
    university: str | None
    graduation_date: str | None
    field: str | None

class EducationExtractor:
    """Handles extraction of education-related information."""

    def __init__(self):
        """Initialize education patterns."""
        self.education_patterns = {
            'degree': [
                r'(?:Bachelor|Master|Ph\.?D|B\.?S|M\.?S|B\.?A|M\.?A|M\.?B\.?A)\.?\s(?:of|in|degree in)?\s[A-Za-z\s]+',
                r'(?:Associate|Doctorate|Post Graduate)',
            ],
            'university': [
                r'(?:University|College|Institute|School)\s(?:of|in)?\s[A-Za-z\s]+',
                r'[A-Z][a-z]+\s(?:University|College|Institute|School)',
            ],
            'graduation': [
                r'(?:19|20)\d{2}(?:\s*-\s*(?:19|20)\d{2}|(?:Present|Current))?',
                r'(?:Graduated|Completed|Expected)\s+(?:in|by)?\s+(?:19|20)\d{2}',
            ]
        }

    def extract_education(self, text: str) -> List[EducationInfo]:
        """
        Extract education information from text.

        Args:
            text (str): Education section text

        Returns:
            List[EducationInfo]: List of education entries with structured information
        """
        education_entries: List[EducationInfo] = []

        # Split into potential education entries
        entries = re.split(r'\n(?=[A-Z])', text)

        for entry in entries:
            education_info: EducationInfo = {
                'degree': None,
                'university': None,
                'graduation_date': None,
                'field': None
            }

            # Extract degree
            for pattern in self.education_patterns['degree']:
                match = re.search(pattern, entry)
                if match:
                    education_info['degree'] = match.group().strip()
                    # Extract field of study
                    field_match = re.search(r'(?:of|in|degree in)\s([A-Za-z\s]+)', match.group())
                    if field_match:
                        education_info['field'] = field_match.group(1).strip()
                    break

            # Extract university
            for pattern in self.education_patterns['university']:
                match = re.search(pattern, entry)
                if match:
                    education_info['university'] = match.group().strip()
                    break

            # Extract graduation date
            for pattern in self.education_patterns['graduation']:
                match = re.search(pattern, entry)
                if match:
                    education_info['graduation_date'] = match.group().strip()
                    break

            # Only add if we have at least a degree or university
            if education_info['degree'] or education_info['university']:
                education_entries.append(education_info)

        return education_entries