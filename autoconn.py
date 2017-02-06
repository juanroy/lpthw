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

if __name__ == "__main__":

    print '\n', threading.currentThread().getName(), 'Lanzado thread principal...'

    # Instancio la cola y el cron
    queue = Queue()
    cron = CronTab()

    #Conexion a la base de datos
    conn = pymssql.connect(server='172.16.5.1', user='undanet', password='undanet2015', port=1433, database='neuman')
    query = 'select cast(sp.id as varchar(3)), sp.alias, sp.cronCommand, sp.description, cast(sp.platform_id as varchar(3)) from neuman.dbo.stock_platform sp join neuman.dbo.platform p on p.id = sp.platform_id where sp.active = 1 and sp.is_webservice = 0 and p.active = 1'

def Enclosures(queue):

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
        print threading.currentThread().getName(), 'Lanzado. idcron: ' + idcron + '. alias: ' + alias + '. slices: ' + slices

while True:
#for i in range(4):

    #Relleno la cola con la informacion de los cron a ejecutar
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        cron_info = [row[0], row[1], row[2]]
        if cron_info not in queue.queue:
            #print 'Encolando...id: ', row[0], ' alias: ', row[1], ' slices: ', row[2]
            try:
                queue.put(cron_info)
            except:
                print 'Error al encolar el cron %s' % cron_info
        else:
            print 'Cron %s ya encolado!!!' % cron_info

    # Procesamos la cola siempre que no este vacia
    while not queue.empty():
        #print '\nProcesando la cola...'
        worker = Thread(target=Enclosures, args=(queue,))
        worker.setDaemon(True)
        worker.start()

    #Yo cambiaria este valor a 60 secs.
    time.sleep(0.2)

#time.sleep(3)
#for job in cron:
#    print job

print '\nDone...'
