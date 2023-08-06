import os
import warnings

message = """
Some test cases might require environment variables to be set in order to work:
  TEST_SPARC_GIT_STASH_URL: https://your_server:7990
  TEST_SPARC_GIT_STASH_USER: your_username
  TEST_SPARC_GIT_STASH_PASSWD: your_password
"""
warnings.warn(message)
yaml_StashConnection = \
               {'url': os.environ.get('TEST_SPARC_GIT_STASH_URL', None),
                'username': os.environ.get('TEST_SPARC_GIT_STASH_USER', None),
                'password': os.environ.get('TEST_SPARC_GIT_STASH_PASSWD', None),
                'requests': 
                    {'verify': False}
               }
