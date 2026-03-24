# thompson.py
from automata import Automata, EstadoTipo

class Thompson:
    @staticmethod
    def simbolo(c: str) -> Automata:
        a = Automata()
        inicio = a.agregar_estado(EstadoTipo.INICIAL)
        fin = a.agregar_estado(EstadoTipo.ACEPTACION)
        a.agregar_transicion(inicio, c, fin)
        return a

    @staticmethod
    def concatenacion(a: Automata, b: Automata) -> Automata:
        result = Automata()
        mapa_a = {}
        mapa_b = {}

        for i, tipo in enumerate(a.estados):
            nuevo = result.agregar_estado(tipo)
            mapa_a[i] = nuevo
        for t in a.transiciones:
            result.agregar_transicion(mapa_a[t.desde], t.simbolo, mapa_a[t.hacia])

        for i, tipo in enumerate(b.estados):
            nuevo = result.agregar_estado(tipo)
            mapa_b[i] = nuevo
        for t in b.transiciones:
            result.agregar_transicion(mapa_b[t.desde], t.simbolo, mapa_b[t.hacia])

        fin_a = mapa_a[a.get_estados_aceptacion()[0]]
        inicio_b = mapa_b[b.get_estado_inicial()]
        result.agregar_transicion(fin_a, '', inicio_b)

        fin_b = mapa_b[b.get_estados_aceptacion()[0]]
        result.marcar_aceptacion(fin_b)
        return result

    @staticmethod
    def union(a: Automata, b: Automata) -> Automata:
        result = Automata()
        nuevo_inicio = result.agregar_estado(EstadoTipo.INICIAL)

        mapa_a = {}
        mapa_b = {}

        for i, tipo in enumerate(a.estados):
            nuevo = result.agregar_estado(tipo)
            mapa_a[i] = nuevo
        for t in a.transiciones:
            result.agregar_transicion(mapa_a[t.desde], t.simbolo, mapa_a[t.hacia])

        for i, tipo in enumerate(b.estados):
            nuevo = result.agregar_estado(tipo)
            mapa_b[i] = nuevo
        for t in b.transiciones:
            result.agregar_transicion(mapa_b[t.desde], t.simbolo, mapa_b[t.hacia])

        inicio_a = mapa_a[a.get_estado_inicial()]
        inicio_b = mapa_b[b.get_estado_inicial()]
        result.agregar_transicion(nuevo_inicio, '', inicio_a)
        result.agregar_transicion(nuevo_inicio, '', inicio_b)

        nuevo_fin = result.agregar_estado(EstadoTipo.ACEPTACION)
        fin_a = mapa_a[a.get_estados_aceptacion()[0]]
        fin_b = mapa_b[b.get_estados_aceptacion()[0]]
        result.agregar_transicion(fin_a, '', nuevo_fin)
        result.agregar_transicion(fin_b, '', nuevo_fin)

        return result

    @staticmethod
    def estrella(a: Automata) -> Automata:
        result = Automata()
        nuevo_inicio = result.agregar_estado(EstadoTipo.INICIAL)
        nuevo_fin = result.agregar_estado(EstadoTipo.ACEPTACION)

        mapa_a = {}
        for i, tipo in enumerate(a.estados):
            nuevo = result.agregar_estado(tipo)
            mapa_a[i] = nuevo
        for t in a.transiciones:
            result.agregar_transicion(mapa_a[t.desde], t.simbolo, mapa_a[t.hacia])

        inicio_a = mapa_a[a.get_estado_inicial()]
        fin_a = mapa_a[a.get_estados_aceptacion()[0]]

        result.agregar_transicion(nuevo_inicio, '', inicio_a)
        result.agregar_transicion(nuevo_inicio, '', nuevo_fin)
        result.agregar_transicion(fin_a, '', inicio_a)
        result.agregar_transicion(fin_a, '', nuevo_fin)

        return result

    @staticmethod
    def una_o_mas(a: Automata) -> Automata:
        return Thompson.concatenacion(a, Thompson.estrella(a))