import threading
import time
import random

PERSONAS = 10
MAX_BALANCE = 5000

balance = 0
opcionesDinero = [100, 200, 300, 400, 500, 1000]

accion = [1, 2]

mutex = threading.Lock()
notFull = threading.Condition(mutex)
notEnough = threading.Condition(mutex)

class Persona(threading.Thread):
  conta = 0
  def __init__(self):
    super(Persona, self).__init__()
    self.id  = Persona.conta
    Persona.conta += 1
    
  def sacar(self):
    global balance
    with mutex:
      while balance == 0:
        print(f"Cuenta vacía. Persona {self.id} esperando para sacar...\n")
        notEnough.wait()
      cantidad = random.choice(opcionesDinero)
      if(balance>=cantidad):
         balance -= cantidad 
         print(f"Persona {self.id} saca $[{cantidad}]. Balance: {balance}\n")
         notFull.notify()
      else:
        print(f"Persona  {self.id} no puede sacar $[{cantidad}]. No hay suficiente dinero. Balance: {balance}\n")
        notEnough.wait()
      time.sleep(5)
      
  def depositar(self):
    global balance
    with mutex:
      while balance == MAX_BALANCE:
        print(f"Cuenta llena. Persona {self.id} esperando a depositar...\n")
        notFull.wait()
      cantidad = random.choice(opcionesDinero)
      balance += cantidad
      if balance > MAX_BALANCE:
        print(f"Rebasa el máximo. Persona {self.id} esperando a depositar...\n")
        balance -= cantidad
        notFull.wait()
      else:
        print(f"Persona {self.id} deposita $[{cantidad}]. Balance: {balance}\n")
        notEnough.notify()
        time.sleep(5)
           
  def run(self):
    for _ in range(100):
      decision = random.choice(accion)
      if decision == 1:
        self.sacar()
      else:
        self.depositar()

def main():    
  personas = []

  for i in range(PERSONAS):
    personas.append(Persona())

  for p in personas:
    p.start()

if __name__ == "__main__":
    main()