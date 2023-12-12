from abc import ABC , abstractmethod
from random import choice
import string

class Ubicacion():
    def __init__(self , nombre : str, orden : int , es_plaza : bool = False , anterior : "Ubicacion" = None ,siguiente : "Ubicacion" = None) -> "Ubicacion":
        super().__init__()

        self._donde : str = nombre
        self._orden : int = orden

        self._paquetes_entregados : list["Paquete"] = []

        self._es_plaza : bool = es_plaza

        self._vecino_der : Ubicacion = siguiente
        self._vecino_izq : Ubicacion = anterior

    @property
    def id(self) -> int:
        return self._orden
    
    @property
    def donde (self) -> str:
        return self._donde
    
    @property
    def es_plaza(self) -> bool:
        return self._es_plaza
    
    @property
    def siguiente_ubi(self) -> "Ubicacion":
        return self._vecino_der
    
    @siguiente_ubi.setter
    def siguiente_ubi(self , ubi : "Ubicacion") -> None:
        self._vecino_der = ubi
    
    @property
    def anterior_ubi(self) -> "Ubicacion":
        return self._vecino_izq
    
    @anterior_ubi.setter
    def anterior_ubi(self , ubi : "Ubicacion") -> None:
        self._vecino_izq = ubi

    def cuantos_paquetes_entregados(self) -> int:
        return len(self._paquetes_entregados)
    
    def dejar_paquete(self , paquete : "Paquete") -> None:
        self._paquetes_entregados.append(paquete)


class Mapa:
    def __init__(self) -> "Mapa":
        self._destino_null = Ubicacion("nada" , 0)
        
        self._ruta : list[Ubicacion] = [Ubicacion("Central" , 0 , True), Ubicacion("Plaza" , 1 , True),
                                        Ubicacion("Pilar" , 2 , ), Ubicacion("Savio" , 3),
                                        Ubicacion("Plaza" , 4 , True), Ubicacion("Escobar" , 5),
                                        Ubicacion("Tortuguitas" , 6) , Ubicacion("Plaza" , 7 , True)]
        self.asignar_rutas()
    
    @property
    def destino_null(self) -> Ubicacion:
        return self._destino_null
    
    def asignar_rutas(self):
        for index , ubi in enumerate(self._ruta):
            if ubi.id != len(self._ruta) - 1:
                ubi.siguiente_ubi = self._ruta[index + 1]

            if ubi.id != 0:
                ubi.anterior_ubi = self._ruta[index - 1]
                
    def nueva_ubicacion(self , nombre : str , es_plaza : bool = False):
        
        self._ruta.append(Ubicacion(nombre , len(self._ruta) , es_plaza))
        
        self.asignar_rutas()
        
    def get_ruta(self):
        return self._ruta
    
    
class Paquete:
    def __init__(self , codigo : str, destino : "Ubicacion" , orden : "OrdenEntrega") -> "Paquete":
        
        self._asignado_a : "Agente" = None
        self._mi_codigo : str = codigo
        self._destino  : "Ubicacion" = destino
        self._entregado : bool = False
        
        orden.añadir_paquete(self)
    
    @property
    def asignado(self) -> "Agente":
        return self._asignado_a
    
    @property
    def entregado(self) -> bool:
        return self._entregado
    
    @asignado.setter
    def asignado(self , agente : "Agente") -> None:
        self._asignado_a = agente

    @property
    def codigo(self) -> str:
        return self._mi_codigo
    
    @property
    def destino(self) -> "Ubicacion":
        return self._destino
    
    def entregar(self) -> None:
        self._destino.dejar_paquete(self)
        self._entregado = True


class OrdenEntrega:
    def __init__(self) -> "OrdenEntrega":
        
        self._asignado_a : "Agente" = None
        self._paquetes : list[Paquete] = []
        
        self._entregado : bool = False
    
    @property
    def asignado_a(self) -> "Agente":
        return self._asignado_a
    
    @asignado_a.setter
    def asignado_a(self , agente : "Agente"):
        self._asignado_a = agente
    
    @property
    def entregado(self) -> bool:
        return self._entregado
    
    def entregar(self) -> None:
        self._entregado = True
        
    def cuantos_hay(self) -> int:
        return len(self._paquetes)
    
    def paquetes(self) -> list[Paquete]:
        return self._paquetes
    
    def añadir_paquete(self , paquete : Paquete):
        paquete.asignado = self.asignado_a
        self._paquetes.append(paquete)

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
    
    def  get_destino_null(self) -> "Ubicacion":
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
    
    def set_inventario(self , nuevo_inventario : list) -> None:
        self._inventario = nuevo_inventario
    
    def añadir_paquete(self , paquete : "Paquete") -> None:
        self._inventario.append(paquete)
    
    def que_soy(self) -> str:
        return 'Agente'
    
    def main(self) -> None:
        self._estado.main()
        
