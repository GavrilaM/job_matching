"""Main module for coordinating resume parsing operations."""
from typing import Dict, Any
from util.text_extractor import TextExtractor
from util.section_extractor import SectionExtractor
from util.contact_extractor import ContactExtractor
from util.skill_extractor import SkillExtractor
from util.education_extractor import EducationExtractor
from util.experience_extractor import ExperienceExtractor
from util.text_utils import TextUtils

class ResumeParser:
    """Coordinates the parsing of different resume sections."""

    def __init__(self):
        """Initialize all necessary extractors."""
        self.text_extractor = TextExtractor()
        self.section_extractor = SectionExtractor()
        self.contact_extractor = ContactExtractor()
        self.skill_extractor = SkillExtractor()
        self.education_extractor = EducationExtractor()
        self.experience_extractor = ExperienceExtractor()

    def parse_resume(self, pdf_file) -> Dict[str, Any]:
        """
        Parse a resume PDF and extract all relevant information.

        Args:
            pdf_file: File object containing the PDF resume

        Returns:
            Dict[str, Any]: Structured resume information
        """
        try:
            # Extract raw text from PDF
            text = self.text_extractor.extract_text_from_pdf(pdf_file)

            if not text:
                raise ValueError("No text could be extracted from the PDF")

            # Clean text
            text = TextUtils.clean_text(text)

            # Extract all sections first
            sections = self.section_extractor.extract_sections(text)

            # Parse each component using relevant section content
            parsed_data = {
                'contact': self.contact_extractor.extract_contact_info(text),
                'education': self.education_extractor.extract_education(
                    sections.get('education', text)
                ),
                'experience': self.experience_extractor.extract_experience(
                    sections.get('experience', text)
                ),
                'skills': self.skill_extractor.extract_skills(
                    sections.get('skills', text)
                ),
                'sections': sections
            }

            # Validate parsed data
            if not any(parsed_data.values()):
                raise ValueError("No meaningful information could be extracted from the resume")

            return parsed_data

        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")