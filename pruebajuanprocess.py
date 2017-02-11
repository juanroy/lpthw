import pymssql
from multiprocessing import Process

class ConcurrentProcess(Process):

    def consultar_datos(self):

        conn = pymssql.connect(server='', user='', password='', port=, database='')

        #for i in range(1,5):
            #query = 'select id, active, alias, configuration from dbo.status_platform where id = %d' % i
        query = 'select id, active, is_webservice, alias, configuration from dbo.stock_platform where active = 1 and is_webservice = 0'
        cursor = conn.cursor()
        cursor.execute(query)

        for row in cursor:
            #print('row = %r' % (row,))
            #print 'id: ', row[0]
            #print 'active: ', row[1]
            #print 'webservice: ', row[2]
            #print 'alias: ', row[3]
            ##print 'configuration: ', row[4]
            #print '-' * 10

            #id = row[0]
            #alias = row[3]
            #if alias == '2_bercar':
            #    print 'id: ' + str(id) + ' alias: ' + alias
            #elif alias == 'schwalm_speed':
            #    print 'id: ' + str(id) + ' alias: ' + alias
            #else:
            #    print 'id: ' + str(id) + ' alias: ' + alias

            print 'Ahora lanzo el comando symfony'

    def run(self):

        self.consultar_datos()

if __name__ == "__main__":
    p = ConcurrentProcess()
    p.start()
    p.join()
