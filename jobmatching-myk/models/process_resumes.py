from flask_restx import fields

# Define the resume model
resume_model = {
    'candidate_id': fields.Integer(required=True, description='Unique identifier for the candidate'),
    'resume': fields.String(required=True, description='The resume text of the candidate')
}

# Define the process resumes model
process_resumes_model = {
    'resumes': fields.List(fields.Nested(resume_model), required=True, description='List of resumes to process'),
    'job_description': fields.String(required=True, description='Job description to match against resumes')
}