'''
 Copyright (C) Devcentric, Inc - All Rights Reserved
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Devdatta Kulkarni <devdattakulkarni@gmail.com> January 3 2017
'''

from os.path import expanduser

DEFAULT_DB_USER = 'testuser'
DEFAULT_DB_PASSWORD = 'testpass123!#$'
DEFAULT_DB_NAME = 'testdb'
DEFAULT_APP_PORT = '80'

UBUNTU_IMAGE_NAME = 'ubuntu'
MYSQL_IMAGE_NAME = 'mysql'

DEPLOY_LOG = ".deploy-log"
RUNTIME_LOG = ".runtime-log"

home_dir = expanduser("~")

APP_STORE_PATH = ("{home_dir}/.cld/data/deployments").format(home_dir=home_dir)
SERVICE_STORE_PATH = APP_STORE_PATH + "/services"

GOOGLE_CREDS_PATH = APP_STORE_PATH + "/google-creds"

LOG_FILE_NAME = "cld.log"

SETTING_UP_APP = "SETTING_UP_APP"
BUILDING_APP = "BUILDING_APP"

DEPLOYING_APP = "DEPLOYING_APP"
APP_DEPLOYMENT_COMPLETE = "APP_DEPLOYMENT_COMPLETE"
DEPLOYMENT_ERROR = "DEPLOYMENT_ERROR"

DEPLOYING_SERVICE_INSTANCE = "DEPLOYING_SERVICE_INSTANCE"
SERVICE_INSTANCE_DEPLOYMENT_COMPLETE = "SERVICE_DEPLOYMENT_COMPLETE"

DELETING = "DELETING"

DB_USER = "USER"
DB_USER_PASSWORD = "PASSWORD"
DB_ROOT_PASSWORD = "ROOT_PASSWORD"
DB_HOST = "HOST"
DB_NAME = "DB_NAME"

RDS_INSTANCE = "RDS_INSTANCE"

CLOUD_SQL_CONNECTION_STR = "CONNECTION_STR"
MYSQL_VERSION = "MYSQL_VERSION"
CLOUD_SQL_TIER = "CLOUD_SQL_TIER"
CLOUD_SQL_INSTANCE = "CLOUD_SQL_INSTANCE"

SQL_CONTAINER = "SQL_CONTAINER"

LOCAL_DOCKER = "local-docker"
GOOGLE = "google"
AWS = "aws"

GOOGLE_APP_CREATE_CONT_SUF = "app-create-cont"
RETRIEVE_LOG_PATH = "./retrieve-logs.sh"
