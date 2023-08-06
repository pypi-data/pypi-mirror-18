import boto3
class Settings():

    def __init__(self, bbug_company_id):
        self.table = boto3.resource('dynamodb').Table('dynamics_settings')
        result=self.table.get_item( Key={ 'bbug_company_id':  bbug_company_id } )
        self.settings=result['Item']

        if 'days_to_delete_old_data' in self.settings :
            self.settings['days_to_delete_old_data']=int(self.settings['days_to_delete_old_data'])
        else:
            self.settings['days_to_delete_old_data']= 5

    def save(self):
        self.table.put_item(Item=self.settings)
