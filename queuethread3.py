# System modules
import subprocess
from Queue import Queue
from threading import Thread
from crontab import CronTab
import threading
import time
import logging
import pymssql

# Global Variables
# Estas rutas habria que guardarlas en algun fichero de configuracion
rutaneuman = "/data/sites"
rutalog = "/home/administrador/genasa2logs/"

print '\nMain thread waiting......................................'

if __name__ == "__main__":

    #Instancio la cola y el cron
    queue = Queue()
    cron = CronTab()
    print '\n', threading.currentThread().getName(), 'Lanzado thread principal......................................'

    #Relleno la cola con la informacion de los cron a ejecutar
    conn = pymssql.connect(server='172.16.5.1', user='undanet', password='undanet2015', port=1433, database='neuman')
    query = 'select sp.id, sp.alias, sp.cronCommand, sp.description from neuman.dbo.stock_platform sp join neuman.dbo.platform p on p.id = sp.platform_id where sp.active = 1 and sp.is_webservice = 0 and p.active = 1'
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print '\nEncolando......................................id: ', row[0], ' alias: ', row[1], ' slices: ', row[2], ' description: ', row[3]
        cron_info = [ row[0], row[1], row[2], row[3] ]
        queue.put(cron_info)

def Enclosures(queue, php=None):

    print '\nLooking for the next item......................................'
    cron_info_queue = queue.get()
    idcron = cron_info_queue[0]
    alias = cron_info_queue[1]
    slices = cron_info_queue[2]
    description = cron_info_queue[3]
    #print 'Id: '+ idcron +' Alias: '+alias+' .Slices: '+slices+' .Description: '+description
    #print ' Alias: ' + alias + ' .Slices: ' + slices + ' .Description: ' + description

    cmd = ["php", "%s/neuman/neuman/bin/console neuman:stock:publish %s >> %s_publish_log.txt 2>&1" % (rutaneuman, alias, alias)]
    #subprocess.call(cmd);

    job = cron.new(command=cmd, comment=idcron)
    #job = cron.new(command=cmd)
    #job.setall(2, 10, '2-4', '*/2', None)
    job.setall(slices)

    print '\n', threading.currentThread().getName(), 'Lanzado. Alias: '+alias
    #time.sleep(1)
    #q.task_done() #Informa de que una tarea encolada ha sido terminada


# Procesamos la cola siempre que no este vacia
while not queue.empty():

    print '\nProcesando la cola......................................'
    worker = Thread(target=Enclosures, args=(queue,))
    worker.setDaemon(True)
    worker.start()

print '\nDone......................................'
