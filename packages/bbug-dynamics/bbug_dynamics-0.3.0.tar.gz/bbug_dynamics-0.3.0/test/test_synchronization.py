from bbug_dynamics import Synchronization

def test_synchronization_accounts():
    sync= Synchronization()
    assert len(sync.accounts)>1

def test_synchronization_test_mode():
    sync = Synchronization()
    sync.run(test=True)
    assert 'Init test synchronization for: localhost__37000' in sync.messages
    assert 'End of the test synchronization for: localhost__37000' in sync.messages
    assert 'Init test synchronization for: test' in sync.messages
    assert 'End of the test synchronization for: test' in sync.messages
    assert 'Init test synchronization for: uk__21' not in sync.messages
    assert 'End of the test synchronization for: uk__21' not in sync.messages
    assert 'Init syncronization for: uk__21' not in sync.messages
    assert 'End of syncronization for: uk__21' not in sync.messages
    assert 'Init syncronization for: localhost__37000' not in sync.messages
    assert 'End of syncronization for: localhost__37000' not in sync.messages
    assert 'Init syncronization for: test' not in sync.messages
    assert 'End of syncronization for: test' not in sync.messages

def test_synchronization_prod_mode():
    sync = Synchronization()
    sync.run()
    assert 'Init test synchronization for: localhost__37000' not in sync.messages
    assert 'End of the test synchronization for: localhost__37000' not in sync.messages
    assert 'Init test synchronization for: test' not in sync.messages
    assert 'End of the test synchronization for: test' not in sync.messages
    assert 'Init test synchronization for: uk__21' not in sync.messages
    assert 'End of the test synchronization for: uk__21' not in sync.messages
    assert 'Init syncronization for: uk__21' in sync.messages
    assert 'End of syncronization for: uk__21' in sync.messages
    assert 'Init syncronization for: localhost__37000' not in sync.messages
    assert 'End of syncronization for: localhost__37000' not in sync.messages
    assert 'Init syncronization for: test' not in sync.messages
    assert 'End of syncronization for: test' not in sync.messages
    assert 'Dynamics accounts dump to bookingbug clients started for: uk__21' in sync.messages
    assert 'Dymamics accounts dump to bookinbug clients ended for: uk__21' in sync.messages
    assert 'Booking events dump to dynamics appointments started for: uk__21' in sync.messages
    assert 'Booking events dump to dynamics appointments ended for: uk__21' in sync.messages
