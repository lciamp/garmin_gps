from datetime import datetime
s1 = '10:33:26'
s2 = '11:15:49' # for example
FMT = '%H:%M:%S'
tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

x = '2018-05-19T11:08:14.000Z'
x = x[:-1]
print(datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.000'))

strftime("%Y-%m-%dT%H:%M:%S", gmtime())


x = myFile.start_time
x = x[11:-5]
y = myFile.end_time
y = y[11:-5]
tdelta = datetime.strptime(y, FMT) - datetime.strptime(x, FMT)

print('total time delta: {}'.format(tdelta))