import datetime
import json

from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

from database.database_controller import DatabaseController
from generators.script_generator import ScriptGenerator
from user_authentication.user_authenticator import UserAuthenticator

app = Flask(__name__)
CORS(app)

userAuthenticator = UserAuthenticator()


@app.route("/get_script_generators/<int:user_id>")
def get_script_generators(user_id):
    database_controller = DatabaseController()
    response = database_controller.get_script_generators(user_id=user_id)
    return response


@app.route("/get_recent_scripts/<int:script_generator_id>")
def get_recent_scripts(script_generator_id):
    database_controller = DatabaseController()
    response = database_controller.get_recent_scripts(script_generator_id=script_generator_id)
    return response


@app.route("/get_recent_script/<int:recent_script_id>")
def get_recent_script(recent_script_id):
    database_controller = DatabaseController()
    response = database_controller.get_recent_script(recent_script_id=recent_script_id)
    return response


@app.route("/get_all_script_generator_id_recent_script_id/<int:user_id>")
def get_all_script_generator_id_recent_script_id(user_id):
    database_controller = DatabaseController()
    response = database_controller.get_all_script_generator_id_recent_script_id(user_id=user_id)
    return response


@app.route("/get_all_script_generator_id/<int:user_id>")
def get_all_script_generator_id(user_id):
    database_controller = DatabaseController()
    response = database_controller.get_all_script_generator_id(user_id=user_id)
    return response


@app.route("/get_script_generator_name/<int:script_generator_id>")
def get_script_generator_name(script_generator_id):
    database_controller = DatabaseController()
    response = database_controller.get_script_generator_name(script_generator_id=script_generator_id)
    return response


@app.post('/add_new_script')
@cross_origin()
def add_new_script():
    request_data = request.get_json()
    script_generator_id = request_data['script_generator_id']
    product_name = request_data['product_name']
    keywords_desc = request_data['keywords_desc']
    script = request_data['script']
    status = request_data['status']

    utc_timestamp = datetime.datetime.now(datetime.timezone.utc)
    created_timestamp = utc_timestamp
    last_updated_timestamp = utc_timestamp

    database_controller = DatabaseController()
    result = database_controller.add_new_script(
        script_generator_id=script_generator_id,
        product_name=product_name,
        keywords_desc=keywords_desc,
        script=script,
        status=status,
        created_timestamp=created_timestamp,
        last_updated_timestamp=last_updated_timestamp)
    response = make_response(result)
    return response


@app.post('/generate_script_options')
@cross_origin()
def generate_script_options():
    request_data = request.get_json()
    script_generator_id = request_data['script_generator_id']
    product_name = request_data['product_name']
    keywords_desc = request_data['keywords_desc']

    script_generator = ScriptGenerator()
    result = script_generator.generate_script_options(script_generator_id=script_generator_id,
                                                      product_name=product_name, keywords_or_desc=keywords_desc)

    response_json = {"generated_script_options": result}
    response_json_str = json.dumps(response_json)

    response = make_response(response_json_str)
    return response


@app.post('/edit_script')
@cross_origin()
def edit_script():
    request_data = request.get_json()
    recent_script_id = request_data['recent_script_id']
    product_name = request_data['product_name']
    keywords_desc = request_data['keywords_desc']
    script = request_data['script']
    status = request_data['status']

    utc_timestamp = datetime.datetime.now(datetime.timezone.utc)
    last_updated_timestamp = utc_timestamp

    database_controller = DatabaseController()
    result = database_controller.update_recent_script(
        recent_script_id=recent_script_id,
        product_name=product_name,
        keywords_desc=keywords_desc,
        script=script,
        status=status,
        last_updated_timestamp=last_updated_timestamp)
    response = make_response(result)
    return response


@app.post('/signin')
@cross_origin()
def signin():
    request_data = request.get_json()
    ## credentials = request_data['credentials']
    email = request_data['email']
    password = request_data['password']

    result = userAuthenticator.authenticate_user_by_email(email=email, password=password)

    response = make_response(result)
    return response


@app.post('/add_script_generator')
@cross_origin()
def add_script_generator():
    request_data = request.get_json()
    user_id = request_data['user_id']
    script_generator_name = request_data['script_generator_name']
    product_names = request_data['product_names']
    keywords_descs = request_data['keywords_descs']
    scripts = request_data['scripts']

    utc_timestamp = datetime.datetime.now(datetime.timezone.utc)
    created_timestamp = utc_timestamp
    last_updated_timestamp = utc_timestamp

    database_controller = DatabaseController()
    result = database_controller.add_script_generator(
        user_id=user_id,
        script_generator_name=script_generator_name,
        product_names=product_names,
        keywords_descs=keywords_descs,
        scripts=scripts,
        created_timestamp=created_timestamp,
        last_updated_timestamp=last_updated_timestamp)
    response = make_response(result)
    return response

# @app.post('/signup')
# @cross_origin()
# def signup():
#     request_data = request.get_json()
#     credentials = request_data['credentials']
#     email = credentials['email']
#     password = credentials['password']
#
#     result = userAuthenticator.authenticate_user_by_email(email=email, password=password)
#
#     response = make_response(result)
#     return response
