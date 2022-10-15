import random
import threading
import time

PRODUCTORES = 5 #Número de productores
CONSUMIDORES = 5 #Número de consumidores
MAX_BUFFER = 50

buffer = [] #Bodega
consumirProductos = threading.Semaphore(0)
      
class Productor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Productor, self).__init__()
    self.id  = Productor.conta
    Productor.conta += 1
  
  def producir(self):
    while True:
      if MAX_BUFFER > len(buffer):
        item = random.randint(0,100)
        buffer.append(item)
        print(f"Productor  {self.id} almacena producto: [{item}]. Productos en bodega: {buffer}")
        consumirProductos.release()
      else:
        print(f"Bodega llena. Productor {self.id} esperando")
      time.sleep(3)
      
  def run(self):
    for _ in range(PRODUCTORES):
      self.producir()
      
class Consumidor(threading.Thread):
  conta = 0
  
  def __init__(self):
    super(Consumidor, self).__init__()
    self.id  = Consumidor.conta
    Consumidor.conta += 1
  
  def consumir(self):
    while True:     
      if len(buffer)>0:
        item = buffer.pop()
        print(f"Consumidor  {self.id} extrae producto: [{item}]. Productos en bodega: {buffer}\n")
        consumirProductos.acquire()
      else:
        print(f"Bodega vacia. Consumidor {self.id} esperando")
      time.sleep(3) 

  def run(self):
    for _ in range(CONSUMIDORES):
      self.consumir()
  
def main():    
  productores = []
  consumidores = []

  for i in range(PRODUCTORES):
    productores.append(Productor())
      
  for i in range(CONSUMIDORES):
    consumidores.append(Consumidor())

  for p in productores:
    p.start()
    
  for c in consumidores:
    c.start()

if __name__ == "__main__":
    main()