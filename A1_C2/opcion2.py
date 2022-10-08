import threading
import time

PRODUCTOS_MAX = 2 #Número de producto máximo que produce cada productor
PRODUCTORES = 1 #Número de productores
CONSUMIDORES = 2 #Número de consumidores
PRODUCTO_INIT = 0

buffer = [] #Bodega
mutex = threading.Lock() 
notEmpty = threading.Semaphore(0) #Bloquear a los consumidores cuando no haya productos
      
class Productor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Productor, self).__init__()
    self.id  = Productor.conta
    Productor.conta += 1
  
  def productor(self):
    global PRODUCTO_INIT
      
    for i in range(PRODUCTOS_MAX):
      with mutex: #Con exclusión mutua
            buffer.append(PRODUCTO_INIT) #Almacena un producto
            PRODUCTO_INIT +=1
            print("Productor ", (self.id)," almacena un producto")
      notEmpty.release()
      print("Productos en bodega:",len(buffer))
      
  def run(self):
    time.sleep(5)
    self.productor()
      
class Consumidor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Consumidor, self).__init__()
    self.id  = Consumidor.conta
    Consumidor.conta += 1
  
  def consumidor(self):
    global PRODUCTO_INIT
    
    for i in range(PRODUCTOS_MAX):
      notEmpty.acquire()
      with mutex:
        aux = buffer.pop(0)
        print("Consumidor ", (self.id)," extrae un producto") 
        PRODUCTO_INIT +=1
      print("Productos en bodega:",len(buffer))
  
  def run(self):
    time.sleep(2)
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