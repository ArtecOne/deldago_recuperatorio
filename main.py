from abc import ABC
from random import randint , choice , randbytes

class Ubicacion(ABC):
    def __init__(self , nombre : str, orden : int , es_plaza : bool = False , anterior : "Ubicacion" = None ,siguiente : "Ubicacion" = None) -> None:
        super().__init__()

        self._donde : str = nombre
        self._orden : int = orden

        self._paquetes_entregados : list[Paquete] = []

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

class Paquete:
    def __init__(self , codigo : str, destino : Ubicacion) -> None:
        
        self._asignado_a : Agente = None
        self._mi_codigo : str = codigo
        self._destino  : Ubicacion = destino
        self._entregado : bool = False
    
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
    def destino(self) -> Ubicacion:
        return self._destino
    
    def entregar(self) -> None:
        self._destino.dejar_paquete(self)
        self._entregado = True


class Agente:
    def __init__(self , codigo : str, pos_actual : Ubicacion) -> None:

        self._mi_codigo : str = codigo
        self._energia : int = 50

        self._posicion : Ubicacion = pos_actual

        self._paquetes : list[Paquete] = []
        
        self._direccion : int = 1
        
        self._destino : Ubicacion = None
    
    @property
    def codigo(self) -> str:
        return self._mi_codigo
    
    @property
    def destino(self) -> Ubicacion:
        return self._destino

    @property
    def energia(self) -> int:
        return self._energia
    
    def posicion_actual(self) -> Ubicacion:
        return self._posicion
    
    def inventario(self) -> list[Paquete]:
        return self._paquetes
    
    def descansar(self) -> None:
        if self._posicion.es_plaza:
            print("descanso \n")
            while self._energia < 50:
                self._energia += 0.5

    def avanzar(self) -> None:
        if self._posicion.siguiente_ubi != None:
            self._posicion = self._posicion.siguiente_ubi
            self._energia -= 10
        else:
            self._direccion *= -1
    
    def retroceder(self) -> None:
        if self._posicion.anterior_ubi != None:
            self._posicion = self._posicion.anterior_ubi
            self._energia -= 10
        else:
            self._direccion *= -1
    
    def agregar_paquete(self , paquete : Paquete) -> bool:
        if paquete.asignado:
            return False
        
        if len(self._paquetes) > 2:
            return False
        
        
        paquete.asignado = self
        self._destino : Ubicacion = paquete.destino
        self._paquetes.append(paquete)
        
        return True
    
    def entregar(self) -> None:
        if self._paquetes == []:
            return
        
        [(paquete.entregar() , print("entregaré \n")) for paquete in self._paquetes if paquete.destino == self._destino]
        self._paquetes = [paquete for paquete in self._paquetes if paquete.destino != self._destino]
        
        self._destino = self._paquetes[0].destino if self._paquetes != [] else self._destino

    def main(self) -> None:
        if self._energia <= 10 and not self._posicion.es_plaza:
            if self._posicion.siguiente_ubi.es_plaza:
                self.avanzar()
            elif self._posicion.anterior_ubi.es_plaza:
                self.retroceder()
            else:
                print("ayudaaaaaa \n")
                
            return
        
        if self._energia <= 10 or (self._paquetes == [] and self._posicion.donde == "Central"):
            self.descansar()
            return
        
        if self._paquetes == [] and self._posicion.donde != "Central":
            print("yendo a central \n")
            self.retroceder()
            return
            
        if self._direccion == 1:
            self.avanzar()
        else:
            self.retroceder()
            
        if self._posicion == self._destino:
            self.entregar()

class Mapa:
    def __init__(self) -> None:
        name_agentes = ["f33" , "A78" , "99971" , "Y22"]



        self._ruta : list[Ubicacion] = [Ubicacion("Central" , 0 , True), Ubicacion("Plaza" , 1 , True),
                                        Ubicacion("Pilar" , 2 , ), Ubicacion("Savio" , 3),
                                        Ubicacion("Plaza" , 4 , True), Ubicacion("Escobar" , 5),
                                        Ubicacion("Tortuguitas" , 6) , Ubicacion("Plaza" , 7 , True)]
        self.asignar_rutas()

        self._activos : list[Agente] = [Agente(choice(name_agentes), self._ruta[0]) , Agente(choice(name_agentes) , self._ruta[0])]

        self._paquetes_por_entregar : list[Paquete] = [Paquete("hola" , self._ruta[6]), Paquete("bombas" , self._ruta[6]),
                                                       Paquete("celu" , self._ruta[3]) , Paquete("gun" , self._ruta[0])]
        self._cuantos_hay : function = lambda: len(self._paquetes_por_entregar)

        self.asignar_paquetes()

    def asignar_rutas(self):
        for index , ubi in enumerate(self._ruta):
            print(index)
            if ubi.id != 7:
                ubi.siguiente_ubi = self._ruta[index + 1]

            if ubi.id != 0:
                ubi.anterior_ubi = self._ruta[index - 1]

    def asignar_paquetes(self, dife = 0):
        print(f"hay {self._cuantos_hay() - dife} paquetes")

        for agente in self._activos:
            for paquete in self._paquetes_por_entregar[::-1]:

                agente.agregar_paquete(paquete)

    def iniciar_simulacion(self):
        i = 0
        while i < 60:

            for agente in self._activos:
                print(f"{agente.codigo} con ultimo destino: {agente.destino.donde}. esta en {agente.posicion_actual().donde} con cant paquetes {len(agente.inventario())}, su energia es {agente.energia}")
                agente.main()
                

                if agente.inventario() == []:
                    continue

            i += 1
        
        suma = 0
            
        for ubi in self._ruta:
            suma += ubi.cuantos_paquetes_entregados()
            print(f"Se han entregado {ubi.cuantos_paquetes_entregados()} en {ubi.donde}")
        
        print(f"paquetes restantes = {self._cuantos_hay() - suma}")
        if self._cuantos_hay() - suma != 0:
            print("reiniciando")
            self.asignar_paquetes(suma)
            self.iniciar_simulacion()
            return
        
        print("fin")
        


Mapa().iniciar_simulacion()