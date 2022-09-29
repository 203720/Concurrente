import threading

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
def free(id):
    objects[id].release()
    objects[(id-1) % peopleN].release()
    print(f"Persona {id} terminó de comer.")

# Proceso de la persona comiendo y las personas esperando  
def eating(id):
    
    if catch(id):
        print(f"Persona {id} comiendo")
        peopleEat.append(id)
        
        difference_1 = set(peopleTotal).difference(set(peopleEat))
        difference_2 = set(peopleEat).difference(set(peopleTotal))
        list_difference = list(difference_1.union(difference_2))
    
        print(f"Personas esperando: {list_difference}")
        
        free(id)
            
if __name__ == '__main__':
    hilos = []
    
    # Inicialización de palillos
    for _ in range(peopleN):
        objects.append(threading.Lock())
        
    for i in range(peopleN):
        peopleTotal.append(i)
        nuevo_hilo = threading.Thread(target=eating, args=(i,))
        hilos.append(nuevo_hilo)
    
    # Iniciar ejecución de los hilos
    for hilo in hilos:
        hilo.start()
