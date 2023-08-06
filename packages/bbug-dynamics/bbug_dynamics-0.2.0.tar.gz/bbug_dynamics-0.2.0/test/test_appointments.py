from bbug_dynamics import Settings, Appointments

def init_appointments(bbug_company_id = 'uk__21'):
    settings= Settings(bbug_company_id).settings
    return Appointments(settings)

def test_all_appointments_status():
    appointments = init_appointments()
    appointments.query()
    assert appointments.response.status == 200

def test_appointments_data():
    appointments = init_appointments()
    appointments.query()
    assert len(appointments.process_response()) > 1

def test_appointments_query():
    appointments = init_appointments()
    appointments.query(params={ '$filter': "subject eq 'Bookingbug test'", '$top': '1' })
    assert len(appointments.process_response()) == 1

def test_find_appointment():
    appointments = init_appointments()
    appointments.query(params={'$top': '1'})
    data = appointments.process_response()
    assert len(data) == 1
    assert 'activityid' in data[0]
    appointments.find_dynamics_object(data[0]['activityid'])
    appointment = appointments.process_response()
    assert data[0]['activityid']== appointment['activityid']

def test_not_found_appointment():
    appointments = init_appointments()
    appointments.find_dynamics_object('fakeid')

    data = appointments.process_response()
    assert data['error'] == 'Cannot get the Appointments object(s) from dynamics'

def test_get_bookings_from_dynamo():
    appointments = init_appointments()
    bookings=appointments.get_bookings_from_dynamo(limit=1)
    assert bookings[0]['id']>1
    booking= appointments.get_booking_from_dymamo(bookings[0]['id'])
    assert booking['id']==bookings[0]['id']
    booking= appointments.get_booking_from_dymamo('12344')
    assert 'error' in booking


def test_save_appointment_in_dynamics():
# copy one booking event to localhost__37000
    appointments = init_appointments()
    bookings=appointments.get_bookings_from_dynamo(limit=1)
    booking=bookings[0]
    booking['bbug_company_id']='localhost__37000'
    del booking['dynamics_updated_at']
    appointments = init_appointments('localhost__37000')
    appointments.save_booking_in_dynamo(booking)
    new_booking=appointments.get_booking_from_dymamo(booking['id'])
    assert new_booking['id']==booking['id']
    assert new_booking['bbug_company_id']=='localhost__37000'
    appointments.save_appointment_in_dynamics(booking)
    assert len(filter((lambda x: x.startswith('Created appointment for booking')),appointments.messages))> 0
    appointments.save_appointment_in_dynamics(booking)
    assert len(filter((lambda x: x.startswith('Updated appointment')),appointments.messages))> 0
# delete the test appointment in dynamics
    appointments.delete_appointment_in_dynamics(booking)
    assert appointments.response.status==204


