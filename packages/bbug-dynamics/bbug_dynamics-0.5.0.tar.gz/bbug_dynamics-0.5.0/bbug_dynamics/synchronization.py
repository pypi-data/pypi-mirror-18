import boto3
from .tasks import Tasks
class Synchronization():

    def __init__(self):
        table = boto3.resource('dynamodb').Table('dynamics_settings')
        accounts=table.scan()
        self.accounts=accounts['Items']
        self.messages=[]

    def run(self, test=False):
        for setting in self.accounts:
            if 'days_to_delete_old_data' in setting:
                setting['days_to_delete_old_data'] =int(setting['days_to_delete_old_data'])
            else:
                setting['days_to_delete_old_data'] = 5
            tasks=Tasks(setting)
            if test:
                if 'test' in setting:
                    self.print_message('Init test synchronization for: ' + setting['bbug_company_id'] )
                    self.messages+=tasks.delete_old_data()
                    self.print_message('End of the test synchronization for: ' + setting['bbug_company_id'] )
            else:
                if 'test' not in setting:
                    self.print_message('Init synchronization for: '+ setting['bbug_company_id'] )
                    self.messages+=tasks.dynamics_accounts_dump_to_bookingbug_clients()
                    self.messages+=tasks.booking_events_dump_to_dynamics_appointments()
                    self.messages+=tasks.delete_old_data()
                    self.print_message('End of synchronization for: '+ setting['bbug_company_id'] )

    def print_message(self,m):
        print m
        self.messages.append(m)
