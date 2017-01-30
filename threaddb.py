#Los hilos nos permiten realizar varias tareas a la vez, sin tener que parar la ejecucion del hilo principal que llamo a esa tarea.
import pymongo
import json
import time
import thread

def consultar_db(iden, coll):

    result = coll.find_one({ '_id' : iden }, { 'd' : 0 })
    print json.dumps(result)

def main():

    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.test
    collection = db.test

    for i in range(1,5):
        #consultar_db(i, collection)
        thread.start_new_thread(consultar_db, (i, collection))
        #time.sleep(1)

    #thread.start_new_thread(consultar_db, (1,))

    x = raw_input("Pulsa enter")
    print('Termino la funcion main')

main()