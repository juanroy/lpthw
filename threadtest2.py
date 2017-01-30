import time
from threading import Thread

def espera(n):
    time.sleep(n)

subproceso = Thread(target=espera, args=(5,))
subproceso.start()

while(subproceso.isAlive()):
    print "Esperando..."
    time.sleep(1)

print "He llegado."