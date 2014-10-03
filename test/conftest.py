import os

import pytest
import django


@pytest.fixture(scope='session', autouse=True)
def setup_package(request):
    os.environ['JUKEBOX_TESTING'] = 'True'

    def fin():
        old_db = os.environ.get('OLD_DB', None)
        if old_db:
            django.db.connection.creation.destroy_test_db(old_db)
    request.addfinalizer(fin)
