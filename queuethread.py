# System modules
from Queue import Queue
from threading import Thread
import time
import logging
import pymssql


# Set up some global variables
num_fetch_threads = 2
q = Queue()
conn = pymssql.connect(server='172.16.2.1', user='undanet', password='undanet2015', port=1433, database='neuman')
query = 'select sp.id, sp.alias, sp.cronCommand, sp.description from neuman.dbo.stock_platform sp join neum an.dbo.platform p on p.id = sp.platform_id where sp.active = 1 and sp.is_webservice = 0 and p.active = 1'
cursor = conn.cursor()

def Enclosures(i, q):
    #These daemon threads go into an infinite loop, and only exit when the main thread ends.
    while True:
        print '%s: Looking for the next enclosure' % i
        q.get()
        print '%s: Executing' % i
        time.sleep(i + 2)
        q.task_done()


# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = Thread(target=Enclosures, args=(i, q,))
    worker.setDaemon(True)
    worker.start()

# Putting the commands into the queue
    for i in range(5):
    #for row in cursor:
        print 'Queuing:'
        q.put(i)
    #q.put(row[1])

# Now wait for the queue to be empty, indicating that we have processed all of the downloads.
print '*** Main thread waiting'
q.join()
print '*** Done'