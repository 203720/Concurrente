import threading
import time

PRODUCTORES = 5 #Número de productores
CONSUMIDORES = 5 #Número de consumidores
MAX_BUFFER = 10

buffer = []
mutex = threading.Lock()
notFull = threading.Condition(mutex)
notEmpty = threading.Condition(mutex)

class Productor(threading.Thread):
  conta = 0
  def __init__(self):
    super(Productor, self).__init__()
    self.id  = Productor.conta
    Productor.conta += 1
  
  def producir(self):
    with mutex:
      while len(buffer) == MAX_BUFFER:
        print(f"Bodega llena. Productor {self.id} esperando\n")
        notFull.wait()
      item = 0
      buffer.append(item)
      print(f"Productor  {self.id} almacena producto: [{item}]. Productos en bodega: {buffer}\n")
      if len(buffer) == 1:
        notEmpty.notify()
        print("Ya hay un producto en la bodega\n")
      time.sleep(2)
    
  def run(self):
    for _ in range(PRODUCTORES):
      self.producir()
  
class Consumidor(threading.Thread):
  conta=0
  def __init__(self):
    super(Consumidor, self).__init__()
    self.id  = Consumidor.conta
    Consumidor.conta += 1
    
  def consumir(self):
    with mutex:
      while not buffer:
        print(f"Bodega vacia. Consumidor {self.id} esperando\n")
        notEmpty.wait()
      item = buffer.pop()
      print(f"Consumidor  {self.id} extrae producto: [{item}]. Productos en bodega: {buffer}\n")
      notFull.notify()
      time.sleep(2)
              
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