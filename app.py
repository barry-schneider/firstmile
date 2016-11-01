import os
import tarfile
import datetime
import time

from os.path import expanduser

from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Resource, Api


from manager import manager as mgr
from common import task_definition

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('app_content', location='form')
parser.add_argument('app_name', location='form')

home_dir = expanduser("~")

APP_STORE_PATH = ("{home_dir}/.lme/data/deployments").format(home_dir=home_dir)


class Deployment(Resource):
    def get(self, dep_id):
        print("Dep id:%s" % dep_id)

        def _get_app_location(dep_id):
            k = dep_id.rfind("--")
            app_version = dep_id[k+2:]
            print("App version:%s" % app_version)

            dep_id = dep_id[:k]
            l = dep_id.rfind("/")
            app_name = dep_id[l+1:]
            print("App name:%s" % app_name)
            return APP_STORE_PATH + "/" + app_name + "/" + app_version

        app_location = _get_app_location(dep_id)
        print("App location:%s" % app_location)

        app_status_file = open(app_location + "/app-status.txt", "r")
        app_status_data = app_status_file.read()
        print("--- App status ---")
        print(app_status_data)
        print("--- App status ---")
        
        resp_data = {}
        resp_data['app_data'] = app_status_data

        response = jsonify(**resp_data)
        response.status_code = 201
        return response

class Deployments(Resource):
    def _untar_the_app(self, app_tar_file, versioned_app_path):
        #TODO(devkulkarni): Untaring is not working
        #os.chdir(versioned_app_path)
        #tar = tarfile.open(app_tar_name)
        #for member in tar.getmembers():
        #    tar.extractfile(member)
        #tar.close()

        untar_cmd = ("tar -xvf {app_tar_file} -C {versioned_app_path}").format(app_tar_file=app_tar_file,
                                                                               versioned_app_path=versioned_app_path)
        os.system(untar_cmd)

    def _store_app_contents(self, app_name, app_tar_name, content):
        # create directory
        app_path = ("{APP_STORE_PATH}/{app_name}").format(APP_STORE_PATH=APP_STORE_PATH, app_name=app_name)
        if not os.path.exists(app_path):
            os.makedirs(app_path)

        ts = time.time()
        app_version = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

        versioned_app_path = ("{app_path}/{st}").format(app_path=app_path, st=app_version)
        os.makedirs(versioned_app_path)

        # store file content
        app_tar_file = ("{versioned_app_path}/{app_tar_name}").format(versioned_app_path=versioned_app_path, 
                                                                      app_tar_name=app_tar_name)
        app_file = open(app_tar_file, "w")
        app_file.write(content.encode("ISO-8859-1"))

        # expand the directory
        self._untar_the_app(app_tar_file, versioned_app_path)
        return versioned_app_path, app_version
    
    def post(self):
        #args = parser.parse_args()
        args = request.get_json(force=True)
        
        app_data = args['app']
        cloud_data = args['cloud']
        service_data = args['service']
        
        app_name = app_data['app_name']
        app_tar_name = app_data['app_tar_name']
        content = app_data['app_content']
        cloud = cloud_data['cloud']

        app_location, app_version = self._store_app_contents(app_name, app_tar_name, content)
        
        # dispatch the handler thread
        #task_dict = {}
        #task_dict['app_name'] = app_name
        #task_dict['app_location'] = app_location
        #task_dict['cloud'] = cloud
        app_data['app_location'] = app_location
        task_def = task_definition.TaskDefinition(app_data, cloud_data, service_data)
        delegatethread = mgr.Manager(app_name, task_def)
        delegatethread.start()        

        response = jsonify()
        response.status_code = 201
        app_id = ("{app_name}--{app_version}").format(app_name=app_name, app_version=app_version)
        print("App id:%s" % app_id)
        response.headers['location'] = ('/deployments/{app_id}').format(app_id=app_id)
        print("Response:%s" % response)

        return response


api.add_resource(Deployment, '/deployments/<dep_id>')
api.add_resource(Deployments, '/deployments')

if __name__ == '__main__':
    # Create the data directory if it does not exist
    if not os.path.exists(APP_STORE_PATH):
        os.makedirs(APP_STORE_PATH)
    app.run(debug=True)