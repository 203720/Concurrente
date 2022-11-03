import threading
import time
import random
from queue import Queue

AFORO = 20
CLIENTES = 25
RESERVACION_MAX = round(AFORO*0.20)
MESEROS = round(AFORO * 0.10)
COCINEROS = round(AFORO * 0.10)

accion = ["Reservar", "Cola"]

class Restaurante():
  mutex = threading.Lock()
  clientes = threading.Condition()
  mesero = threading.Condition()
  cocinero = threading.Condition()
  clientes_reservacion = threading.Condition()
    
  adentro = Queue(AFORO)
  ordenes = Queue()
  comidas = Queue()
  reservaciones = Queue(RESERVACION_MAX)

  def __init__(self):
    super(Restaurante, self).__init__()

  def en_cola(self, cliente):
    self.clientes_reservacion.acquire()
    print(f"Cliente {cliente.id} está en la cola, paga cover\n")
    time.sleep(2)
    self.mutex.acquire()
    self.entrar(cliente)
    self.clientes_reservacion.notify()
    self.clientes_reservacion.release()

  def reservacion(self, cliente):
    self.clientes_reservacion.acquire()
    if self.reservaciones.full():
      self.clientes_reservacion.wait()
    else:
      self.reservaciones.put(cliente)
      print(f"Cliente {cliente.id} con reservación, no paga cover\n")
      time.sleep(3)

    self.mutex.acquire()
    self.entrar(cliente)
    self.reservaciones.get()
    self.clientes_reservacion.notify()
    self.clientes_reservacion.release()

  def entrar(self, cliente):
    self.clientes.acquire()
    if self.adentro.full():
      print(f"UPPRO está lleno, cliente {cliente.id} esperando...\n")
      self.clientes.wait()
    else:
      print(f"Cliente {cliente.id} entra a UPPRO\n")
      time.sleep(2)
      self.adentro.put(cliente)
      print(f"El recepcionista asigna una mesa a el cliente {cliente.id}\n")
      self.mesero.acquire()
      self.mesero.notify()
      self.mesero.release()
      self.mutex.release()
      self.clientes.release()

  def ordenar(self, mesero):
    while True:
      time.sleep(2)
      self.mesero.acquire()
      if self.adentro.empty():
        print(f"Mesero {mesero.id} está descansando Zzz\n")
        self.mesero.wait()
      else:
        cliente = self.adentro.get()
        if cliente.atendido == "no":
          print(f"Mesero {mesero.id} tomando orden a cliente {cliente.id}...\n")
          time.sleep(2)
          print(f"El pedido del cliente {cliente.id} se añadió a la lista de ordenes\n")
          self.ordenes.put(cliente.id)
          self.cocinero.acquire()
          self.cocinero.notify()
          self.cocinero.release()
          cliente.atendido = "si"
          self.mesero.release()
        else:
          self.mesero.release()

  def cocinar(self, cocinero):
    while True:
      time.sleep(2)
      self.cocinero.acquire()
      if self.ordenes.empty():
        print(f"Cocinero {cocinero.id} está descansando Zzz\n")
        self.cocinero.wait()
      else:
        orden = self.ordenes.get()
        print(f"Cocinero {cocinero.id} preparando orden de cliente {orden}...\n")
        time.sleep(2)
        print(f"La orden del cliente {orden} está lista!\n")
        self.comidas.put(orden)
        self.cocinero.release()

  def comer(self):
    time.sleep(2)
    if not self.comidas.empty():
      cliente = self.comidas.get()
      print(f"Cliente {cliente} está comiendo...\n")
      time.sleep(3)
      print(f"Cliente {cliente} terminó de comer!\n")
      print(f"Cliente {cliente} se ha ido :(\n")


class Cliente(threading.Thread):
  conta = 1
  atendido = "no"

  def __init__(self):
    super(Cliente, self).__init__()
    self.id = Cliente.conta
    Cliente.conta += 1

  def run(self):
    time.sleep(2)
    decision = random.choice(accion)
    if decision == "Reservar":
      restaurante.reservacion(self)
    else:
      restaurante.en_cola(self)
    restaurante.comer()


class Mesero(threading.Thread):
  conta = 1

  def __init__(self):
    super(Mesero, self).__init__()
    self.id = Mesero.conta
    Mesero.conta += 1

  def run(self):
    restaurante.ordenar(self)


class Cocinero(threading.Thread):
  conta = 1

  def __init__(self):
    super(Cocinero, self).__init__()
    self.id = Cocinero.conta
    Cocinero.conta += 1

  def run(self):
    restaurante.cocinar(self)


def main():
  threads = []
  
  print(f"\nBienvenido a UPPRO\n")

  for i in range(CLIENTES):
    threads.append(Cliente())
    
  for i in range(MESEROS):
    threads.append(Mesero())
  
  for i in range(COCINEROS):
    threads.append(Cocinero())

  for t in threads:
    t.start()

if __name__ == '__main__':
    restaurante = Restaurante()
    main()