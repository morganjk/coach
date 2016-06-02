"""
wsgi file for the COACH directory service, to make it useable from Apache.
The script should be in the same directory as the Python file it imports.
"""

import os
import sys

# Activate virtual environment
activate_this = '/var/www/developmentenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.append("/var/www/COACH/COACH/framework")
sys.path.append("/var/www/COACH")

if sys.version_info[0] < 3:
    raise Exception("Python 3 required! Current Python version is %s" % sys.version_info)


from COACH.framework import coach

application = coach.DirectoryService(os.path.normpath("/var/www/COACH/COACH/development_settings.json"), 
                                     working_directory = os.path.abspath(os.curdir)).ms
