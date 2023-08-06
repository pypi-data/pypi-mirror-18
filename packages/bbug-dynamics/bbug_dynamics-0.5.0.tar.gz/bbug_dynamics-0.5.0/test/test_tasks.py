from bbug_dynamics import Settings,Tasks, Accounts, Bbug, Appointments
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import copy_data_backup

def test_dynamics_accounts_dump_to_bookingbug_clients():
    settings = Settings('uk__21').settings
    tasks = Tasks(settings)
    messages = tasks.dynamics_accounts_dump_to_bookingbug_clients()
    assert 'Dynamics accounts dump to BookingBug clients started for: uk__21' == messages[0]
    assert 'Dymamics accounts dump to BookingBug clients ended for: uk__21' == messages[-1]

    accounts=Accounts(settings)
    dynamo_accounts=accounts.get_from_dynamo()
    print "Accounts in Dynamo:" + str(len(dynamo_accounts))
    for m in messages:
        print m
    bbug = Bbug(settings)
    for account in dynamo_accounts:
        bbug.get_client(account['accountid'])
        assert bbug.response.status_code == 200

def test_after_dynamics_accounts_dump_to_bookingbug_clients():
    settings = Settings('uk__21').settings
    tasks = Tasks(settings)
    messages = tasks.dynamics_accounts_dump_to_bookingbug_clients()

    # sync without accounts to update
    for m in messages:
        print m
    assert 'There are no accounts to update' in messages

    accounts=Accounts(settings)
    dynamo_accounts=accounts.get_from_dynamo(limit=1)
    account=dynamo_accounts[0]
    del account['bbug_updated_at']
    accounts.save(account)

    # sync with accounts to update
    messages = tasks.dynamics_accounts_dump_to_bookingbug_clients()
    for m in messages:
        print m
    assert 'There are no accounts to update' not in messages

def test_booking_events_dump_to_dynamics_appointments():
# copy one booking event in localhost__37000 test account
    appointments = Appointments(Settings('uk__21').settings)
    bookings=appointments.get_bookings_from_dynamo(limit=1)
    booking=bookings[0]
    del booking['dynamics_updated_at']
    booking['bbug_company_id']='localhost__37000'
    settings= Settings('localhost__37000').settings
    local_appointments = Appointments(settings)
    local_appointments.save_booking_in_dynamo(booking)
# init the syncro for localhost__37000
    tasks= Tasks(settings)
    messages = tasks.booking_events_dump_to_dynamics_appointments()
    assert len(messages)>0
    assert 'Booking events dump to dynamics appointments started for: localhost__37000' in messages
    assert 'There are 1 bookings pending to process' in messages
    assert len(filter((lambda x: x.startswith('Saved in dynamics the booking event')),messages))> 0
    assert 'Booking events dump to dynamics appointments ended for: localhost__37000' in messages
# delete the test appointment in dynamics
    local_appointments.delete_appointment_in_dynamics(booking)
    assert local_appointments.response.status==204
    messages = tasks.booking_events_dump_to_dynamics_appointments()
    assert 'There are 1 bookings pending to process' not in messages

def test_booking_events_dump_to_dynamics_appointments_no_dynamics():
# copy one booking event in localhost__37000 test account
    appointments = Appointments(Settings('uk__21').settings)
    bookings=appointments.get_bookings_from_dynamo(limit=1)
    booking=bookings[0]
    del booking['dynamics_updated_at']
    del booking['_embedded']['client']['reference']
    booking['bbug_company_id']='localhost__37000'
    settings= Settings('localhost__37000').settings
    local_appointments = Appointments(settings)
    local_appointments.save_booking_in_dynamo(booking)
# init the syncro for localhost__37000
    tasks= Tasks(settings)
    messages = tasks.booking_events_dump_to_dynamics_appointments()
    assert len(messages)>0
    assert 'Booking events dump to dynamics appointments started for: localhost__37000' in messages
    assert 'There are 1 bookings pending to process' in messages
    assert len(filter((lambda x: x.startswith('Saved in dynamics the booking event')),messages))== 0
    assert 'Booking events dump to dynamics appointments ended for: localhost__37000' in messages
    assert 'The client ' + booking['client_name'] + ' is not a dynamics account' in messages
    messages = tasks.booking_events_dump_to_dynamics_appointments()
    assert 'There are 1 bookings pending to process' not in messages

def test_to_delete_in_dynamo():
    copy_data_backup('testbackup','test')
    date_after_month = datetime.today() - relativedelta(months=1)
    settings=Settings('test').settings
# set 2 accounts and 2 appointment updated date 1 month ago
    settings['days_to_delete_old_data']=10
    appointments = Appointments(settings)
    accounts=Accounts(settings)
    bookings=appointments.get_bookings_from_dynamo(limit=4)
    clients=accounts.get_from_dynamo(limit=4)

    for x in range(0,2):
        bookings[x]['dynamics_updated_at']=str(date_after_month.strftime('%Y-%m-%-d'))
        clients[x]['bbug_updated_at']=str(date_after_month.strftime('%Y-%m-%-d'))
    for x in range(2,4):
        bookings[x]['dynamics_updated_at']=str(datetime.today().strftime('%Y-%m-%-d'))
        clients[x]['bbug_updated_at']=str(datetime.today().strftime('%Y-%m-%-d'))

    for x in range(0,4):
        appointments.save_booking_in_dynamo(bookings[x])
        accounts.save(clients[x])

    settings['days_to_delete_old_data']=100
    appointments2 = Appointments(settings)
    accounts2 = Accounts(settings)
    assert len(appointments.to_delete_in_dynamo()) > len(appointments2.to_delete_in_dynamo())
    assert len(accounts.to_delete_in_dynamo()) > len(accounts2.to_delete_in_dynamo())


def test_delete_old_data():
    copy_data_backup('testbackup','test')
    settings = Settings('test').settings
    backup_settings = Settings('testbackup').settings
    tasks = Tasks(settings)
    accounts = Accounts(settings)
    appointments = Appointments(settings)

    total_accounts_before_delete= len(accounts.get_from_dynamo())
    print "Accounts before delete " + str(total_accounts_before_delete)

    total_appointments_before_delete = len(appointments.get_bookings_from_dynamo())
    print "Appointments bebore delete " + str(total_appointments_before_delete)

    messages=tasks.delete_old_data()

    total_accounts_after_delete= len(accounts.get_from_dynamo())
    print "Accounts after delete " + str(total_accounts_after_delete)

    total_appointments_after_delete = len(appointments.get_bookings_from_dynamo())
    print "Appointments bebore delete " + str(total_appointments_after_delete)

    assert total_appointments_after_delete < total_appointments_before_delete
    assert total_accounts_after_delete < total_accounts_before_delete

    print "Messages: "
    print messages
    assert len(filter((lambda x: 'old booking events registers have been deleted' in x),messages))> 0
    assert len(filter((lambda x: 'old accounts registers have been deleted' in x),messages))> 0
    assert len(Appointments(settings).get_bookings_from_dynamo()) < len(Appointments(backup_settings).get_bookings_from_dynamo())
    assert len(Accounts(settings).get_from_dynamo()) < len(Accounts(backup_settings).get_from_dynamo())

    copy_data_backup('testbackup','test')
