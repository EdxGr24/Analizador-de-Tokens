# automata.py
from enum import Enum
from typing import List, Set, Optional
from dataclasses import dataclass

class EstadoTipo(Enum):
    NORMAL = 1
    INICIAL = 2
    ACEPTACION = 3

@dataclass
class Transicion:
    desde: int
    simbolo: str  # '' para epsilon
    hacia: int

class Automata:
    def __init__(self):
        self.estados: List[EstadoTipo] = []
        self.transiciones: List[Transicion] = []
        self.alfabeto: Set[str] = set()

    def agregar_estado(self, tipo: EstadoTipo = EstadoTipo.NORMAL) -> int:
        self.estados.append(tipo)
        return len(self.estados) - 1

    def agregar_transicion(self, desde: int, simbolo: str, hacia: int):
        self.transiciones.append(Transicion(desde, simbolo, hacia))
        if simbolo != '':
            self.alfabeto.add(simbolo)

    def marcar_inicial(self, estado: int):
        if 0 <= estado < len(self.estados):
            self.estados[estado] = EstadoTipo.INICIAL

    def marcar_aceptacion(self, estado: int):
        if 0 <= estado < len(self.estados):
            self.estados[estado] = EstadoTipo.ACEPTACION

    def get_estado_inicial(self) -> Optional[int]:
        for i, tipo in enumerate(self.estados):
            if tipo == EstadoTipo.INICIAL:
                return i
        return None

    def get_estados_aceptacion(self) -> List[int]:
        return [i for i, tipo in enumerate(self.estados) if tipo == EstadoTipo.ACEPTACION]

    def get_transiciones_desde(self, estado: int) -> List[Transicion]:
        return [t for t in self.transiciones if t.desde == estado]

    def imprimir(self):
        print(f"Estados: {len(self.estados)}")
        print(f"Estado inicial: {self.get_estado_inicial()}")
        print(f"Estados de aceptación: {self.get_estados_aceptacion()}")
        print("Transiciones:")
        for t in self.transiciones:
            simbolo = 'ε' if t.simbolo == '' else t.simbolo
            print(f"  {t.desde} --{simbolo}--> {t.hacia}")