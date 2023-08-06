from bbug_dynamics import Synchronization, Settings
from utils import copy_data_backup

def test_synchronization_accounts():
    sync= Synchronization()
    assert len(sync.accounts)>1

def test_synchronization_test_mode():
    # to exclude testbackup for the delete_old_data in sync
    settings = Settings('testbackup')
    if 'test' in settings.settings:
        del settings.settings['test']
        settings.save()

    copy_data_backup('testbackup','test')
    sync = Synchronization()
    sync.run(test=True)

    assert 'Init test synchronization for: localhost__37000' in sync.messages
    assert 'End of the test synchronization for: localhost__37000' in sync.messages
    assert 'Init test synchronization for: test' in sync.messages
    assert 'End of the test synchronization for: test' in sync.messages
    assert 'Init test synchronization for: uk__21' not in sync.messages
    assert 'End of the test synchronization for: uk__21' not in sync.messages
    assert 'Init synchronization for: uk__21' not in sync.messages
    assert 'End of synchronization for: uk__21' not in sync.messages
    assert 'Init synchronization for: localhost__37000' not in sync.messages
    assert 'End of synchronization for: localhost__37000' not in sync.messages
    assert 'Init synchronization for: test' not in sync.messages
    assert 'End of synchronization for: test' not in sync.messages
    assert len(filter((lambda x: 'old booking events registers have been deleted in: test' in x),sync.messages))> 0
    assert len(filter((lambda x: 'old accounts registers have been deleted in: test' in x),sync.messages))> 0

    settings.settings['test']=True
    settings.save()

def test_synchronization_prod_mode():
    sync = Synchronization()
    sync.run()
    assert 'Init test synchronization for: localhost__37000' not in sync.messages
    assert 'End of the test synchronization for: localhost__37000' not in sync.messages
    assert 'Init test synchronization for: test' not in sync.messages
    assert 'End of the test synchronization for: test' not in sync.messages
    assert 'Init test synchronization for: uk__21' not in sync.messages
    assert 'End of the test synchronization for: uk__21' not in sync.messages
    assert 'Init synchronization for: uk__21' in sync.messages
    assert 'End of synchronization for: uk__21' in sync.messages
    assert 'Init synchronization for: localhost__37000' not in sync.messages
    assert 'End of synchronization for: localhost__37000' not in sync.messages
    assert 'Init synchronization for: test' not in sync.messages
    assert 'End of synchronization for: test' not in sync.messages
    assert 'Dynamics accounts dump to BookingBug clients started for: uk__21' in sync.messages
    assert 'Dymamics accounts dump to BookingBug clients ended for: uk__21' in sync.messages
    assert 'Booking events dump to dynamics appointments started for: uk__21' in sync.messages
    assert 'Booking events dump to dynamics appointments ended for: uk__21' in sync.messages
