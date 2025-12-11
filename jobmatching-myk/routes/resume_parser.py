"""Module for handling resume parsing endpoints."""
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from util.resume_parser import ResumeParser
from auth import authentication

# Create namespace
api = Namespace('resume_parser', description='APIs related to Resume Parsing')

# File upload parser
upload_parser = api.parser()
upload_parser.add_argument('resume',
                           type=FileStorage,
                           location='files',
                           required=True,
                           help='PDF resume file')

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.

    Args:
        filename (str): Name of the uploaded file

    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/parse')
class ResumeParserResource(Resource):
    @api.doc(security="apikey")
    @authentication
    @api.expect(upload_parser)
    def post(self):
        """
        Parse and categorize sections from a PDF resume.

        Returns:
            tuple: Response containing parsed resume data and HTTP status code
        """
        # Check if file was uploaded
        if 'resume' not in request.files:
            return {'error': 'No resume file provided'}, 400

        resume_file = request.files['resume']

        # Validate file selection
        if resume_file.filename == '':
            return {'error': 'No selected file'}, 400

        # Validate file type
        if not allowed_file(resume_file.filename):
            return {'error': 'Invalid file type. Only PDF files are allowed'}, 400

        try:
            # Initialize parser and process resume
            parser = ResumeParser()
            parsed_data = parser.parse_resume(resume_file)

            return {
                'message': 'Resume parsed successfully',
                'data': parsed_data
            }, 200

        except Exception as e:
            return {'error': f'Error processing resume: {str(e)}'}, 500