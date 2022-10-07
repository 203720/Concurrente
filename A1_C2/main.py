import threading
import time

PRODUCTORES = 1 #Número de productores
CONSUMIDORES = 2 #Número de consumidores
PRODUCTO_INIT = 0

buffer = [] #Bodega
mutex = threading.Lock() #Exclusión mutua al insertar o quitar elementos
notEmpty = threading.Semaphore(0) #Bloquear a los consumidores cuando no haya productos
      
class Productor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Productor, self).__init__()
    self.id  = Productor.conta
    Productor.conta += 1
  
  def productor(self):
    global PRODUCTO_INIT
    while True:
      with mutex:
        buffer.append(PRODUCTO_INIT) #Almacena un producto
        PRODUCTO_INIT +=1
        print("Productor ", (self.id)," almacena un producto")
        time.sleep(2)
      notEmpty.release()
      print("Productos en bodega:",len(buffer))
      
  def run(self):
    self.productor()
      
class Consumidor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Consumidor, self).__init__()
    self.id  = Consumidor.conta
    Consumidor.conta += 1
  
  def consumidor(self):
    global PRODUCTO_INIT
    while True:
      notEmpty.acquire()
      time.sleep(2)
      with mutex:
        aux = buffer.pop(0)
        print("Consumidor ", (self.id)," extrae un producto")
        PRODUCTO_INIT +=1
      print("Productos en bodega:",len(buffer))

  def run(self):
    self.consumidor()
  
def main():
    personas = []

    for i in range(CONSUMIDORES):
      personas.append(Productor())
      
    for i in range(PRODUCTORES):
      personas.append(Consumidor())

    for t in personas:
        t.start()

if __name__ == "__main__":
    main()