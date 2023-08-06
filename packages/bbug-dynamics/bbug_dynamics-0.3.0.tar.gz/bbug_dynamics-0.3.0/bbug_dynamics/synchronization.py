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
            if test:
                if 'test' in setting:
                    self.messages.append('Init test synchronization for: ' + setting['bbug_company_id'] )
                    self.messages.append('End of the test synchronization for: ' + setting['bbug_company_id'] )
            else:
                if 'test' not in setting:
                    self.messages.append('Init syncronization for: '+ setting['bbug_company_id'] )
                    tasks=Tasks(setting)
                    self.messages+=tasks.dynamics_accounts_dump_to_bookingbug_clients()
                    self.messages+=tasks.booking_events_dump_to_dynamics_appointments()
                    self.messages.append('End of syncronization for: '+ setting['bbug_company_id'] )

