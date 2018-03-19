import json
from datetime import datetime

AWS_CONFIG = json.load(open('settings.json'))

"""
" Log file name
"""
LOG_FILE = 'log.json'

"""
" Created instance name
"""
DEFAULT_NAME = 'peoplefirst-prod'

"""
" Created Autoscaling group suffix
"""
AS_SUFFIX = '-as'

now = datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute
second = now.second

"""
" Time related hash
"""
SUFFIX = "{0}{1}{2}-{3}{4}{5}".format(year, month, day, hour, minute, second)

