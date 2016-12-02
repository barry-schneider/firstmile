import logging
import json
import prettytable

from cliff.command import Command

import deployment as dp


class Show(Command):
    "Show application status"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('--deploy-id',
                                 dest='deployid',
                                 help="Deployment ID/URL")
        return parser

    def take_action(self, parsed_args):
        #self.log.info('Show application info')
        #self.log.debug('Show application info')
        #self.app.stdout.write('Show app info\n')
        #self.app.stdout.write("Passed args:%s" % parsed_args)
        
        if parsed_args.deployid:
            result = dp.Deployment().get(parsed_args.deployid)
            
            status_json = json.loads(result)
            status_val = status_json['app_data']
            
            status_val_list = status_val.split(',')

            x = prettytable.PrettyTable()
            x.field_names = ["App Name", "Deploy ID", "Status", "App URL"]

            app_name = ''
            app_deploy_id = ''
            app_deploy_time = ''
            app_status = ''
            app_url = ''
            for stat in status_val_list:
                stat = stat.rstrip().lstrip()
                if stat.lower().find("name") >= 0:
                    l = stat.split("::")
                    app_name = l[1]
                elif stat.lower().find("deploy_id") >= 0:
                    l = stat.split("::")
                    app_deploy_id = l[1]
                elif stat.lower().find("status") >= 0:
                    l = stat.split("::")
                    app_status = l[1]
                elif stat.lower().find("url") >= 0:
                    l = stat.split("::")
                    app_url = l[1]

            row = [app_name, app_deploy_id, app_status, app_url]
            x.add_row(row)
            self.app.stdout.write("%s\n" % x)