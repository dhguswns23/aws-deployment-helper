import json
from datetime import datetime

AWS_CONFIG = json.load(open('settings.json'))

LOG_FILE = 'log.json'
DEFAULT_NAME = 'peoplefirst-prod'
AS_SUFFIX = '-as'

now = datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute
second = now.second

SUFFIX = "{0}{1}{2}-{3}{4}{5}".format(year, month, day, hour, minute, second)

