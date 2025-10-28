# 📖 Guía Rápida - Analizador Sintáctico

## 🎯 Flujo de Trabajo Recomendado

### 1️⃣ Cargar Gramática
Primero, ingresa o carga una gramática usando una de estas opciones:
- **Opción 1**: Formato del proyecto (con número de no-terminales)
- **Opción 2**: Formato libre (manual)
- **Opción 3**: Desde archivo (ejemplos predefinidos)

### 2️⃣ Calcular FIRST y FOLLOW
Usa la **Opción 4** para calcular los conjuntos FIRST y FOLLOW.
Esto es necesario para generar las tablas de análisis.

### 3️⃣ Generar Tabla de Análisis
Usa la **Opción 5** para generar:
- Parser LL(1)
- Parser SLR(1)
- Detección automática (recomendado)

### 4️⃣ Probar Cadenas
Usa la **Opción 6** para analizar cadenas de entrada.

---

## 📝 Formato de Entrada Proyecto

```
<número_de_no_terminales>
<nonterminal> -> <producción1> | <producción2> | ...
<nonterminal> -> <producción1> | <producción2> | ...
...
```

**Ejemplo:**
```
3
S -> A B
A -> a | ε
B -> b | ε
```

---

## 🎮 Ejemplo de Uso Completo

### Paso 1: Cargar gramática LL(1)
```
➤ Seleccione opción: 3
➤ Seleccione opción (1-3): 1
```

### Paso 2: Calcular FIRST y FOLLOW
```
➤ Seleccione opción: 4
```

### Paso 3: Generar tabla LL(1)
```
➤ Seleccione opción: 5
➤ Seleccione opción (1-3): 3  (Detectar automáticamente)
```

### Paso 4: Probar cadena
```
➤ Seleccione opción: 6
➤ Tokens: id + id * id
```

---

## 🔤 Símbolos Especiales

| Símbolo | Significado | Uso |
|---------|-------------|-----|
| `ε` | Epsilon (cadena vacía) | En producciones |
| `$` | Fin de cadena | Automático en el parser |
| `\|` | Alternativa (OR) | Separar producciones |
| `->` | Produce | Separar no-terminal de producciones |

---

## ✅ Ejemplos de Cadenas Válidas

### Para gramática LL(1) de expresiones:
- `id`
- `id + id`
- `id * id`
- `( id )`
- `id + id * id`
- `( id + id ) * id`

### Tokens comunes:
- `id` - identificador
- `num` - número
- `+` - suma
- `*` - multiplicación
- `(` - paréntesis izquierdo
- `)` - paréntesis derecho

---

## ⚠️ Errores Comunes

### Error: "No hay gramática cargada"
**Solución**: Primero carga una gramática (opciones 1, 2 o 3)

### Error: "Parser no ha sido inicializado"
**Solución**: Primero genera la tabla de análisis (opción 5)

### Error: "Gramática no es LL(1) ni SLR(1)"
**Solución**: La gramática tiene conflictos. Revisa las producciones.

---

## 📊 Diferencias LL(1) vs SLR(1)

| Característica | LL(1) | SLR(1) |
|----------------|-------|--------|
| **Dirección** | Top-Down | Bottom-Up |
| **Tipo** | Predictivo | Shift-Reduce |
| **Recursión** | No permite recursión izquierda | Permite recursión izquierda |
| **Potencia** | Menos potente | Más potente |
| **Ejemplo** | `E -> T E'` | `E -> E + T` |

---

## 🎓 Tips para el Proyecto

1. **Usa la opción 3** (detección automática) para saber qué parser funciona
2. **Guarda tus gramáticas** en archivos .txt en la carpeta `data/`
3. **Prueba con cadenas simples** primero antes de complejas
4. **Verifica FIRST y FOLLOW** antes de generar tablas
5. **Usa ejemplos predefinidos** para familiarizarte con el sistema

---

