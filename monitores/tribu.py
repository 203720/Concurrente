import threading
import time
import random
from queue import Queue

MIEMBROS = 8
MAX_OLLA = 10

class Tribu():
  mutex = threading.Lock()
  miembros = threading.Condition()
  cocinero = threading.Condition()
  
  olla = Queue(MAX_OLLA)
  
  def __init__(self):
    super(Tribu, self).__init__()
    
  def comer(self, miembro):
    self.miembros.acquire()
    self.mutex.acquire()
    if self.olla.empty():
      print(f"Olla vacía: {self.olla.qsize()}. Se despierta al cocinero...\nMiembro {miembro.id} esperando...\n")
      self.miembros.wait()
      self.miembros.release()
      self.cocinero.acquire()
      self.cocinero.notify()
      self.cocinero.release()
    else:
      time.sleep(1)
      self.olla.get()
      self.mutex.release()
      print(f"Miembro {miembro.id} se sirve de la olla. Misioneros en la olla {self.olla.qsize()}\n")
      self.miembros.release()
    
  def cocinar(self):
    while True:
      time.sleep(1)
      self.cocinero.acquire()
      
      if self.olla.full():
        print(f"Cocinero descansando. Olla llena: {self.olla.qsize()}\n")
        self.mutex.release()
        self.miembros.acquire()
        self.miembros.notify()
        self.miembros.release() 
        self.cocinero.release() 
        
      if self.olla.empty():
        while self.olla.qsize()<MAX_OLLA:
          time.sleep(1)
          misionero = random.randint(0, 100)
          self.olla.put(misionero)
          print(f"Cocinero preparando misionero. Misioneros en la olla {self.olla.qsize()}\n") 
    
class Miembros(threading.Thread):
  conta = 1
  
  def __init__(self):
    super(Miembros, self).__init__()
    self.id = Miembros.conta
    Miembros.conta += 1
  
  def run(self):
    for _ in range(MIEMBROS):
      time.sleep(1)
      tribu.comer(self)

class Cocinero(threading.Thread):
  def __init__(self):
    super(Cocinero, self).__init__()
    self.id = 1
    
  def run(self):
    time.sleep(1)
    tribu.cocinar()
    
def main():
  threads = []
  
  for i in range(MIEMBROS): 
    threads.append(Miembros())
    
  threads.append(Cocinero())
  
  for t in threads:
    t.start()
    
if __name__ == '__main__':
  tribu = Tribu()
  main()