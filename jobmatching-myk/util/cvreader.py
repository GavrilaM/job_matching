"""Main module for processing and categorizing resumes."""
import spacy
from typing import Dict, List
from util.text_extractor import TextExtractor
from util.contact_extractor import ContactExtractor
from util.skill_extractor import SkillExtractor

class PDFReader:
    def __init__(self):
        """Initialize the PDFReader with required components."""
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_extractor = SkillExtractor()

    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """Delegate PDF text extraction to TextExtractor."""
        return TextExtractor.extract_text_from_pdf(pdf_file)

    def categorize_resume(self, text: str) -> Dict[str, List[str]]:
        """
        Categorize resume text into different sections.

        Args:
            text (str): The text content of the resume

        Returns:
            Dict[str, List[str]]: Categorized sections of the resume
        """
        doc = self.nlp(text)

        categories = {
            'education': [],
            'experience': [],
            'skills': [],
            'contact': []
        }

        # Extract education information
        education_keywords = ['education', 'university', 'college', 'degree', 'bachelor', 'master', 'phd']
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in education_keywords):
                categories['education'].append(sent.text.strip())

        # Extract work experience
        experience_keywords = ['experience', 'work', 'employment', 'job', 'position']
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in experience_keywords):
                categories['experience'].append(sent.text.strip())

        # Extract skills using SkillExtractor
        categories['skills'] = self.skill_extractor.extract_skills(doc)

        # Extract contact information using ContactExtractor
        categories['contact'] = ContactExtractor.extract_contact_info(text)

        return categories