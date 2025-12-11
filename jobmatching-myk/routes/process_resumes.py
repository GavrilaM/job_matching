"""Module for handling resume processing endpoints."""
from flask import request
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
from util.cvparser import preprocess_text
from util.cvreader import PDFReader
from util.applicantscoring import ApplicantScorer

# Create a namespace for the process resumes endpoint
api = Namespace('process_resumes', description='Process resumes for job matching')

# File upload parser
upload_parser = api.parser()
upload_parser.add_argument('resume',
                           type=FileStorage,
                           location='files',
                           required=True,
                           help='PDF resume file')
upload_parser.add_argument('job_description',
                           type=str,
                           location='form',
                           required=True,
                           help='Job description text')

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/')
class ProcessResumes(Resource):
    @api.expect(upload_parser)
    def post(self):
        """
        Process a resume PDF file and return extracted information and matching score.

        Returns:
            tuple: Response containing processed data and HTTP status code
        """
        args = upload_parser.parse_args()

        # Check if resume file was uploaded
        if 'resume' not in request.files:
            return {'error': 'No resume file provided'}, 400

        resume_file = request.files['resume']
        job_description = args['job_description']

        # Check if a file was actually selected
        if resume_file.filename == '':
            return {'error': 'No selected file'}, 400

        # Validate file type
        if not allowed_file(resume_file.filename):
            return {'error': 'Invalid file type. Only PDF files are allowed'}, 400

        try:
            # Initialize PDF reader
            pdf_reader = PDFReader()

            # Extract text from PDF
            resume_text = pdf_reader.extract_text_from_pdf(resume_file)

            if not resume_text:
                return {'error': 'Could not extract text from PDF'}, 400

            # Preprocess the extracted text
            cleaned_resume = preprocess_text(resume_text)

            # Initialize scorer and calculate score
            scorer = ApplicantScorer()
            scorer.fit([job_description])
            score = scorer.score_applicants([cleaned_resume], [job_description])[0]

            # Get categorized information
            categories = pdf_reader.categorize_resume(resume_text)

            return {
                'message': 'Resume processed successfully',
                'score': score,
                'categories': categories,
                'extracted_text': resume_text
            }, 200

        except Exception as e:
            return {'error': f'Error processing resume: {str(e)}'}, 500