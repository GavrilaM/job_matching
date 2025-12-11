"""Models for Resume Parser API responses."""
from flask_restx import fields
from typing import Dict, Any


class ResumeParserModel:
    """Models for Resume Parser API responses."""

    def __init__(self, namespace):
        """Initialize models with namespace."""
        self.ns = namespace
        self.base_models = self._create_base_models()

    def _create_base_models(self) -> Dict[str, Any]:
        """Create base models for reuse across response models."""
        return {
            'contact': self.ns.model('ContactInfo', {
                'email': fields.String(description='Email address'),
                'phone': fields.String(description='Phone number'),
                'address': fields.String(description='Physical address'),
                'linkedin': fields.String(description='LinkedIn profile URL')
            }),

            'education': self.ns.model('Education', {
                'degree': fields.String(description='Degree obtained'),
                'university': fields.String(description='Institution name'),
                'graduation_date': fields.String(description='Graduation date'),
                'field': fields.String(description='Field of study')
            }),

            'experience': self.ns.model('Experience', {
                'title': fields.String(description='Job title'),
                'company': fields.String(description='Company name'),
                'date_range': fields.Nested(self.ns.model('DateRange', {
                    'start_date': fields.String(description='Start date'),
                    'end_date': fields.String(description='End date')
                })),
                'responsibilities': fields.List(
                    fields.String,
                    description='List of job responsibilities'
                )
            }),

            'skills': self.ns.model('Skills', {
                'technical': fields.List(
                    fields.String,
                    description='Technical skills'
                ),
                'soft': fields.List(
                    fields.String,
                    description='Soft skills'
                )
            }),

            'certifications': self.ns.model('Certification', {
                'name': fields.String(description='Certification name'),
                'issuer': fields.String(description='Issuing organization'),
                'date': fields.String(description='Date obtained'),
                'expiry': fields.String(description='Expiration date', required=False)
            })
        }

    def resume_upload_response(self):
        """
        Create the complete resume parse response model.

        Returns:
            Model: Flask-RESTX model for resume parse response
        """
        return self.ns.model('ResumeParseResponse', {
            'contact': fields.Nested(
                self.base_models['contact'],
                description='Contact information'
            ),
            'education': fields.List(
                fields.Nested(self.base_models['education']),
                description='Educational background'
            ),
            'experience': fields.List(
                fields.Nested(self.base_models['experience']),
                description='Work experience'
            ),
            'skills': fields.Nested(
                self.base_models['skills'],
                description='Skills categorization'
            ),
            'certifications': fields.List(
                fields.Nested(self.base_models['certifications']),
                description='Professional certifications'
            ),
            'metadata': fields.Nested(self.ns.model('Metadata', {
                'parsed_date': fields.DateTime(description='Date and time of parsing'),
                'file_name': fields.String(description='Original file name'),
                'version': fields.String(description='Parser version')
            }))
        })

    def error_response(self):
        """
        Create error response model.

        Returns:
            Model: Flask-RESTX model for error responses
        """
        return self.ns.model('ErrorResponse', {
            'error': fields.String(description='Error message'),
            'code': fields.Integer(description='Error code'),
            'details': fields.Raw(description='Additional error details')
        })