import PyPDF2
import re
import spacy
from typing import Dict, List, Any


class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

        # Define category patterns
        self.patterns = {
            'education': r'(?i)(education|university|college|bachelor|master|phd|degree)',
            'experience': r'(?i)(experience|work|employment|job|position|company)',
            'skills': r'(?i)(skills|technologies|programming|languages|tools)',
            'certifications': r'(?i)(certification|certificate|certified|license)'
        }

        # Contact information patterns
        self.contact_patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}',
            'linkedin': r'linkedin\.com/\S+'
        }

    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """
        Extracts text content from a PDF file.

        Args:
            pdf_file: The PDF file object to process

        Returns:
            str: Extracted text from the PDF

        Raises:
            Exception: If there's an error processing the PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extracts contact information from the text.

        Args:
            text (str): The text to process

        Returns:
            Dict[str, str]: Dictionary containing extracted contact information
        """
        contact_info = {}
        for key, pattern in self.contact_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                contact_info[key] = matches[0]
        return contact_info

    @staticmethod
    def extract_skills(doc) -> List[str]:
        """
        Extracts skills from the processed document.

        Args:
            doc: spaCy document object

        Returns:
            List[str]: List of unique skills
        """
        skills = []
        relevant_pos = {'NOUN', 'PROPN', 'ADJ'}  # Including adjectives for technical skills

        for token in doc:
            if token.pos_ in relevant_pos and len(token.text) > 2:
                # Convert to lowercase for better deduplication
                skill = token.text.lower()
                skills.append(skill)

        return list(set(skills))  # Remove duplicates

    def categorize_sections(self, text: str) -> Dict[str, List[str]]:
        """
        Categorizes the text into different sections.

        Args:
            text (str): The text to categorize

        Returns:
            Dict[str, List[str]]: Dictionary containing categorized sections
        """
        doc = self.nlp(text)

        categories = {
            'education': [],
            'experience': [],
            'skills': [],
            'certifications': [],
            'contact': self.extract_contact_info(text)
        }

        sentences = [sent.text.strip() for sent in doc.sents]

        for sentence in sentences:
            for category, pattern in self.patterns.items():
                if re.search(pattern, sentence):
                    cleaned_sentence = re.sub(r'\s+', ' ', sentence).strip()
                    if cleaned_sentence and len(cleaned_sentence) > 10:
                        categories[category].append(cleaned_sentence)

        categories['skills'] = self.extract_skills(doc)

        return categories

    def parse_resume(self, pdf_file) -> Dict[str, Any]:
        """
        Main method to parse PDF resume.

        Args:
            pdf_file: The PDF file to parse

        Returns:
            Dict[str, Any]: Parsed resume data in categorized format
        """
        text = self.extract_text_from_pdf(pdf_file)
        return self.categorize_sections(text)
