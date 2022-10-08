import threading
import time

PRODUCTORES = 1 #Número de productores
CONSUMIDORES = 10 #Número de consumidores
producto_bodega = 0

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
    global producto_bodega
    while True:
      with mutex:
        buffer.append(producto_bodega) #Almacena un producto
        producto_bodega +=1
        print("\nProductor ", (self.id)," almacena un producto")
        print("Productos en bodega:",len(buffer))
        time.sleep(2)
      notEmpty.release()
      
  def run(self):
    self.productor()
      
class Consumidor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Consumidor, self).__init__()
    self.id  = Consumidor.conta
    Consumidor.conta += 1
  
  def consumidor(self):
    while True:
      notEmpty.acquire()
      with mutex:
        buffer.pop(0)
        print("\nConsumidor ", (self.id)," extrae un producto")
        print("Productos en bodega:",len(buffer),"\n")
        time.sleep(2)

  def run(self):
    self.consumidor()
  
def main():
    personas = []

    for i in range(PRODUCTORES):
      personas.append(Productor())
      
    for i in range(CONSUMIDORES):
      personas.append(Consumidor())

    for t in personas:
        t.start()

if __name__ == "__main__":
    main()