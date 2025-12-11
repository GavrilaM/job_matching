"""Module for extracting work experience information from resume text."""
import re
from typing import List, TypedDict, Optional

class DateRange(TypedDict):
    """Type definition for date range information."""
    start_date: str
    end_date: str

class ExperienceInfo(TypedDict):
    """Type definition for experience information."""
    title: Optional[str]
    company: Optional[str]
    date_range: Optional[DateRange]
    responsibilities: List[str]

class ExperienceExtractor:
    """Handles extraction of work experience information."""

    # Job title patterns
    TITLE_PREFIXES = [
        'Senior', 'Lead', 'Principal', 'Junior', 'Staff', 'Chief',
        'Associate', 'Director', 'Manager', 'Head'
    ]

    TITLE_DOMAINS = [
        'Software', 'Systems', 'Data', 'Full Stack', 'Frontend', 'Backend',
        'DevOps', 'Cloud', 'Machine Learning', 'AI', 'Mobile', 'Web'
    ]

    TITLE_ROLES = [
        'Engineer', 'Developer', 'Architect', 'Manager', 'Consultant',
        'Analyst', 'Specialist', 'Lead', 'Administrator', 'Designer'
    ]

    def __init__(self):
        """Initialize experience patterns."""
        # Build job title pattern dynamically
        title_pattern = (
            f'(?:{"|".join(self.TITLE_PREFIXES)})?\s*'
            f'(?:{"|".join(self.TITLE_DOMAINS)})?\s*'
            f'(?:{"|".join(self.TITLE_ROLES)})'
        )

        self.patterns = {
            'job_title': title_pattern,
            'company': r'(?:at|with|for)?\s([A-Z][A-Za-z0-9\s&]+(?:Inc\.?|Corp\.?|Ltd\.?|LLC\.?|Company|Co\.?)?)',
            'date': r'(?:(?:19|20)\d{2})\s*(?:-|to|–)\s*(?:(?:19|20)\d{2}|Present|Current)',
            'bullet_point': r'[-•]\s*([^\n]+)'
        }

        # Compile patterns for better performance
        self.compiled_patterns = {
            key: re.compile(pattern) for key, pattern in self.patterns.items()
        }

    @staticmethod
    def _parse_date_range(date_str: str) -> DateRange:
        """
        Parse date range into start and end dates.

        Args:
            date_str (str): Date range string (e.g., "2020-Present" or "2018-2020")

        Returns:
            DateRange: Dictionary containing start and end dates
        """
        parts = re.split(r'\s*(?:-|to|–)\s*', date_str)
        return {
            'start_date': parts[0].strip(),
            'end_date': parts[1].strip() if len(parts) > 1 else 'Present'
        }

    def _extract_responsibilities(self, text: str) -> List[str]:
        """
        Extract bullet-pointed responsibilities from text.

        Args:
            text (str): Text containing responsibilities

        Returns:
            List[str]: List of responsibilities
        """
        responsibilities = self.compiled_patterns['bullet_point'].findall(text)
        return [r.strip() for r in responsibilities if r.strip()]

    def extract_experience(self, text: str) -> List[ExperienceInfo]:
        """
        Extract work experience information from text.

        Args:
            text (str): Experience section text

        Returns:
            List[ExperienceInfo]: List of work experience entries
        """
        experience_entries: List[ExperienceInfo] = []

        # Split into potential job entries
        entries = re.split(r'\n(?=[A-Z][a-z]+\s)', text)

        for entry in entries:
            experience_info: ExperienceInfo = {
                'title': None,
                'company': None,
                'date_range': None,
                'responsibilities': []
            }

            # Extract job title
            title_match = self.compiled_patterns['job_title'].search(entry)
            if title_match:
                experience_info['title'] = title_match.group().strip()

            # Extract company
            company_match = self.compiled_patterns['company'].search(entry)
            if company_match:
                experience_info['company'] = company_match.group(1).strip()

            # Extract date range
            date_match = self.compiled_patterns['date'].search(entry)
            if date_match:
                experience_info['date_range'] = self._parse_date_range(date_match.group())

            # Extract responsibilities
            experience_info['responsibilities'] = self._extract_responsibilities(entry)

            # Only add if we have essential information
            if experience_info['title'] or experience_info['company']:
                experience_entries.append(experience_info)

        return experience_entries