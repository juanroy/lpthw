# System modules
import subprocess
from Queue import Queue
from threading import Thread
import threading
import time
import logging
import pymssql

# Set up some global variables
# Estas rutas habra que guardarlas en algun fichero de configuracion
rutaneuman = "/data/sites"
rutalog = "/home/administrador/genasa2logs/"

q = Queue()

print '\nMain thread waiting......................................'

# Filling in the queue
#while True:
if __name__ == "__main__":
    print '\n', threading.currentThread().getName(), 'Lanzado thread principal......................................'
    conn = pymssql.connect(server='', user='', password='', port=, database='')
    query = 'select sp.id, sp.alias, sp.cronCommand, sp.description from neuman.dbo.stock_platform sp join neuman.dbo.platform p on p.id = sp.platform_id where sp.active = 1 and sp.is_webservice = 0 and p.active = 1'

    cursor = conn.cursor()
    cursor.execute(query)

    for row in cursor:
        print '\nEncolando......................................id: ', row[0], ' alias: ', row[1]
        q.put(row[1])


def Enclosures(q, php=None):
    print '\nLooking for the next item......................................'
    alias = q.get()
    cmd = "php %s/neuman/neuman/bin/console neuman:stock:publish %s >> %s%s_goggel_publish_log.txt 2>&1" % (rutaneuman, alias, rutalog, alias)
    #subprocess.call(cmd.explode());
    print '\n', threading.currentThread().getName(), 'Lanzado. Alias: '+alias
    time.sleep(1)
    q.task_done()


# Processing the queue
while not q.empty():
    print '\nProcesando la cola......................................'
    worker = Thread(target=Enclosures, args=(q,))
    worker.setDaemon(True)
    worker.start()

print '\nDone......................................'
