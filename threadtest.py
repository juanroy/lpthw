import time
import thread

def imprimir_mensaje(mensaje):
    while True:
        print(mensaje)
        time.sleep(1)

def main():
    mensaje = 'Thread1'
    mensaje2 = 'Thread2'

    thread.start_new_thread(imprimir_mensaje, (mensaje,))
    thread.start_new_thread(imprimir_mensaje, (mensaje2,))

    x = raw_input("Pulsa enter")

    print('Termino la funcion main')

main()