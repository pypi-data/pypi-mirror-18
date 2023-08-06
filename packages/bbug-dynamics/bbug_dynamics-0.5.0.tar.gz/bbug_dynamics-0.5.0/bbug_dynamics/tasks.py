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
        self.messages = ['Dynamics accounts dump to BookingBug clients started for: ' + self.bbug_company_id]
        accounts=Accounts(self.settings)
        self.messages+= accounts.get_from_dynamics()

        accounts_for_update = accounts.to_update()
        if len(accounts_for_update) > 0:
            self.print_message('There are ' + `len(accounts_for_update)` + ' to update')

            modifiedon='2010-01-01'
            bbug = Bbug(self.settings)
            for account in accounts_for_update:
                try:
                    self.messages+=bbug.save_client(account)

                    # update the account in dynamo
                    my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
                    account['bbug_updated_at']=str(my_date)
                    accounts.save(account)
                except RuntimeError as err:
                    self.print_message(err)

                if modifiedon < account['modifiedon']:
                    modifiedon=account['modifiedon']

            table_modifiedon = self.dynamodb.Table('dynamics_accounts_greater_modifiedon')
            table_modifiedon.put_item(Item={ 'bbug_company_id': self.bbug_company_id, 'modifiedon': modifiedon})
            self.print_message('Updated the last mofied on ' + modifiedon )
        else:
            self.print_message('There are no accounts to update')
        self.print_message('Dymamics accounts dump to BookingBug clients ended for: ' + self.bbug_company_id)
        return self.messages

    def booking_events_dump_to_dynamics_appointments(self):
        self.messages = ['Booking events dump to dynamics appointments started for: ' + self.bbug_company_id]
        appointments=Appointments(self.settings)
        to_update= appointments.bookings_to_update()

        if len(to_update) > 0:
            self.print_message('There are ' + `len(to_update)` + ' bookings pending to process')

            for booking_event in to_update:
                try:
                    reference = '-'
                    if 'reference' in booking_event['_embedded']['client']:
                        reference = booking_event['_embedded']['client']['reference']
                    if isinstance(reference,unicode) and len(reference)==36:
                        appointments.save_appointment_in_dynamics(booking_event)
                        self.messages+=appointments.messages
                        self.print_message('Saved in dynamics the booking event ' + str(booking_event['id']))
                    else:
                        self.print_message('The client ' + booking_event['client_name'] + ' is not a dynamics account')
                        booking_event['not_dynamic_client']=True
                        my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
                        booking_event['dynamics_updated_at']=str(my_date)
                        # update the booking event in dynamo
                        appointments.save_booking_in_dynamo(booking_event)
                    self.messages+=appointments.messages
                except RuntimeError as err:
                    self.print_message(err)

        else:
            self.print_message('There are no appointments to update')
        self.print_message('Booking events dump to dynamics appointments ended for: ' + self.bbug_company_id)
        return self.messages

    def delete_old_data(self):
        self.messages = []
        appointments_deleted=len(Appointments(self.settings).to_delete_in_dynamo(persist=True))
        accounts_deleted=len(Accounts(self.settings).to_delete_in_dynamo(persist=True))

        if appointments_deleted > 0:
            self.print_message(str(appointments_deleted) + ' old booking events registers have been deleted in: ' + self.bbug_company_id )

        if accounts_deleted > 0 :
            self.print_message(str(accounts_deleted) + ' old accounts registers have been deleted in: ' + self.bbug_company_id)

        return self.messages

    def print_message(self,m):
        print m
        self.messages.append(m)
