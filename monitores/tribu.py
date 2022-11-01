import threading
import time

MIEMBROS = 12
MAX_OLLA = 12
COCINEROS = 1

olla = []
mutex = threading.Lock()
miembro = threading.Condition(mutex)
cocinero = threading.Condition(mutex)

class Miembros(threading.Thread):
  conta = 1
  def __init__(self):
    super(Miembros, self).__init__()
    self.id  = Miembros.conta
    Miembros.conta += 1

  def comer(self):
    with mutex:
        while not olla:
            print(f"Olla vacía {olla}. Se despierta al cocinero...\nMiembro {self.id} esperando...\n")
            miembro.wait()
            cocinero.notify()
        olla.pop()
        print(f"Miembro {self.id} se sirve de la olla. Misioneros en la olla {olla}\n")
        time.sleep(2)
                 
  def run(self):
    for _ in range(MIEMBROS):
      self.comer()
      
class Cocineros(threading.Thread):
  
  def __init__(self):
    super(Cocineros, self).__init__()
    self.id  = 1
    
  def cocinar(self):
    if len(olla) == 0:
      while len(olla) < MAX_OLLA:
        print(f"Cocinero {self.id} preparando misioneros xd...\nOlla {olla}\n")
        item = 0
        olla.append(item)
        time.sleep(2)
    if len(olla) == MAX_OLLA:
      print(f"Olla llena. El cocinero {self.id} va a descansar...\nOlla {olla}\n")
      cocinero.wait()
      miembro.notify_all()
      
  def run(self):
    for _ in range(COCINEROS):
      self.cocinar()

def main():    
  miembros = []
  cocineros = []

  for i in range(MIEMBROS):
    miembros.append(Miembros())
      
  for i in range(COCINEROS):
    cocineros.append(Cocineros())

  for m in miembros:
    m.start()
    
  for c in cocineros:
    c.start()

if __name__ == "__main__":
    main()