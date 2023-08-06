from .settings import Settings
from .accounts import Accounts
from .appointments import Appointments
from .bbug import Bbug
from boto3.dynamodb.conditions import Key, Attr
import boto3, datetime, pytz

class Tasks():
    def __init__(self,settings):
        self.bbug_company_id=settings['bbug_company_id']
        self.settings = settings
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    def dynamics_accounts_dump_to_bookingbug_clients(self):
        messages = ['Dynamics accounts dump to bookingbug clients started for: ' + self.bbug_company_id]
        accounts=Accounts(self.settings)
        messages+= accounts.get_from_dynamics()

        accounts_for_update = accounts.to_update()
        if len(accounts_for_update) > 0:
            messages.append('There are ' + `len(accounts_for_update)` + ' to update')

            modifiedon='2010-01-01'
            bbug = Bbug(self.settings)
            for account in accounts_for_update:
                try:
                    messages+=bbug.save_client(account)

                    # update the account in dynamo
                    my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
                    account['bbug_updated_at']=str(my_date)
                    accounts.save(account)
                except RuntimeError as err:
                    messages.append(err)

                if modifiedon < account['modifiedon']:
                    modifiedon=account['modifiedon']

            table_modifiedon = self.dynamodb.Table('dynamics_accounts_greather_modifiedon')
            table_modifiedon.put_item(Item={ 'bbug_company_id': self.bbug_company_id, 'modifiedon': modifiedon})
            messages.append('Updated the last mofied on ' + modifiedon )
        else:
            messages.append('There are no accounts to update')
        messages.append('Dymamics accounts dump to bookinbug clients ended for: ' + self.bbug_company_id)
        return messages

    def booking_events_dump_to_dynamics_appointments(self):
        messages = ['Booking events dump to dynamics appointments started for: ' + self.bbug_company_id]
        appointments=Appointments(self.settings)
        to_update= appointments.bookings_to_update()

        if len(to_update) > 0:
            messages.append('There are ' + `len(to_update)` + ' bookings pending to process')

            for booking_event in to_update:
                try:
                    reference = '-'
                    if 'reference' in booking_event['_embedded']['client']:
                        reference = booking_event['_embedded']['client']['reference']
                    if isinstance(reference,unicode) and len(reference)==36:
                        appointments.save_appointment_in_dynamics(booking_event)
                        messages+=appointments.messages
                        messages.append('Saved in dynamics the booking event ' + str(booking_event['id']))
                    else:
                        messages.append('The client ' + booking_event['client_name'] + ' is not a dynamics account')
                        booking_event['not_dynamic_client']=True
                        my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
                        booking_event['dynamics_updated_at']=str(my_date)
                        # update the booking event in dynamo
                        appointments.save_booking_in_dynamo(booking_event)
                    messages+=appointments.messages
                except RuntimeError as err:
                    messages.append(err)

        else:
            messages.append('There are no appointments to update')
        messages.append('Booking events dump to dynamics appointments ended for: ' + self.bbug_company_id)
        return messages

