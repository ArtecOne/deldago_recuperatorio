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