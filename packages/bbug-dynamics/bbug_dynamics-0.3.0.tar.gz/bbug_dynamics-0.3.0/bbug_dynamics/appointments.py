import json, datetime, pytz
from .dynamics import Dynamics
from .bbug import Bbug
from .mapper import Mapper
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

class Appointments(Dynamics):

    def __init__(self,settings):
        Dynamics.__init__(self,settings)
        self.table=self.dynamodb.Table('dynamics_bookingbug_events')

        self.booking_to_appointment_map={
            'subject': '_embedded.bookings.__first.full_describe',
            'scheduleddurationminutes': '_embedded.bookings.__first.duration',
            'category': '_embedded.bookings.__first.category_name',
            'scheduledstart': '_embedded.bookings.__first.datetime',
            'scheduledend': '_embedded.bookings.__first.end_datetime',
            '__methods': [
                {
                    'method': 'replace_substring',
                    'field': 'location',
                    'value': '_embedded.bookings.__first.address.map_marker',
                    'search': '+',
                    'replace_by': ' '
                }
            ]
        }
        self.booking_to_activity_party_map={
            '__methods': [
                {
                    'method': 'set_navigation_property',
                    'field': 'partyid_account@odata.bind',
                    'value': '_embedded.client.reference',
                    'uri': '/accounts'
                },
                {
                    'method': 'set_value',
                    'field': 'participationtypemask',
                    'value': 5
                }
            ]

        }



    def base_uri(self):
        return '/appointments'

    def save_booking_in_dynamo(self,bbug_event):
        self.table.put_item(Item=bbug_event)
        self.messages.append("Bookingbug Event " + str(bbug_event['id']) + " was saved in dynamodb.")

    def get_booking_from_dymamo(self, booking_id):
        try:
            booking= self.table.get_item(Key={'bbug_company_id': self.bbug_company_id, 'id': booking_id})
            return booking['Item']
        except Exception as e:
            return { 'error': 'cannot get the booking with id ' + str(booking_id) }

    def get_messages(self):
        """Get messages and clean the messages instance variable
        """
        messages = self.messages
        self.messages=[]
        return messages

    def get_bookings_from_dynamo(self, limit = 100 ):
        response=self.table.query( KeyConditionExpression= Key('bbug_company_id').eq( self.bbug_company_id), Limit=limit)
        return response['Items']

    def bookings_to_update(self):
        response=self.table.query( KeyConditionExpression= Key('bbug_company_id').eq( self.bbug_company_id),
                                  FilterExpression='attribute_not_exists(dynamics_updated_at)')
        return response['Items']

    def save_appointment_in_dynamics(self, booking):
        self.messages=[]
        self.booking_id = booking['id']
        mapper=Mapper(booking,self.booking_to_appointment_map)
        mapper.parse()
        appointment = mapper.target_entity
        mapper=Mapper(booking,self.booking_to_activity_party_map)
        mapper.parse()
        activity_party= mapper.target_entity
        appointment['appointment_activity_parties']=[activity_party]

        booking_appointment = self.get_booking_appointment()
        if booking_appointment:
            self.udate_appointment_in_dynamics(appointment,booking_appointment,booking)
        else:
            self.create_appointment_in_dynamics(appointment,booking)


    def get_booking_appointment(self):
        table=self.dynamodb.Table('dynamics_booking_appointments')
        booking_appointment=table.get_item( Key={'id': self.bbug_company_id + '__' + str(self.booking_id) } )
        if 'Item' in booking_appointment:
            return booking_appointment['Item']
        else:
            return None

    def udate_appointment_in_dynamics(self,appointment,booking_appointment,booking):
        self.query(path="("+booking_appointment['activityid']+")",body=json.dumps(appointment),http_method='PATCH')
        if self.response.status==204:
            my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
            booking['dynamics_updated_at']=str(my_date)
            self.save_booking_in_dynamo(booking)
            table=self.dynamodb.Table('dynamics_booking_appointments')
            booking_appointment['dynamics_updated_at']+=", " + str(my_date)
            table.put_item(Item=booking_appointment)
            self.messages.append("Updated appointment " + booking_appointment['activityid'] + " for booking " + booking_appointment['id'])
        else:
            self.messages.append("Error cannot update the appointment "+booking_appointment['activityid'] +" for booking: " + str(booking['id']))
            self.messages.append("Response status: " + str(self.response.status))
            self.messages.append("Response : " + self.response.read())
    def create_appointment_in_dynamics(self,appointment,booking):
        self.query(body=json.dumps(appointment),http_method='POST')
        if self.response.status==204:
            obid= self.response.getheader('odata-entityid')
            obid= obid[obid.find("(") + 1 : obid.find(")") ]
            my_date = datetime.datetime.now(pytz.timezone('Europe/London'))
            booking['dynamics_updated_at']=str(my_date)
            table=self.dynamodb.Table('dynamics_booking_appointments')
            table.put_item(Item={'id': self.bbug_company_id + '__' + str(self.booking_id), 'activityid': obid, 'dynamics_updated_at': str(my_date) })
            self.save_booking_in_dynamo(booking)
            self.messages.append("Created appointment for booking " + str(booking['id']))
        else:
            self.messages.append("Error cannot create an appointment for booking: " + str(booking['id']))
            self.messages.append("Response status: " + str(self.response.status))
            self.messages.append("Response : " + self.response.read())

    def delete_appointment_in_dynamics(self, booking):
        self.booking_id = booking['id']
        booking_appointment = self.get_booking_appointment()
        if booking_appointment:
            activityid = booking_appointment['activityid']
            self.query(path="("+  activityid + ")", http_method='DELETE')
            if self.response.status==204:
                table=self.dynamodb.Table('dynamics_booking_appointments')
                booking_appointment=table.delete_item( Key={'id': self.bbug_company_id + '__' + str(self.booking_id) } )
                self.messages.append("Deleted appointment " + activityid )
            else:
                self.messages.append("Error, cannot delete the appointment " + booking_appointment['activityid'] )
        else:
            self.messages.append("Error, the acitvityid not found")
