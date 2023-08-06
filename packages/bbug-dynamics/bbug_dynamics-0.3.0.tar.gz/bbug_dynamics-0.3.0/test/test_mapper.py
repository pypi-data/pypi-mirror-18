# -*- coding: utf-8 -*-
from bbug_dynamics import Mapper

def test_parse():
    entities_map={
            'subject': '_embedded.bookings.__first.full_describe',
            'scheduleddurationminutes': '_embedded.bookings.__first.duration',
            'category': '_embedded.bookings.__first.category_name',
            'scheduledstart': '_embedded.bookings.__first.datetime',
            'scheduledend': '_embedded.bookings.__first.end_datetime',
            'location': '_embedded.bookings.__first.address.map_marker',
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
                },
                {
                    'method': 'replace_substring',
                    'field': 'location',
                    'value': '_embedded.bookings.__first.address.map_marker',
                    'search': '+',
                    'replace_by': ' '
                }
            ]

        }

    source_entity={
        '_embedded':
             { 'bookings':
              [
                  {
                      'full_describe': '£1 Lesson with Sven Benedict - Court 2',
                      'duration': 60,
                      'category_name': 'Private Lessons',
                      'datetime': '2016-07-22T20:00:00-04:00',
                      'end_datetime': '2016-07-22T21:00:00-04:00',
                      'address': { 'map_marker': 'A+sport+Centre,+123+A+Road,+Some+Town,+sw17+9jy,+United+Kingdom' }
                  }

              ],
              'client': { 'reference': 'b0a19cdd-88df-e311-b8e5-6c3be5a8b200' }
             }
            }


    mapper= Mapper(source_entity, entities_map)
    mapper.parse()
    assert mapper.target_entity['subject'] == source_entity['_embedded']['bookings'][0]['full_describe']
    assert mapper.target_entity['scheduleddurationminutes'] == source_entity['_embedded']['bookings'][0]['duration']
    assert mapper.target_entity['category'] == source_entity['_embedded']['bookings'][0]['category_name']
    assert mapper.target_entity['scheduledstart'] == source_entity['_embedded']['bookings'][0]['datetime']
    assert mapper.target_entity['scheduledend'] == source_entity['_embedded']['bookings'][0]['end_datetime']
    assert mapper.target_entity['location'] == 'A sport Centre, 123 A Road, Some Town, sw17 9jy, United Kingdom'
    assert mapper.target_entity['partyid_account@odata.bind']== '/accounts(' + source_entity['_embedded']['client']['reference'] + ')'
    assert mapper.target_entity['participationtypemask']== 5
