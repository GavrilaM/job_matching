from flask_restx import Namespace, Resource
from models.job import JobModel
from flask import request
from auth import authentication

api = Namespace('jobs', "APIs related to job listings")
job_model = JobModel(api)
job_dummy_data = []

@api.doc(security="apikey")
@authentication
@api.route('/')
class JobResource(Resource):
    @api.marshal_with(job_model.get_job())
    def get(self):
        """List all job listings"""
        return job_dummy_data, 200

    @api.doc(security="apikey")
    @authentication
    @api.expect(job_model.get_job())  # Expecting the job model for input
    @api.marshal_with(job_model.get_job())  # Marshaling the response
    def post(self):
        """Add a new job listing"""
        new_job = {
            "id": str(len(job_dummy_data) + 1),
            "title": request.json.get("title"),
            "description": request.json.get("description"),
            "company": request.json.get("company"),
            "location": request.json.get("location"),
            "skills": request.json.get("skills")
        }
        job_dummy_data.append(new_job)
        return new_job, 201

    @api.response(204, "Job listing deleted successfully")
    @api.doc(
        params={
            "id": "Job listing ID"
        }
    )
    def delete(self):
        """Delete a job listing"""
        global job_dummy_data
        job_dummy_data = [job for job in job_dummy_data if job['id'] != id]
        return 'delete successfully', 204