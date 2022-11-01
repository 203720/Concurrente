import threading
import time

PERSONAS = 8
COMER_CONTA = 50

class Persona(threading.Thread):
  mutex = threading.Lock()
  palillos = []
  disponible = []
  conta = 0
  
  def __init__(self):
    super(Persona, self).__init__()
    self.id  = Persona.conta
    print(self)
    self.right = (self.id - 1) % PERSONAS
    self.left = (self.id + 1) % PERSONAS
    Persona.conta += 1
    Persona.palillos.append(2)
    Persona.disponible.append(threading.Condition(Persona.mutex))
  
  def tomar_palillo(self):
    with Persona.mutex:
        while Persona.palillos[self.id] != 2:
            Persona.disponible[self.id].wait()
        Persona.palillos[self.left] -= 1
        Persona.palillos[self.right] -= 1
  
  def comer(self):
    print("Comiendo => " + str(self.id) + "\n")
    time.sleep(2)
    print("Terminó de comer => " + str(self.id) + "\n")

  def libera(self):
    with Persona.mutex:
      Persona.palillos[self.left] +=1
      Persona.palillos[self.right] +=1
      if Persona.palillos[self.left] ==2:
        Persona.disponible[self.left].notify()
      if Persona.palillos[self.right] ==2:
        Persona.disponible[self.right].notify()
        
    
  def run(self):
    for i in range(COMER_CONTA):
      time.sleep(0.15)
      self.tomar_palillo()
      self.comer()
      self.libera()
      
def main():
    personas = []

    for i in range(PERSONAS):
        personas.append(Persona())

    for p in personas:
        p.start()

if __name__ == '__main__':
    main()