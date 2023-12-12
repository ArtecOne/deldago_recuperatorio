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
    def entregado(self):
        return self._entregado
    
    def entregar(self):
        self._entregado = True
        
    def cuantos_hay(self) -> int:
        return len(self._paquetes)
    
    def paquetes(self) -> list[Paquete]:
        return self._paquetes
    
    def añadir_paquete(self , paquete : Paquete):
        paquete.asignado = self.asignado_a
        self._paquetes.append(paquete)