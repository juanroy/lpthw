# System modules
from Queue import Queue
from threading import Thread
from crontab import CronTab
import threading
import time
import pymssql

# Global Variables
# Estas rutas habria que guardarlas en algun fichero de configuracion
rutaneuman = "/data/sites"
rutalog = "/home/administrador/genasa2logs/"

#print '\nMain thread waiting...'

def Enclosures(queue, php=None):

    #print '\nLooking for the next item...'
    cron_info_queue = queue.get()
    idcron = cron_info_queue[0]
    alias = cron_info_queue[1]
    slices = cron_info_queue[2]
    #print 'Id: ' + idcron + ' Alias: ' + alias + ' .Slices: ' + slices

    #Antes de crear el mismo cron dos veces compruebo que no lo he hecho antes
    cronitem = cron.find_comment(idcron)
    a = list(cronitem)
    #for lista in cronitem:
    #    print 'Cron %s ya tratado!!!' % lista
    #print '\nLongitud: ', len(a)
    if len(a) == 0:
        comando = "php %s/neuman/neuman/bin/console neuman:stock:publish %s >> %s_publish_log.txt 2>&1" % (rutaneuman, alias, alias)
        job = cron.new(command=comando,comment=idcron)
        job.setall(slices)
        #job.enable() #No se que hace este comando
        print threading.currentThread().getName(), 'Lanzado. idcron: ' + idcron

if __name__ == "__main__":

    #Instancio la cola y el cron
    queue = Queue()
    cron = CronTab()
    print '\n', threading.currentThread().getName(), 'Lanzado thread principal...'

    #Relleno la cola con la informacion de los cron a ejecutar
    conn = pymssql.connect(server='', user='', password='', port=, database='')
    query = 'select cast(sp.id as varchar(3)), sp.alias, sp.cronCommand, sp.description, cast(sp.platform_id as varchar(3)) from neuman.dbo.stock_platform sp join neuman.dbo.platform p on p.id = sp.platform_id where sp.active = 1 and sp.is_webservice = 0 and p.active = 1'
    #while True:
    for i in range(4):
        cursor = conn.cursor()
        cursor.execute(query)
        for row in cursor:
            cron_info = [row[0], row[1], row[2]]
            if cron_info not in queue.queue:
                print 'Encolando...id: ', row[0], ' alias: ', row[1], ' slices: ', row[2]
                try:
                    queue.put(cron_info)
                except:
                    print 'Error al encolar el cron %s' % cron_info
                time.sleep(0.2)
            #else:
            #    print 'Cron %s ya encolado!!!' % cron_info

# Procesamos la cola siempre que no este vacia
while not queue.empty():

    #print '\nProcesando la cola...'
    worker = Thread(target=Enclosures, args=(queue,))
    worker.setDaemon(True)
    worker.start()

#time.sleep(3)

#for job in cron:
#    print job

print '\nDone...'
