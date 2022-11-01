import random
import threading
import time

AFORO = 10
CLIENTES = 20 
RESERVACION_MAX = round(AFORO*0.20)
MESEROS = round(AFORO * 0.10)
COCINEROS = round(AFORO * 0.10)

accion = ["Reservar", "Cola"]
orden = ["Pizza", "Hamburguesa", "Papas"]

reservacion = []
restaurante = []
ordenes = []
comidas = []

mutex = threading.Lock()
clientes = threading.Condition(mutex)
meseros = threading.Condition(mutex)
cocineros = threading.Condition(mutex)

class Restaurante(threading.Thread):
  
  def __init__(self,hilo):
    self.name=hilo.name
    self.id = hilo.id
    print(f"{self.name} {self.id}")
    
  def esCliente(hilo):
    return (hilo.name == "Cliente")
  
  def esMesero(hilo):
    return (hilo.name == "Mesero")
  
  def esCocinero(hilo):
    return (hilo.name == "Cocinero")
  
  def recepcion(self,hilo):
    decision = random.choice(accion)
    if decision == "Reservar":
      if(self.puedoReservar()):
        print(f"Cliente {hilo.id} con reservación")
        reservacion.append(hilo)
        time.sleep(1)
        reservacion.pop()
        self.entrar()
      else:
        print("Ya no hay reservaciones\n")
        decision = "Cola"
          
    if decision == "Cola":
      print(f"Cliente {hilo.id} en cola")
      time.sleep(2)
      if(self.puedoEntrar()):
        self.entrar()
      else:
        clientes.wait()    
        
  def cocina():
    print("a")
  
  def otro(self,hilo):
    print("a")
    if(self.esCliente(hilo)):
      self.recepcion()
    
    if(self.esCocinero(hilo)):
      self.cocina()
      
    if(self.esMesero(hilo)):
      self.cocina()
    
      
class Cliente(threading.Thread):
  conta = 1
  def __init__(self):
    super(Cliente, self).__init__()
    self.name = "Cliente"
    self.id  = Cliente.conta
    Cliente.conta += 1
    
  def run(self):
    Restaurante(self)
    
class Mesero(threading.Thread):
  conta = 1
  def __init__(self):
    super(Mesero, self).__init__()
    self.name = "Mesero"
    self.id  = Mesero.conta
    Mesero.conta += 1
    
  def run(self):
    Restaurante(self)
    
class Cocinero(threading.Thread):
  conta = 1
  def __init__(self):
    super(Cocinero, self).__init__()
    self.name = "Cocinero"
    self.id  = Cocinero.conta
    Cocinero.conta += 1
    
  def run(self):
    Restaurante(self)
    
def main():    
  clientes = []
  meseros = []
  cocineros = []

  for i in range(CLIENTES):
    clientes.append(Cliente())
    
  for i in range(MESEROS):
    meseros.append(Mesero())
    
  for i in range(COCINEROS):
    cocineros.append(Cocinero())
  
  for m in meseros:
    m.start()
    
  for c in cocineros:
    c.start()

  for c in clientes:
    c.start()

if __name__ == "__main__":
    main()