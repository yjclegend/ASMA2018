import datetime
import json

time = datetime.datetime.now()
print('time = ', time)
print(type(time))
jTime = json.dumps(time, default=str)
print('jTime = ', jTime)