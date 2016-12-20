'''
Created on Dec 19, 2016

@author: devdatta
'''
import os
import subprocess
import logging

class DockerLib(object):

    def stop_container(self, cont_name, reason_phrase):
        logging.debug("Stopping container %s. Reason: %s" % (cont_name, reason_phrase))
        stop_cmd = ("docker ps -a | grep {cont_name} | cut -d ' ' -f 1 | xargs docker stop").format(cont_name=cont_name)
        logging.debug("stop command:%s" % stop_cmd)
        os.system(stop_cmd)

    def remove_container(self, cont_name, reason_phrase):
        logging.debug("Removing container %s. Reason: %s" % (cont_name, reason_phrase))
        rm_cmd = ("docker ps -a | grep {cont_name} | cut -d ' ' -f 1 | xargs docker rm").format(cont_name=cont_name)
        logging.debug("rm command:%s" % rm_cmd)
        os.system(rm_cmd)

    def remove_container_image(self, cont_name, reason_phrase):
        logging.debug("Removing container image %s. Reason: %s" % (cont_name, reason_phrase))
        rmi_cmd = ("docker images -a | grep {cont_name}  | awk \'{{print $3}}\' | xargs docker rmi").format(cont_name=cont_name)
        logging.debug("rmi command:%s" % rmi_cmd)
        os.system(rmi_cmd)



    
    