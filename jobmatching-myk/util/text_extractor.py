"""Module for handling text extraction from PDF files."""
import PyPDF2

class TextExtractor:
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_file: File object containing the PDF

        Returns:
            str: Extracted text from the PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_parts = []

            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())

            return " ".join(text_parts).strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")