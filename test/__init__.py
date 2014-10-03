""" The tests module holds all unittests that we run.

To run them use tox. Just go to the project root and run the tox command.

Because some tools and modules need access to the database we have to establish a test database.
This is automatically done, when djadapter is imported and the tesing environment is initialized (env var JUKEBOX_TESTING).
The test db name will be saved in another env var ``TEST_DB``.
The test db name will be the name of the default database preceded by ``test_``.
As for now, we do not destroy the test db at the end of the test. It will be destroyed when the test runs again.
This is easier, when running multiple python instances simultaniously.
"""
import os


os.environ['JUKEBOX_TESTING'] = 'True'
