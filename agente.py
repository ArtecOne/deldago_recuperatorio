from abc import ABC , abstractmethod

class Agente:
    def __init__(self , codigo : str, pos_actual : "Ubicacion" , destino : "Ubicacion" , amigos : list["Agente"]) -> "Agente":

        self._mi_codigo : str = codigo
        self._energia : int = 50
        
        self._veces_rescatado : int = 0
        self._ordenes_completas : int = 0
        
        self._posicion : "Ubicacion" = pos_actual
        self._central : "Ubicacion" = pos_actual
        self._destino : "Ubicacion" = destino
        self._destino_null : "Ubicacion" = destino
        
        self._amigos : list['Agente'] = amigos
        
        self._estado : Estado = None
        self.set_estado(Esperando)
        
        self._orden_paquetes : "OrdenEntrega" = None
        
        self._inventario : list["Paquete"] = []

        self._direccion : int = 1
    
    
    @property
    def codigo(self) -> str:
        return self._mi_codigo
    
    @property
    def rescates(self) -> int:
        return self._veces_rescatado
    
    @rescates.setter
    def rescates(self, cant) -> None:
        self._veces_rescatado += cant
    
    @property
    def ordenes_completas(self) -> int:
        return self._ordenes_completas
    
    @ordenes_completas.setter
    def ordenes_completas(self , cant) -> None:
        self._ordenes_completas += cant
    
    @property
    def amigos(self) -> list['Agente']:
        return self._amigos
    
    @property
    def destino(self) -> "Ubicacion":
        return self._destino
    
    @destino.setter
    def destino(self , destino : "Ubicacion") -> None:
        self._destino = destino
    
    @property
    def energia(self) -> int:
        return self._energia
    
    @energia.setter
    def energia(self , cant : int) -> None:
        self._energia = cant
    
    @property
    def orden_entrega(self) -> "OrdenEntrega":
        return self._orden_paquetes
    
    @orden_entrega.setter
    def orden_entrega(self , orden : "OrdenEntrega") -> None:
        if orden == None:
            self._orden_paquetes = None
            return
        
        orden.asignado_a = self
        self._orden_paquetes = orden
    
    @property
    def posicion(self) -> "Ubicacion":
        return self._posicion
    
    @posicion.setter
    def posicion(self , pos : "Ubicacion") -> None:
        self._posicion = pos
    
    def  get_destino_null(self):
        return self._destino_null
    
    def get_central(self) -> "Ubicacion":
        return self._central
    
    def direccion(self) -> int:
        return self._direccion
    
    def reversa(self) -> None:
        self._direccion *= -1
    
    def set_estado(self , estado : "Estado"):
        self._estado = estado()
        self._estado.agente = self
    
    def inventario(self) -> list["Paquete"]:
        return self._inventario
    
    def set_inventario(self , nuevo_inventario : list):
        self._inventario = nuevo_inventario
    
    def añadir_paquete(self , paquete : "Paquete") -> None:
        self._inventario.append(paquete)
    
    def que_soy(self):
        return 'Agente'
    
    def main(self):
        self._estado.main()
        
class AgenteRescate(Agente):
    def __init__(self , codigo , pos_actual , destino , a_rescatar):
        super().__init__(codigo , pos_actual , destino , a_rescatar)
        
        self._energia = 120
        self._mi_codigo = 'AgenteRescate-' + codigo
    
    def que_soy(self):
        return 'Rescate'


class Estado(ABC):
    
    @property
    def agente(self) -> Agente:
        return self._agente
    
    @agente.setter
    def agente(self , agent : Agente):
        self._agente = agent
    
    @abstractmethod
    def main(self):
        pass

class Rescatando(Estado):
    def main(self):
        
        if self.agente.posicion == self.agente.amigos[0].posicion:
            self.agente.amigos[0].energia = 50
    
        print(f'{self.agente.codigo} ha rescatado a {self.agente.amigos[0].codigo}\n')

