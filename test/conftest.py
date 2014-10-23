import os

import pytest
import django


@pytest.fixture(scope='session', autouse=True)
def setup_package(request):
    os.environ['JUKEBOX_TESTING'] = 'True'

    def fin():
        test_db = os.environ.get('TEST_DB', None)
        if test_db:
            django.db.connection.creation.destroy_test_db(test_db)
    request.addfinalizer(fin)
