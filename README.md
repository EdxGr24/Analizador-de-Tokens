¡Tienes razón, me faltó el final! Aquí está completo, sin cortes.

---

# Proyecto: Analizador Léxico con Construcción Formal de Autómatas

## 1. Introducción

Este proyecto implementa un **analizador léxico (scanner)** que, dado un código fuente, identifica dos tipos de tokens:

- **Operadores** (`+`, `-`, `=`, `==`, `+=`, etc.)
- **Palabras reservadas** (`int`, `if`, `return`, etc.)

La construcción del analizador sigue el proceso formal usado en los compiladores:

1. **Expresiones regulares** que describen los patrones de los tokens.
2. **Construcción de un AFND** (Autómata Finito No Determinista) mediante el algoritmo de **Thompson**.
3. **Conversión a AFD** (Autómata Finito Determinista) con el **algoritmo de subconjuntos**.
4. **Minimización del AFD** para obtener la versión más eficiente.
5. **Uso del AFD mínimo** para reconocer los tokens en el código fuente.

El programa está escrito en **Python** y no requiere bibliotecas externas (se ha eliminado la dependencia de Graphviz).

---

## 2. Proceso Teórico

### 2.1. Expresiones Regulares

Para los dos tipos de tokens se definen expresiones regulares:

- **Operadores**: se enumeran todos los operadores deseados y se expresan como la **unión** de cada uno.  
  Por ejemplo: `"+" | "-" | "*" | "=" | "==" | ...`

- **Identificadores** (que luego se clasifican como palabra reservada si pertenecen a un conjunto fijo):  
  `letra (letra | dígito)*`  
  donde `letra` = `[a-zA-Z_]` y `dígito` = `[0-9]`.

### 2.2. Construcción del AFND (Algoritmo de Thompson)

Thompson transforma una expresión regular en un AFND con transiciones ε. Las operaciones básicas son:

- **Símbolo** `c`: crea un autómata con un estado inicial, un estado final y una transición con `c`.
- **Concatenación** `a·b`: une el estado final de `a` con el inicial de `b` mediante una ε-transición.
- **Unión** `a|b`: crea un nuevo estado inicial que se conecta mediante ε a los inicios de `a` y `b`; los finales de `a` y `b` se conectan a un nuevo estado final.
- **Cerradura de Kleene** `a*`: se añaden ε-transiciones para permitir cero o más repeticiones.

Con estas operaciones se construye el AFND de cada token.

### 2.3. Conversión a AFD (Algoritmo de Subconjuntos)

El AFND se convierte en un AFD determinista. El algoritmo:

- Calcula la **clausura ε** del estado inicial.
- Para cada conjunto de estados y cada símbolo del alfabeto, calcula el conjunto alcanzable (mover + clausura ε).
- Cada conjunto único se convierte en un estado del AFD.
- Se repite hasta que no aparecen nuevos conjuntos.

### 2.4. Minimización del AFD

El AFD se minimiza usando el **algoritmo de llenado de tabla** (Hopcroft):

- Inicialmente se separan estados de aceptación de no aceptación.
- Se marcan pares de estados como distinguibles si sus transiciones con algún símbolo llevan a pares ya distinguibles.
- Al final, los estados no distinguibles se unen en un solo estado, obteniendo el AFD mínimo.

### 2.5. Analizador Léxico

El AFD mínimo se utiliza para reconocer tokens:

- Se recorre el código carácter a carácter.
- Se busca el prefijo más largo que sea aceptado por el AFD de operadores (se prueba primero longitud 2, luego 1).
- Si no es operador, se extrae un identificador (letra o _ seguida de letras/dígitos) y se simula en el AFD de identificadores usando una **cadena de clases** (`l` para letra, `d` para dígito) porque ese es el alfabeto con el que se construyó el autómata.
- Si el identificador está en la tabla de palabras reservadas, se emite `PALABRA_RESERVADA`; si no, `IDENTIFICADOR` (no se muestra en la salida final).
- Los demás caracteres se marcan como `OTRO` y no se muestran.

Finalmente, se filtran los tokens para mostrar solo los de tipo `OPERADOR` y `PALABRA_RESERVADA`, cumpliendo la consigna.

---

## 3. Estructura del Código (Archivos)

### 3.1. `automata.py`

Define las clases que representan un autómata finito:

- `EstadoTipo`: enum con los tipos de estado (NORMAL, INICIAL, ACEPTACION).
- `Transicion`: una tupla con (desde, símbolo, hacia).
- `Automata`: contiene listas de estados y transiciones, y métodos para agregar estados/transiciones, marcar inicial/aceptación, consultar estado inicial, aceptación, transiciones desde un estado, etc.

### 3.2. `thompson.py`

Implementa el **algoritmo de Thompson** para construir AFND a partir de expresiones regulares.  
Métodos estáticos:

- `simbolo(c)`: crea un AFND para un símbolo `c`.
- `concatenacion(a, b)`: une dos AFND en secuencia.
- `union(a, b)`: crea un AFND para `a|b`.
- `estrella(a)`: crea un AFND para `a*`.
- `una_o_mas(a)`: para `a+` (equivalente a `a·a*`).

### 3.3. `subconjuntos.py`

Contiene el **algoritmo de subconjuntos** para convertir AFND en AFD:

- `clausura_epsilon(afnd, estados)`: calcula el conjunto de estados alcanzables mediante ε-transiciones.
- `mover(afnd, estados, simbolo)`: conjunto de estados alcanzables con un símbolo.
- `convertir(afnd)`: realiza la conversión y devuelve un AFD.

