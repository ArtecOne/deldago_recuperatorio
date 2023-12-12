from mapa import Mapa
from paquetes import Paquete , OrdenEntrega
from agente import Agente
from random import choice
import string

def generar_codigo(largo : int) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(choice(letters_and_digits) for i in range(largo))

class NuevaSimulacion:
    def __init__(self) -> "NuevaSimulacion":
        self._ordenes : list[OrdenEntrega] = []
        self._activos : list[Agente] = []
        self._mapa = Mapa()
        self._cant_vueltas = 1
    
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