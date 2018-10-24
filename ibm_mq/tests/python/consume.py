import os
import pymqi
import sys
import re

host = os.environ['HOST']
port = os.environ['PORT']
user = os.environ['USERNAME']
password = os.environ['PASSWORD']

channel = os.environ['CHANNEL']

queue_manager = os.environ['QUEUE_MANAGER']
queue_name = os.environ['QUEUE']

conn_info = "%s(%s)" % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

queue = pymqi.Queue(qmgr, queue_name)

for i in range(10):
    try:
        message = queue.get()
        print "got a new message: {}".format(message)
    except Exception as e:
        if not re.search("MQRC_NO_MSG_AVAILABLE", e.errorAsString()):
            print e
            queue.close()
            qmgr.disconnect()
            sys.exit()
        else:
            pass

queue.close()
qmgr.disconnect()
sys.exit()
