from flask_restx import fields

class JobModel:
    def __init__(self, api):
        self.api = api
        self.model = api.model('Job', {
            'id': fields.String(required=True, description='Job ID'),
            'title': fields.String(required=True, description='Job title'),
            'description': fields.String(required=True, description='Job description'),
            'company': fields.String(required=True, description='Company name'),
            'location': fields.String(required=True, description='Job location'),
            'skills': fields.List(fields.String, required=True, description='Required skills')
        })

    def get_job(self):
        return self.model