class Ayuda(Estado):
    def __init__(self):
        self._rescate_creado = False
    
    def crear_rescate(self):
        self._salvador = AgenteRescate(self.agente.codigo , self.agente.get_central() , self.agente.posicion , [self.agente])
        
        self.agente.amigos.append(self._salvador)

        self._rescate_creado = True
    
    def main(self):
        if not self._rescate_creado:
            self.crear_rescate()
        
        if self.agente.energia == 50:
            self.agente.amigos.remove(self._salvador)
            del self._salvador
            self.agente.rescates = 1
            self.agente.set_estado(Movimiento)
            return
        
        print(f'el agente {self.agente.codigo} esta muy cansado para continuar')

class Esperando(Estado):
    def asignar_paquetes(self) -> None:
        for paquete in self.agente.orden_entrega.paquetes():
            paquete.asignado = self.agente
            
        self.asignar_inventario()

    
    def asignar_inventario(self):
        
        print(f"hay {self.agente.orden_entrega.cuantos_hay()} paquetes en esta orden")
        
        for paquete in self.agente.orden_entrega.paquetes():
            if not paquete.entregado and len(self.agente.inventario()) < 2:
                self.agente.añadir_paquete(paquete)
                
        if self.agente.destino == self.agente.get_central():
            self.agente.destino = self.agente.get_destino_null()
    
    def main(self):
        if self.agente.que_soy() == 'Rescate':
            self.agente.set_estado(Movimiento)
            return
        
        if not self.agente.orden_entrega:
            print("sin ordenes...\n")
            return
        
        print("asignando paquetes....\n")
        self.asignar_paquetes()
        
        if self.agente.inventario() == []:
            print("nada por entregar....\n")
            self.agente.orden_entrega.entregar()
            return
        
        self.agente.set_estado(Movimiento)
        

class Movimiento(Estado):
    def asignar_destino(self):
        self.agente.destino = self.agente.inventario()[0].destino
        
    def descansar(self) -> None:
        if self.agente.posicion.es_plaza:
            print("descanso \n")
            while self.agente.energia < 50:
                self.agente.energia += 5

    def avanzar(self) -> None:
        if self.agente.posicion.siguiente_ubi:
            self.agente.posicion = self.agente.posicion.siguiente_ubi
            self.agente.energia -= 10
            
        else:
            self.agente.reversa()
    
    def retroceder(self) -> None:
        if self.agente.posicion.anterior_ubi != None:
            self.agente.posicion = self.agente.posicion.anterior_ubi
            self.agente.energia -= 10
            
        else:
            self.agente.reversa()
            
    def main(self):
        if  self.agente.destino.donde == "nada":
            self.asignar_destino()
        
        if self.agente.energia <= 10 and not self.agente.posicion.es_plaza:
            
            if self.agente.posicion.siguiente_ubi.es_plaza:
                self.avanzar()
            elif self.agente.posicion.anterior_ubi.es_plaza:
                self.retroceder()
            else:
                self.agente.set_estado(Ayuda)
                
            return
        
        if self.agente.destino == self.agente.get_central() and self.agente.posicion == self.agente.get_central():
            self.agente.set_estado(Esperando)
            return
        
        if self.agente.energia <= 10 or (self.agente.inventario() == [] and self.agente.posicion == self.agente.get_central() and not 'AgenteRescate-' in self.agente.codigo):
            self.descansar()
            return
        
        if self.agente.inventario() == [] and self.agente.destino == self.agente.get_central():
            print("yendo a central \n")
            self.retroceder()
            return
            
        if self.agente.direccion() == 1:
            self.avanzar()
            
        else:
            self.retroceder()
        
        #if self.agente.posicion.donde == self.agente.destino:
            #self.agente.set_estado(Esperando)
        
        if self.agente.posicion == self.agente.destino:
            if self.agente.que_soy() == 'Rescate':
                print('cambio de estado rescatando')
                self.agente.set_estado(Rescatando)
                return
            
            
            self.agente.set_estado(Entregar)
            return

class Entregar(Estado):
    def entregar(self) -> None:
        if self.agente.inventario() == []:
            return
        
        [(paquete.entregar() , print("entregaré \n")) for paquete in self.agente.inventario() if paquete.destino == self.agente.destino]
        
        self.agente.set_inventario([paquete for paquete in self.agente.inventario() if not paquete.entregado])
        
    def main(self):
        self.entregar()
        
        self.agente.destino = self.agente.inventario()[0].destino if self.agente.inventario() != [] else self.agente.get_central()
        
        self.agente.set_estado(Movimiento)