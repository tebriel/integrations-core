import os
import pymqi
import sys

host = os.environ['HOST']
port = os.environ['PORT']
user = os.environ['USERNAME']
password = os.environ['PASSWORD']

channel = os.environ['CHANNEL']

queue_manager = os.environ['QUEUE_MANAGER']
queue_name = os.environ['QUEUE']
conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

queue = pymqi.Queue(qmgr, queue_name)

for i in range(10):
    try:
        message = 'Hello from Python! Message {}'.format(i)
        print "sending message: {}".format(message)
        queue.put(message)
    except Exception as e:
        queue.close()
        qmgr.disconnect()
        sys.exit()

queue.close()
qmgr.disconnect()
sys.exit()
