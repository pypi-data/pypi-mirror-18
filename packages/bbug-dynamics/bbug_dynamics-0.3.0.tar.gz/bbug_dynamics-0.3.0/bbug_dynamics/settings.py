import boto3
class Settings():

    def __init__(self, bbug_company_id):
        table = boto3.resource('dynamodb').Table('dynamics_settings')
        result=table.get_item( Key={ 'bbug_company_id':  bbug_company_id } )
        self.settings=result['Item']
