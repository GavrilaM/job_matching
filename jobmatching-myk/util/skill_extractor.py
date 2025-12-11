"""Module for extracting skills from resume text."""
import re
from typing import Dict, List, Set

class SkillExtractor:
    """Handles extraction of skills from resume text."""

    # Move skill categories to a separate configuration file
    SKILL_CATEGORIES = {
        'programming_languages': {
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift',
            'Kotlin', 'Go', 'Rust', 'TypeScript', 'Scala', 'R', 'MATLAB'
        },
        'frameworks': {
            'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'Express',
            'Node.js', '.NET', 'Laravel', 'Ruby on Rails', 'TensorFlow', 'PyTorch'
        },
        'databases': {
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle',
            'SQL Server', 'SQLite', 'DynamoDB', 'Elasticsearch'
        },
        'tools': {
            'Git', 'Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Azure', 'GCP',
            'Linux', 'Nginx', 'Apache', 'Jira', 'Confluence'
        },
        'soft_skills': {
            'Leadership', 'Communication', 'Problem Solving', 'Team Management',
            'Project Management', 'Agile', 'Scrum', 'Critical Thinking',
            'Time Management', 'Collaboration', 'Mentoring'
        }
    }

    def __init__(self):
        """Initialize skill patterns."""
        self.patterns = self._compile_skill_patterns()

    def _compile_skill_patterns(self) -> Dict[str, re.Pattern]:
        """
        Compile regex patterns for skill matching.

        Returns:
            Dict[str, re.Pattern]: Dictionary of compiled regex patterns
        """
        return {
            category: self._create_pattern(skills)
            for category, skills in self.SKILL_CATEGORIES.items()
        }

    @staticmethod
    def _create_pattern(skills: Set[str]) -> re.Pattern:
        """
        Create a regex pattern for matching skills.

        Args:
            skills (Set[str]): Set of skills to match

        Returns:
            re.Pattern: Compiled regex pattern
        """
        escaped_skills = map(re.escape, skills)
        pattern = r'\b(' + '|'.join(escaped_skills) + r')\b'
        return re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def _normalize_skill(skill: str) -> str:
        """
        Normalize skill name for consistent matching.

        Args:
            skill (str): Skill name to normalize

        Returns:
            str: Normalized skill name
        """
        return skill.lower().strip()

    def _extract_category_skills(self, text: str, category: str) -> Set[str]:
        """
        Extract skills for a specific category from text.

        Args:
            text (str): Text to extract skills from
            category (str): Category of skills to extract

        Returns:
            Set[str]: Set of extracted skills
        """
        matches = self.patterns[category].findall(text)
        return {match.strip() for match in matches}

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract and categorize skills from text.

        Args:
            text (str): Resume text content

        Returns:
            Dict[str, List[str]]: Categorized skills
        """
        skills = {
            'technical': set(),
            'soft': set()
        }

        # Process text by lines to maintain context
        lines = text.split('\n')
        for line in lines:
            if not line.strip():
                continue

            # Extract technical skills
            for category in ['programming_languages', 'frameworks', 'databases', 'tools']:
                category_skills = self._extract_category_skills(line, category)
                skills['technical'].update(category_skills)

            # Extract soft skills
            soft_skills = self._extract_category_skills(line, 'soft_skills')
            skills['soft'].update(soft_skills)

        # Convert sets to sorted lists for consistent output
        return {
            'technical': sorted(list(skills['technical'])),
            'soft': sorted(list(skills['soft']))
        }