class AgenteRescate(Agente):
    def __init__(self , codigo , pos_actual , destino , a_rescatar):
        super().__init__(codigo , pos_actual , destino , a_rescatar)
        
        self._energia : int = 120
        self._mi_codigo : str = 'AgenteRescate-' + codigo
    
    def que_soy(self) -> str:
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
    def main(self) -> None:
        
        if self.agente.posicion == self.agente.amigos[0].posicion:
            self.agente.amigos[0].energia = 50
    
        print(f'{self.agente.codigo} ha rescatado a {self.agente.amigos[0].codigo}\n')

class Ayuda(Estado):
    def __init__(self):
        self._rescate_creado : bool = False
    
    def crear_rescate(self) -> None:
        self._salvador : AgenteRescate = AgenteRescate(self.agente.codigo , self.agente.get_central() , self.agente.posicion , [self.agente])
        
        self.agente.amigos.append(self._salvador)

        self._rescate_creado = True
    
    def main(self) -> None:
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

    
    def asignar_inventario(self) -> None:
        
        print(f"hay {self.agente.orden_entrega.cuantos_hay()} paquetes en esta orden")
        
        for paquete in self.agente.orden_entrega.paquetes():
            if not paquete.entregado and len(self.agente.inventario()) < 2:
                self.agente.añadir_paquete(paquete)
                
        if self.agente.destino == self.agente.get_central():
            self.agente.destino = self.agente.get_destino_null()
    
    def main(self) -> None:
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
    def asignar_destino(self) -> None:
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
            
    def main(self) -> None:
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
        
    def main(self)  -> None:
        self.entregar()
        
        self.agente.destino = self.agente.inventario()[0].destino if self.agente.inventario() != [] else self.agente.get_central()
        
        self.agente.set_estado(Movimiento)
        
        
        
def generar_codigo(largo : int) -> str:
    letters_and_digits : str = string.ascii_letters + string.digits
    return ''.join(choice(letters_and_digits) for i in range(largo))

class NuevaSimulacion:
    def __init__(self) -> "NuevaSimulacion":
        self._ordenes : list[OrdenEntrega] = []
        self._activos : list[Agente] = []
        self._mapa : Mapa = Mapa()
        self._cant_vueltas : int = 1
    
    @property
    def mapa(self) -> Mapa:
        return self._mapa
    
    def crear_agentes(self , cant : int) -> None:
        name_agentes : list[str] = [generar_codigo(6) for _ in range(cant)]
        
        for name in name_agentes:
            self._activos.append(Agente(name , self._mapa.get_ruta()[0] , self._mapa.destino_null , self._activos))
    
    def crear_orden(self , cant_paquetes : int) -> None:
        name_paquetes : list[str] = [generar_codigo(6) for _ in range(cant_paquetes)]
                                                                         
        orden = OrdenEntrega()
        
        for name in name_paquetes:
            
            while True:
                eleccion = choice(self._mapa.get_ruta())

                if eleccion.es_plaza:
                    continue
                
                break
            
            Paquete(name , eleccion , orden)
        
        self._ordenes.append(orden)

            
    def asignar_ordenes(self) -> None:
        for agente in self._activos:
            agente.orden_entrega = None
        
        
        i = 0
        for orden in self._ordenes:
            if orden.entregado:
                continue
            
            if i > len(self._activos) - 1:
                i = len(self._activos) - 1
            
            if self._activos[i].orden_entrega:
                continue
            
            self._activos[i].orden_entrega = orden
            self._activos[i].ordenes_completas = 1
            
            i += 1
            
    def iniciar(self) -> None:
        print("iniciando\n")
        
        ruta = [ubi.donde for ubi in self._mapa.get_ruta()]
        
        print(f'tu ruta es {ruta}')
        
        self.asignar_ordenes()
        
        i = 0
        
        print(f"hay {len(self._ordenes)} cant ordenes \n")
        
        while i < 50:
            for agente in self._activos:
                print(f"{agente.codigo} con destino {agente.destino.donde}, esta en {agente.posicion.donde} con cant paquetes {len(agente.inventario())}, su energia es {agente.energia} \n")
                agente.main()
            
            i += 1
        
        suma = 0
        
        print(f"hay {len(self._activos)} cant de agentes")
        print(f"hay {len(self._ordenes)} cant de ordenes")
        
        print(f"se han completado ....")
        
        for orden in self._ordenes:
           if orden.entregado:
               suma += 1
                
        print(f"{suma}")
        print(f"en {self._cant_vueltas} cant de vueltas \n")
        
        print(f'los puntos son....')
        
        for agente in self._activos:
            print(f'{agente.codigo} ha sido rescatado {agente.rescates} cant de veces y ha completado {agente.ordenes_completas} cant de ordenes')
        
        if suma != len(self._ordenes):
            self._cant_vueltas += 1
            self.iniciar()
        
        
        
        
###############


simu = NuevaSimulacion()
simu.crear_agentes(1)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)
simu.crear_orden(cant_paquetes= 2)


simu.mapa.nueva_ubicacion("Antartida")
simu.mapa.nueva_ubicacion("Las Vegas")
simu.mapa.nueva_ubicacion("Obelisco")


simu.iniciar() 