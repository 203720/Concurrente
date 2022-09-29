import threading
import time
import random

objects = []
peopleEat = []
peopleTotal = []
peopleN = 8

# Se toman los palillos. El orden es de izquierda a derecha.
def catch(id):
    left_object = objects[id]
    right_object = objects[(id-1) % peopleN]
    
    left_object.acquire()
    
    if right_object.acquire():
        return True
    else:
        left_object.release()
        return False
    
# Se liberan los palillos cercanos a la persona
def free(id, timeEat):
    objects[id].release()
    objects[(id-1) % peopleN].release()
    print(f"Persona {id+1} terminó de comer en {timeEat} segundos.\n")

# Proceso de la persona comiendo y las personas esperando  
def eating(id):
    
    if catch(id):
        print(f"Persona {id+1} comiendo")
        peopleEat.append(id+1)
        
        difference_1 = set(peopleTotal).difference(set(peopleEat))
        difference_2 = set(peopleEat).difference(set(peopleTotal))
        list_difference = list(difference_1.union(difference_2))

        print(f"Personas esperando: {list_difference}")
        
        # Tiempo que tarda cada hilo en ejecutarse, entre 0 y 5 segundos
        timeEat = random.uniform(0,5)
        time.sleep(timeEat)
        
        free(id, timeEat)
            
if __name__ == '__main__':
    hilos = []
    
    # Inicialización de palillos
    for _ in range(peopleN):
        objects.append(threading.Lock())
    
    # Inicialización de personas e hilos    
    for i in range(peopleN):
        peopleTotal.append(i+1)
        nuevo_hilo = threading.Thread(target=eating, args=(i,))
        hilos.append(nuevo_hilo)
    
    # Ejecución de los hilos
    for hilo in hilos:
        hilo.start()
