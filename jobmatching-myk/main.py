from flask import Flask
from flask_restx import Api
from routes.job import api as job_namespace
from routes.authen import api as login_namespace
from routes.process_resumes import api as process_resumes_api
from routes.resume_parser import api as resume_parser_api
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

api = Api(
    title='Job Matching API',
    version='1.0',
    description='API for Job Matching Application',
    doc="/doc",
    authorizations={
        "apikey":{
            "type":"apiKey",
            "in":"header",
            "name":"token"
        }
    }
)

api.add_namespace(job_namespace, path='/jobs')
api.add_namespace(login_namespace, path='/login')
api.add_namespace(process_resumes_api, path='/process_resumes')
api.add_namespace(resume_parser_api, path='/resume_parser')

app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"]=False
api.init_app(app)

@app.route('/log')
def log_example():
    app.logger.debug('Debug message')
    app.logger.info('Info message')
    app.logger.warning('Warning message')
    app.logger.error('Error message')
    app.logger.critical('Critical message')
    return 'Logged messages!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
