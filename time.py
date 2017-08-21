import datetime
d = datetime.datetime.strptime('20170322.123422','%Y%m%d.%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
print d