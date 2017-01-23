'''
Created on Dec 18, 2016

@author: devdatta
'''
import logging
import os
import subprocess

from docker import Client
from common import app
from common import service

from manager.service_handler.mysql import google_handler as gh

class GoogleBuilder(object):
    
    def __init__(self, task_def):
        self.task_def = task_def
        if task_def.app_data:
            self.app_dir = task_def.app_data['app_location']
            self.app_name = task_def.app_data['app_name']
            self.app_version = task_def.app_data['app_version']

        self.services = {}

        if task_def.service_data:
            self.service_obj = service.Service(task_def.service_data[0])
            if self.service_obj.get_service_type() == 'mysql':
                self.services['mysql'] = gh.MySQLServiceHandler(self.task_def)

        self.docker_client = Client(base_url='unix://var/run/docker.sock', version='1.18')


    def _build_first_time_container(self, app_obj):
        df_first_time_loc = self.app_dir[:self.app_dir.rfind("/")]
        
        try:
            gae_app_created = os.path.isfile(df_first_time_loc + "/app-created.txt")
        except Exception as e:
            logging.debug(e)
            
        if not gae_app_created:
            app_obj.update_app_status("BUILDING FIRST TIME APP CONTAINER")
            cwd = os.getcwd()
            app_dir = self.task_def.app_data['app_location']
            app_name = self.task_def.app_data['app_name']
            cont_name = app_name + "-app-create-cont"
            logging.debug("Container name that will be used in building:%s" % cont_name)

            os.chdir(app_dir + "/" + app_name)
            build_cmd = ("docker build -t {name} -f Dockerfile.first_time . ").format(name=cont_name)
            logging.debug("Docker build command:%s" % build_cmd)

            try:
                result = subprocess.check_output(build_cmd, shell=True)
                logging.debug(result)
            except Exception as e:
                logging.debug(e)
                logging.debug("Probably gae app was already created.")

            os.chdir(cwd)

            user_email = self.task_def.cloud_data['user_email']
            project_id = self.task_def.cloud_data['project_id']
            fp = open(df_first_time_loc + "/app-created.txt", "w")
            fp.write("%s %s %s" % (app_name, user_email, project_id))
            fp.close()

    def _build_app_container(self, app_obj):
        app_obj.update_app_status("BUILDING APP CONTAINER")
        cwd = os.getcwd()
        app_dir = self.task_def.app_data['app_location']
        app_name = self.task_def.app_data['app_name']
        os.chdir(app_dir + "/" + app_name)

        cont_name = app_obj.get_cont_name()
        logging.debug("Container name that will be used in building:%s" % cont_name)

        build_cmd = ("docker build -t {name} . ").format(name=cont_name)
        logging.debug("Docker build command:%s" % build_cmd)

        result = subprocess.check_output(build_cmd, shell=True)
        logging.debug(result)

        os.chdir(cwd)

    def build_for_delete(self, info):
        logging.debug("Google builder called for delete of app:%s" % info['app_name'])

    def build(self, build_type, build_name):
        if build_type == 'service':
            logging.debug("Google builder called for service")

            for serv in self.task_def.service_data:
                serv_handler = self.services[serv['service']['type']]
                # Invoke public interface
                serv_handler.build_instance_artifacts()
        elif build_type == 'app':
            logging.debug("Google builder called for app %s" %
                          self.task_def.app_data['app_name'])
            app_obj = app.App(self.task_def.app_data)
            self._build_app_container(app_obj)
            self._build_first_time_container(app_obj)
        else:
            logging.debug("Build type %s not supported." % build_type)
        
