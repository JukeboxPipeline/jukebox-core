""" This is a test environment file. It should only set os.environ['testenvvar'] to 'foo'.
The testenvvar will be checked in a unittest to see, if this file was loaded correctly. """

import os
os.environ['testenvvar'] = 'foo'
