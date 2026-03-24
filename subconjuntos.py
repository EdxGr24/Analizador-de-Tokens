# subconjuntos.py
from automata import Automata, EstadoTipo
from typing import Set, FrozenSet
from collections import deque

class Subconjuntos:
    @staticmethod
    def clausura_epsilon(afnd: Automata, estados: Set[int]) -> Set[int]:
        resultado = set(estados)
        cola = deque(estados)
        while cola:
            actual = cola.popleft()
            for t in afnd.get_transiciones_desde(actual):
                if t.simbolo == '' and t.hacia not in resultado:
                    resultado.add(t.hacia)
                    cola.append(t.hacia)
        return resultado

    @staticmethod
    def mover(afnd: Automata, estados: Set[int], simbolo: str) -> Set[int]:
        resultado = set()
        for e in estados:
            for t in afnd.get_transiciones_desde(e):
                if t.simbolo == simbolo:
                    resultado.add(t.hacia)
        return resultado

    @staticmethod
    def convertir(afnd: Automata) -> Automata:
        afd = Automata()
        inicial = {afnd.get_estado_inicial()}
        inicial_clausura = Subconjuntos.clausura_epsilon(afnd, inicial)

        conj2estado: dict[FrozenSet[int], int] = {}
        cola = deque()

        nuevo_estado = afd.agregar_estado()
        conj2estado[frozenset(inicial_clausura)] = nuevo_estado
        cola.append(inicial_clausura)

        aceptacion_afnd = set(afnd.get_estados_aceptacion())
        if inicial_clausura & aceptacion_afnd:
            afd.marcar_aceptacion(nuevo_estado)
        afd.marcar_inicial(nuevo_estado)

        while cola:
            actual = cola.popleft()
            estado_actual_afd = conj2estado[frozenset(actual)]

            for simbolo in afnd.alfabeto:
                movidos = Subconjuntos.mover(afnd, actual, simbolo)
                if not movidos:
                    continue
                clausura = Subconjuntos.clausura_epsilon(afnd, movidos)
                conjunto_congelado = frozenset(clausura)
                if conjunto_congelado not in conj2estado:
                    nuevo = afd.agregar_estado()
                    conj2estado[conjunto_congelado] = nuevo
                    cola.append(clausura)
                    if clausura & aceptacion_afnd:
                        afd.marcar_aceptacion(nuevo)
                afd.agregar_transicion(estado_actual_afd, simbolo, conj2estado[conjunto_congelado])

        return afd