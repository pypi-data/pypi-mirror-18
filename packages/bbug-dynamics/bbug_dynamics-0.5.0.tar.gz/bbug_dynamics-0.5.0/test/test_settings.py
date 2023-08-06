from bbug_dynamics import Settings

def test_save():
    settings = Settings('testbackup')
    settings.settings['test']= True
    settings.save()
    assert 'test' in settings.settings
    del settings.settings['test']
    assert 'test' not in settings.settings
    settings.save()

    settings = Settings('testbackup')
    assert 'test' not in settings.settings
    settings.settings['test']= True
    settings.save()

    settings = Settings('testbackup')
    assert 'test' in settings.settings
