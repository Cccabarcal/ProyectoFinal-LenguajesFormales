# ProyectoFinal-LenguajesFormales

## 📚 Analizador Sintáctico - Proyecto Final

Implementación de algoritmos para análisis sintáctico con parsers **LL(1)** y **SLR(1)**.

### 🎯 Características

- ✅ Cálculo de conjuntos **FIRST** y **FOLLOW**
- ✅ Parser **LL(1)** (Top-Down / Predictivo Descendente)
- ✅ Parser **SLR(1)** (Bottom-Up / Ascendente Simple)
- ✅ Interfaz de consola interactiva
- ✅ Múltiples formatos de entrada
- ✅ Ejemplos predefinidos

### 🚀 Instalación y Ejecución

```bash
# Clonar el repositorio
git clone https://github.com/Cccabarcal/ProyectoFinal-LenguajesFormales.git
cd ProyectoFinal-LenguajesFormales

# Ejecutar el programa
python main.py
```

### 📝 Formato de Entrada (Proyecto)

El formato oficial del proyecto requiere:

1. Primera línea: número `n` de no-terminales
2. Siguientes `n` líneas: producciones en formato `<nonterminal> -> <derivaciones>`

**Ejemplo:**
```
5
S -> A B
A -> a A | ε
B -> b B | ε
```

### 🎮 Uso del Menú Interactivo

```
🎯 ANALIZADOR SINTÁCTICO - Proyecto Final
==================================================
1. Ingresar gramática (Formato Proyecto)
2. Ingresar gramática manualmente (Libre)
3. Cargar gramática desde archivo
4. Calcular FIRST y FOLLOW
5. Generar tabla de análisis sintáctico
6. Probar análisis de cadena
7. Ver gramática actual
8. Ejemplos de gramáticas
9. Salir
==================================================
```

### 📂 Estructura del Proyecto

```
ProyectoFinal-LenguajesFormales/
│
├── main.py                    # Programa principal con menú interactivo
├── grammar/
│   ├── grammar_module.py      # Clase Grammar para manejo de gramáticas
│   ├── first_follow.py        # Algoritmos FIRST y FOLLOW
│   ├── ll1_parser.py          # Implementación del parser LL(1)
│   └── slr1_parser.py         # Implementación del parser SLR(1)
├── data/
│   ├── Sample_ll1.txt         # Ejemplo de gramática LL(1)
│   └── Sample_slr1.txt        # Ejemplo de gramática SLR(1)
└── README.md
```

### 📖 Ejemplos de Gramáticas

#### Gramática LL(1) - Expresiones Aritméticas
```
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id
```

**Cadenas válidas:** `id`, `id + id`, `id * id + id`, `( id + id ) * id`

#### Gramática SLR(1) - Expresiones Aritméticas
```
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

**Cadenas válidas:** `id`, `id + id`, `id * id`, `id + id * id`

### 🔧 Funcionalidades

#### 1. Calcular FIRST y FOLLOW
Calcula los conjuntos FIRST y FOLLOW para todos los no-terminales de la gramática.

#### 2. Generar Tablas de Análisis
- **LL(1)**: Genera tabla de análisis predictivo
- **SLR(1)**: Genera tablas ACTION y GOTO
- **Detección automática**: Verifica si la gramática es LL(1) o SLR(1)

#### 3. Análisis de Cadenas
Prueba si una cadena de entrada es aceptada por la gramática usando el parser seleccionado.

### 📌 Notas Importantes

- Use `ε` para representar epsilon (cadena vacía)
- Use `$` para el símbolo de fin de cadena
- Los no-terminales se representan con letras mayúsculas
- Los terminales se representan con letras minúsculas o símbolos

### 👥 Autores

Proyecto Final - Lenguajes Formales  
EAFIT University - 2025

### 📄 Licencia

Este proyecto es parte de un trabajo académico para el curso de Lenguajes Formales.
