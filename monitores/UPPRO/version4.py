import random
import threading
import time

AFORO = 20
CLIENTES = 25
RESERVACION_MAX = round(AFORO*0.20)
MESEROS = round(AFORO * 0.10)
COCINEROS = round(AFORO * 0.10)
TO_CONSUME = 100

accion = ["Reservar", "Cola"]
ordenes = ["Pizza", "Hamburguesa", "Papas"]

class Restaurante(object):
  def __init__(self):
    self.mutex = threading.Lock()
    self.clientes = threading.Condition(self.mutex)
    self.clientePedido = threading.Condition(self.mutex)
    self.cocineros = threading.Condition(self.mutex)
    self.meseros = threading.Condition(self.mutex)
    self.enCola = []
    self.enReservacion = []
    self.adentro = []
    self.ordenes = []
    self.comidas = []
    self.afuera = []
    
  def descansoMesero(self):
    with self.mutex:
      if len(self.adentro) > 0:
        return False
      else:
        self.meseros.wait()
        return True
      
  def descansoCocinero(self):
    with self.mutex:
      if len(self.ordenes) > 0:
        return False
      else:
        self.cocineros.wait()
        return True

  def puedoReservar(self):
    return len(self.enReservacion) < RESERVACION_MAX
    
  def puedoEntrar(self):
    return len(self.adentro) < AFORO
      
  def entrar(self):
    print(f"Cliente {self} entra al restaurante")
    self.adentro.append(self)
    self.meseros.notify()
    
  def ordenar(self):
    with self.mutex:
      print(f"Mesero {self} atendiendo")
      decision = random.choice(ordenes)
      time.sleep(1)
      self.ordenes.append(decision)
      
  
  def cocinar(self):
    with self.mutex:
      print(f"Cocinero {self} cocinando")
      if len(ordenes) == 0:
        print("Ya no hay ordenes")
      else:
        orden = self.ordenes.pop()
        time.sleep(1)
        self.comidas.append(orden)
        print(f"Cocinero {self} termina: {orden}")
        self.servir()
    
  def servir(self):
    orden = self.comidas.pop()
    time.sleep(1)
    print(f"Mesero {self} entrega: {orden}")
    self.clientePedido.notify()
    
  def comer(self):
    print(f"Cliente {self} comiendo")
    time.sleep(1)
    print(f"Cliente {self} terminó de comer")
    
  def salir(self):
    self.adentro.pop()
    print(f"Cliente {self} se va del restaurante")
    time.sleep(1)
    self.afuera.append(self)
    self.clientes.notify()
    
  def recepcion(self):
    with self.mutex:
      decision = random.choice(accion)
      
      if decision == "Reservar":
        if(self.puedoReservar()):
          print(f"Cliente {self} con reservación")
          self.enReservacion.append(self)
          time.sleep(1)
          self.entrar()
          self.clientePedido.wait()
        else:
          print("Ya no hay reservaciones\n")
          decision = "Cola"
      
      if decision == "Cola":
        print(f"Cliente {self} en cola")
        time.sleep(2)
        if(self.puedoEntrar()):
          self.entrar()
          self.clientePedido.wait()
        else:
          print(f"Cliente {self} esperando para entrar")
          self.clientes.wait()

def meseros(restaurante):
  for i in range(MESEROS):
    while(restaurante.descansoMesero() == False):
        restaurante.ordenar()
    print(f"Mesero {i} descansando")

def cocineros(restaurante):
  for i in range(COCINEROS):
    while(restaurante.descansoCocinero() == False):
      restaurante.cocinar()
    print(f"Cocinero {i} descansando")

def clientes(restaurante):
  for i in range(CLIENTES):
    restaurante.recepcion()
    restaurante.comer()
    restaurante.salir()

def main():
  threads=[]
  restaurante = Restaurante()
  
  for c in range(CLIENTES):
    c = threading.Thread(target=clientes, args=(restaurante,))
    threads.append(c)
    
  for m in range(MESEROS):
    m = threading.Thread(target=meseros, args=(restaurante,))
    threads.append(m)
    
  for c in range(COCINEROS):
    c = threading.Thread(target=cocineros, args=(restaurante,))
    threads.append(c)
  
  for t in threads:
    t.start()
  
if __name__ == "__main__":
  main()