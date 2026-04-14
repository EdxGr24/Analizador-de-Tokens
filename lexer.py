# lexer.py
from automata import Automata
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Token:
    tipo: str
    lexema: str
    linea: int

class Lexer:
    def __init__(self, afd_operadores: Automata, afd_identificadores: Automata):
        self.afd_operadores = afd_operadores
        self.afd_identificadores = afd_identificadores
        self.palabras_reservadas = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'printf', 'scanf', 'include'
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }

    def _es_digito(self, c: str) -> bool:
        return c.isdigit()

    def _es_letra(self, c: str) -> bool:
        return c.isalpha() or c == '_'

    def _simular_afd(self, afd: Automata, cadena: str) -> Tuple[bool, int]:
        """Simula un AFD con una cadena y retorna (aceptado, estado_final)"""
        estado_actual = afd.get_estado_inicial()
        if estado_actual is None:
            return False, -1
        for c in cadena:
            transicion_encontrada = False
            for t in afd.get_transiciones_desde(estado_actual):
                if t.simbolo == c:
                    estado_actual = t.hacia
                    transicion_encontrada = True
                    break
            if not transicion_encontrada:
                return False, -1
        aceptacion = set(afd.get_estados_aceptacion())
        return estado_actual in aceptacion, estado_actual

    def analizar(self, codigo: str) -> List[Token]:
        tokens = []
        i = 0
        n = len(codigo)
        linea = 1

        while i < n:
            c = codigo[i]

            # Espacios en blanco
            if c in ' \t':
                i += 1
                continue
            if c == '\n':
                linea += 1
                i += 1
                continue

            # --- Intentar operadores (máximo 2 caracteres) ---
            for long in [2, 1]:
                if i + long <= n:
                    posible = codigo[i:i+long]
                    aceptado, _ = self._simular_afd(self.afd_operadores, posible)
                    if aceptado:
                        tokens.append(Token('OPERADOR', posible, linea))
                        i += long
                        break
            else:
                # --- Si no es operador, puede ser identificador ---
                if self._es_letra(c):
                    inicio = i
                    while i < n and (self._es_letra(codigo[i]) or self._es_digito(codigo[i])):
                        i += 1
                    identificador = codigo[inicio:i]

                    # Convertir a cadena de clases: 'l' para letra/_, 'd' para dígito
                    clases = []
                    for ch in identificador:
                        if self._es_letra(ch):
                            clases.append('l')
                        elif self._es_digito(ch):
                            clases.append('d')
                        else:
                            # No debería ocurrir, pero por seguridad
                            break
                    cadena_clases = ''.join(clases)

                    aceptado, _ = self._simular_afd(self.afd_identificadores, cadena_clases)
                    if aceptado:
                        if identificador in self.palabras_reservadas:
                            tokens.append(Token('PALABRA_RESERVADA', identificador, linea))
                        else:
                            tokens.append(Token('IDENTIFICADOR', identificador, linea))
                    else:
                        tokens.append(Token('DESCONOCIDO', identificador, linea))
                    continue

                # --- Cualquier otro carácter (no operador, no letra) ---
                tokens.append(Token('OTRO', c, linea))
                i += 1

        return tokens