### 3.4. `minimizacion.py`

Implementa la **minimización de AFD**:

- `minimizar(afd)`: aplica el algoritmo de llenado de tabla y devuelve un AFD mínimo.

### 3.5. `lexer.py`

Define la clase `Lexer` que usa los AFDs mínimos para analizar el código fuente:

- Constructor recibe los AFDs mínimos de operadores e identificadores.
- `_simular_afd(afd, cadena)`: simula un AFD con una cadena y retorna si es aceptada.
- `analizar(codigo)`: recorre el código, identifica tokens y los almacena en una lista de objetos `Token`.

**Importante**: para reconocer identificadores, primero se convierte la cadena a una secuencia de clases (`'l'`/`'d'`) y luego se simula el AFD con esa cadena. Esto es necesario porque el AFD fue construido con el alfabeto `{l, d}`.

### 3.6. `main.py`

Es el programa principal:

1. Construye los AFND de operadores e identificadores usando las funciones `construir_afnd_operadores()` y `construir_afnd_identificadores()`.
2. Convierte cada AFND en AFD (subconjuntos) y luego minimiza.
3. Imprime estadísticas de cada autómata.
4. Crea una instancia de `Lexer` con los AFDs mínimos.
5. Solicita el nombre del archivo con código fuente (o lo toma como argumento de línea de comandos).
6. Lee el archivo, analiza y filtra los tokens.
7. Muestra en pantalla los tokens de tipo `OPERADOR` y `PALABRA_RESERVADA`.
8. Espera una tecla para cerrar (útil cuando se ejecuta con doble clic).

---

## 4. Prueba de Escritorio (Desk Test)

Vamos a simular la ejecución sobre un pequeño fragmento de código:

**Código fuente** (`prueba.txt`):
```c
int a = 5;
```

**Proceso paso a paso**:

### 4.1. Construcción de los autómatas (previo al análisis)

- **AFD mínimo para operadores**: reconoce todos los operadores de la lista (en este caso, `=`, `;`, etc.).
- **AFD mínimo para identificadores**: reconoce cadenas de la forma `l(l|d)*` (en clases). Acepta, por ejemplo, la cadena de clases `"lll"` para `"int"`.

### 4.2. Análisis línea por línea

**Línea 1:**
Caracteres: `i`, `n`, `t`, espacio, `a`, espacio, `=`, espacio, `5`, `;`, fin de línea.

1. **Posición 0**: `i` (letra). No es operador (se prueba "i" como posible operador de longitud 1, no está en la lista de operadores).  
   Se inicia extracción de identificador: se lee mientras sea letra o dígito → `"int"`.  
   Se convierte a clases: `"i"` → `'l'`, `"n"` → `'l'`, `"t"` → `'l'` → cadena `"lll"`.  
   Se simula en el AFD de identificadores: la cadena `"lll"` es aceptada.  
   Se comprueba si `"int"` está en palabras reservadas → sí.  
   Se añade token: `("PALABRA_RESERVADA", "int", 1)`.

2. **Posición 3**: carácter espacio → se ignora.

3. **Posición 4**: `a` (letra). Se extrae identificador `"a"`. Clases: `"l"`. Aceptado. No es palabra reservada → se añade `IDENTIFICADOR` (pero no se mostrará en la salida final porque filtramos solo operadores y reservadas).

4. **Posición 5**: espacio → ignora.

5. **Posición 6**: `=` (operador). Se prueba longitud 2: `"= "` no es operador (contiene espacio). Longitud 1: `"="` sí es operador. Se añade `("OPERADOR", "=", 1)`. Avanza 1.

6. **Posición 7**: espacio → ignora.

7. **Posición 8**: `5` (dígito). No es letra, no es operador (probamos longitud 2: `"5;"` no está en operadores; longitud 1: `"5"` no es operador). Como no es letra, se trata como `OTRO`. No se muestra en la salida final.

8. **Posición 9**: `;` (operador). Longitud 1: `";"` es operador. Añadir `("OPERADOR", ";", 1)`.

9. **Posición 10**: salto de línea → incrementa línea.

**Línea 2:** (vacía, solo fin de archivo)

### 4.3. Tokens resultantes (filtrados)

- `("PALABRA_RESERVADA", "int", 1)`
- `("OPERADOR", "=", 1)`
- `("OPERADOR", ";", 1)`

Esto coincide con la salida esperada.

---

## 5. Conclusión

El proyecto implementa completamente un analizador léxico siguiendo los fundamentos teóricos de los compiladores. Se han aplicado los algoritmos de Thompson, subconjuntos y minimización para construir autómatas óptimos que reconocen operadores y palabras reservadas. El código está modularizado, es fácil de entender y puede extenderse para incluir más tipos de tokens o soportar otros lenguajes.

---

## 6. Instrucciones de Ejecución

1. Guardar todos los archivos en una misma carpeta.
2. Crear un archivo de código fuente (por ejemplo `codigo.txt`) con el contenido a analizar.
3. Ejecutar `main.py`:
   - En terminal: `python main.py codigo.txt`
   - O con doble clic: luego ingresar el nombre del archivo cuando se solicite.
4. Ver la salida en pantalla con los tokens de operadores y palabras reservadas.

¡El programa está listo para usar!

---

Ahora sí está completo. Puedes copiar este contenido en un archivo con extensión `.md` y usarlo como documentación.