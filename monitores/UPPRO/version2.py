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

class Cliente(threading.Thread):
  conta = 0
  def __init__(self):
    super(Cliente, self).__init__()
    self.id  = Cliente.conta
    Cliente.conta += 1
    
  def puedoReservar(self):
    return len(reservacion) < RESERVACION_MAX
  
  def puedoEntrar(self):
    return len(restaurante) < AFORO
  
  def entrar(self):
    print(f"Cliente {self} entra al restaurante")
    restaurante.append(self)
    self.despertarMesero()
  
  def despertarMesero(self):
      meseros.wait()
      meseros.notify()
      time.sleep(2)
      self.comer()
      
  def comer(self):
    orden = Mesero(threading.current_thread)
    print(f"Cliente {self.id} comiendo")
    time.sleep(3)
    print(f"Cliente {self.id} termino de comer")
    self.retirarse()
    
  def retirarse(self):
    restaurante.pop()
    print(f"Cliente {self.id} se ha ido")
    clientes.notify()
    
  def run(self):
    with mutex:
      
      if decision == "Reservar":
        if(self.puedoReservar()):
          print(f"Cliente {self.id} con reservación")
          reservacion.append(self)
          time.sleep(1)
          reservacion.pop()
          self.entrar()
        else:
          print("Ya no hay reservaciones\n")
          decision = "Cola"
          
      if decision == "Cola":
        print(f"Cliente {self.id} en cola")
        time.sleep(2)
        if(self.puedoEntrar()):
          self.entrar()
        else:
          clientes.wait()
      
class Mesero(threading.Thread):
  conta = 0
  def __init__(self):
    super(Mesero, self).__init__()
    self.id  = Mesero.conta
    Mesero.conta += 1
    
  def atenderCliente(self):
    with mutex:
      while(self.noHayClientes()):
        print(f"Mesero {self.id} descansando")
        meseros.wait()
      print(f"Mesero {self.id} atendiendo")
      decision = random.choice(orden)
      ordenes.append(decision)
      meseros.wait()
      self.despertarCocinero()
  
  def despertarCocinero(self):
    with mutex:
      cocineros.notify()
        
  def entregarComida(self):
    with mutex:
      comidas.pop()
      print(f"Mesero {self.id} entrega comida")
      
        
  def noHayClientes(self):
      return len(restaurante) == 0
    
  def run(self):
    self.atenderCliente()
        
class Cocinero(threading.Thread): 
  conta = 0
  def __init__(self):
    super(Cocinero, self).__init__()
    self.id  = Cocinero.conta
    Cocinero.conta += 1
    
  def prepararPedido(self):
    with mutex:
      while(self.noHayPedidos()):
        print(f"Cocinero {self.id} descansando")
        cocineros.wait()
      print(f"Cocinero {self.id} cocinando")
      aux = ordenes.pop()
      comidas.append(aux)
      meseros.notify()
    
  def noHayPedidos(self):
    return len(ordenes) == 0
    
  def run(self):
    self.prepararPedido()


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