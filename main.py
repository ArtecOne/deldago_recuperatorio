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
    def id(self):
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
    def siguiente_ubi(self , ubi : "Ubicacion"):
        self._vecino_der = ubi
    
    @property
    def anterior_ubi(self) -> "Ubicacion":
        return self._vecino_izq
    
    @anterior_ubi.setter
    def anterior_ubi(self , ubi : "Ubicacion"):
        self._vecino_izq = ubi

    def dejar_paquete(self , paquete : "Paquete"):
        self._paquetes_entregados.append(paquete)

class Paquete:
    def __init__(self , codigo : str, destino : Ubicacion) -> None:
        
        self._asignado_a = None
        self._mi_codigo = codigo
        self._destino = destino
    
    @property
    def asignado(self):
        return self._asignado_a

    @property
    def codigo(self):
        return self._mi_codigo
    
    @property
    def destino(self):
        return self._destino
    
    def entregar(self):
        self._destino.dejar_paquete(self)


class Agente:
    def __init__(self , codigo : str, pos_actual : Ubicacion) -> None:

        self._mi_codigo : str = codigo
        self._energia : int = 50

        self._posicion : Ubicacion = pos_actual

        self._paquetes : list[Paquete] = []
    
    @property
    def codigo(self):
        return self._mi_codigo

    @property
    def energia(self):
        return self._energia
    
    def posicion_actual(self):
        return self._posicion
    
    def descansar(self):
        if self._posicion.es_plaza:
            self._energia += 5

    def avanzar(self):
        if self._posicion.siguiente_ubi != None:
            self._posicion = self._posicion.siguiente_ubi
            self._energia -= 10
            self.descansar()
    
    def retroceder(self):
        if self._posicion.anterior_ubi != None:
            self._posicion = self._posicion.anterior_ubi
            self._energia -= 10
            self.descansar()

        

    def inventario(self):
        return self._paquetes
    
    def agregar_paquete(self , paquete):
        if len(self._paquetes) < 4:
            self._paquetes.append(paquete)
            return True
        
        return False
    
    def entregar(self):
        if self._paquetes == []:
            return

        if self._posicion == self._paquetes[0].destino:
            print("entregaré")
            self._paquetes[0].entregar()
            self._paquetes.remove(self._paquetes[0])

    def main(self):
        if not self._paquetes == []:

            self.avanzar()

            self.entregar()

        else:

            self.retroceder()
            self.entregar()



class Mapa:
    def __init__(self) -> None:
        name_agentes = ["f33" , "A78" , "99971" , "Y22"]



        self._ruta : list[Ubicacion] = [Ubicacion("Central" , 0), Ubicacion("Plaza" , 1 , True),
                                        Ubicacion("Pilar" , 2 , ), Ubicacion("Savio" , 3),
                                        Ubicacion("Plaza" , 4 , True), Ubicacion("Escobar" , 5),
                                        Ubicacion("Tortuguitas" , 6) , Ubicacion("Plaza" , 7 , True)]
        self.asignar_rutas()

        self._activos : list[Agente] = [Agente(choice(name_agentes), self._ruta[0]) ]

        self._paquetes_por_entregar : list[Paquete] = [Paquete("hola" , self._ruta[6]) , Paquete("bombas" , self._ruta[1])]
        self._cuantos_hay : int = len(self._paquetes_por_entregar)

        self.asignar_paquetes()

    def asignar_rutas(self):
        for index , ubi in enumerate(self._ruta):
            print(index)
            if ubi.id != 7:
                ubi.siguiente_ubi = self._ruta[index + 1]

            if ubi.id != 0:
                ubi.anterior_ubi = self._ruta[index - 1]

    def asignar_paquetes(self):
        print(f"hay {self._cuantos_hay} paquetes")

        for agente in self._activos:
            for paquete in self._paquetes_por_entregar:

                agente.agregar_paquete(paquete)

    def iniciar_simulacion(self):
        i = 0
        while i < 60:

            for agente in self._activos:
                print(f"{agente.codigo} esta en {agente.posicion_actual().donde} con cant paquetes {len(agente.inventario())}")
                agente.main()
                

                if agente.inventario() == []:
                    continue

            

            i += 1
            


Mapa().iniciar_simulacion()