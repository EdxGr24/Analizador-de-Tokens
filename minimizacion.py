# minimizacion.py
from automata import Automata

class Minimizacion:
    @staticmethod
    def minimizar(afd: Automata) -> Automata:
        n = len(afd.estados)
        distinguishable = [[False] * n for _ in range(n)]

        aceptacion = set(afd.get_estados_aceptacion())

        for i in range(n):
            for j in range(i + 1, n):
                i_acept = i in aceptacion
                j_acept = j in aceptacion
                if i_acept != j_acept:
                    distinguishable[i][j] = distinguishable[j][i] = True

        cambio = True
        while cambio:
            cambio = False
            for i in range(n):
                for j in range(i + 1, n):
                    if not distinguishable[i][j]:
                        for simbolo in afd.alfabeto:
                            trans_i = None
                            trans_j = None
                            for t in afd.transiciones:
                                if t.desde == i and t.simbolo == simbolo:
                                    trans_i = t.hacia
                                if t.desde == j and t.simbolo == simbolo:
                                    trans_j = t.hacia
                            if trans_i is not None and trans_j is not None and trans_i != trans_j:
                                if distinguishable[trans_i][trans_j]:
                                    distinguishable[i][j] = distinguishable[j][i] = True
                                    cambio = True
                                    break

        representante = [-1] * n
        rep2nuevo = {}
        num_estados = 0
        for i in range(n):
            if representante[i] == -1:
                representante[i] = num_estados
                rep2nuevo[i] = num_estados
                num_estados += 1
                for j in range(i + 1, n):
                    if not distinguishable[i][j]:
                        representante[j] = representante[i]

        minimo = Automata()
        for _ in range(num_estados):
            minimo.agregar_estado()

        inicial_afd = afd.get_estado_inicial()
        minimo.marcar_inicial(representante[inicial_afd])

        for e in afd.get_estados_aceptacion():
            minimo.marcar_aceptacion(representante[e])

        transiciones_agregadas = set()
        for i in range(n):
            for t in afd.transiciones:
                if t.desde == i:
                    desde_nuevo = representante[t.desde]
                    hacia_nuevo = representante[t.hacia]
                    clave = (desde_nuevo, t.simbolo, hacia_nuevo)
                    if clave not in transiciones_agregadas:
                        minimo.agregar_transicion(desde_nuevo, t.simbolo, hacia_nuevo)
                        transiciones_agregadas.add(clave)

        return minimo