# main.py
import sys
import os
from automata import Automata, EstadoTipo
from thompson import Thompson
from subconjuntos import Subconjuntos
from minimizacion import Minimizacion
from lexer import Lexer, Token

# --------------------------------------------------------------
# Construcción de AFND para operadores
# --------------------------------------------------------------
def construir_afnd_operadores() -> Automata:
    operadores = [
        "+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">=",
        "&&", "||", "!", "&", "|", "^", "~", "?", ":", ";", ",",
        "(", ")", "{", "}", "[", "]", "<<", ">>",
        "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="
    ]

    def operador_a_afnd(op: str) -> Automata:
        afnd = Thompson.simbolo(op[0])
        for ch in op[1:]:
            afnd = Thompson.concatenacion(afnd, Thompson.simbolo(ch))
        return afnd

    if not operadores:
        raise ValueError("No hay operadores definidos")

    afnd_total = operador_a_afnd(operadores[0])
    for op in operadores[1:]:
        afnd_total = Thompson.union(afnd_total, operador_a_afnd(op))
    return afnd_total

# --------------------------------------------------------------
# Construcción de AFND para identificadores (usando clases l y d)
# --------------------------------------------------------------
def construir_afnd_identificadores() -> Automata:
    letra = Thompson.simbolo('l')
    digito = Thompson.simbolo('d')
    letra_o_digito = Thompson.union(letra, digito)
    estrella = Thompson.estrella(letra_o_digito)
    return Thompson.concatenacion(letra, estrella)

# --------------------------------------------------------------
# Mostrar estadísticas
# --------------------------------------------------------------
def imprimir_automatas(nombre: str, afnd: Automata, afd: Automata, afd_min: Automata):
    print(f"\n--- {nombre} ---")
    print("AFND (Thompson):")
    print(f"  Estados: {len(afnd.estados)}")
    print(f"  Transiciones: {len(afnd.transiciones)}")
    print("\nAFD (Subconjuntos):")
    print(f"  Estados: {len(afd.estados)}")
    print(f"  Transiciones: {len(afd.transiciones)}")
    print("\nAFD Mínimo:")
    print(f"  Estados: {len(afd_min.estados)}")
    print(f"  Transiciones: {len(afd_min.transiciones)}")

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def main():
    print("=" * 60)
    print("    ANALIZADOR LÉXICO - OPERADORES Y PALABRAS RESERVADAS")
    print("=" * 60)

    # 1. Operadores
    print("\n1. Construyendo AFND para operadores...")
    afnd_op = construir_afnd_operadores()
    print(f"   ✓ AFND construido ({len(afnd_op.estados)} estados)")

    print("2. Convirtiendo a AFD (subconjuntos)...")
    afd_op = Subconjuntos.convertir(afnd_op)
    print(f"   ✓ AFD obtenido ({len(afd_op.estados)} estados)")

    print("3. Minimizando AFD...")
    afd_min_op = Minimizacion.minimizar(afd_op)
    print(f"   ✓ AFD mínimo obtenido ({len(afd_min_op.estados)} estados)")

    # 2. Identificadores
    print("\n4. Construyendo AFND para identificadores...")
    afnd_id = construir_afnd_identificadores()
    print(f"   ✓ AFND construido ({len(afnd_id.estados)} estados)")

    print("5. Convirtiendo a AFD...")
    afd_id = Subconjuntos.convertir(afnd_id)
    print(f"   ✓ AFD obtenido ({len(afd_id.estados)} estados)")

    print("6. Minimizando AFD...")
    afd_min_id = Minimizacion.minimizar(afd_id)
    print(f"   ✓ AFD mínimo obtenido ({len(afd_min_id.estados)} estados)")

    # 3. Estadísticas
    print("\n" + "=" * 60)
    print("          ESTADÍSTICAS DE LOS AUTÓMATAS")
    print("=" * 60)
    imprimir_automatas("OPERADORES", afnd_op, afd_op, afd_min_op)
    imprimir_automatas("IDENTIFICADORES", afnd_id, afd_id, afd_min_id)

    # 4. Crear lexer
    lexer = Lexer(afd_min_op, afd_min_id)

    # 5. Obtener archivo de entrada
    if len(sys.argv) >= 2:
        archivo = sys.argv[1]
    else:
        archivo = input("\nIngrese el nombre del archivo con código fuente: ").strip()

    if not os.path.exists(archivo):
        print(f"\n✗ Error: No se encontró el archivo '{archivo}'.")
        input("\nPresione Enter para salir...")
        return

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        print(f"\n✓ Archivo cargado: {archivo}")
    except Exception as e:
        print(f"\n✗ Error al leer el archivo: {e}")
        input("\nPresione Enter para salir...")
        return

    # 6. Analizar
    tokens = lexer.analizar(codigo)

    # 7. Filtrar solo OPERADOR y PALABRA_RESERVADA
    tokens_filtrados = [t for t in tokens if t.tipo in ('OPERADOR', 'PALABRA_RESERVADA')]

    print("\n" + "-" * 60)
    print("TOKENS IDENTIFICADOS (OPERADORES Y PALABRAS RESERVADAS):")
    print(f"{'Línea':<6} {'Tipo':<20} {'Lexema':<15}")
    print("-" * 60)
    for tok in tokens_filtrados:
        print(f"{tok.linea:<6} {tok.tipo:<20} {tok.lexema:<15}")
    print("-" * 60)
    print(f"Total de tokens (solo operadores y palabras reservadas): {len(tokens_filtrados)}")

    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()