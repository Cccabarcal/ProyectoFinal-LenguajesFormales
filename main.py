from grammar.grammar_module import Grammar
from grammar.first_follow import FirstFollow
from grammar.ll1_parser import LL1Parser
from grammar.slr1_parser import SLR1Parser
from ai_assistant.neural_interface import NeuralInterface
import os


class AnalizadorSintactico:
    def __init__(self):
        self.grammar = None
        self.first_follow = None
        self.ll1_parser = None
        self.slr1_parser = None
        self.parser_type = None  # 'll1' o 'slr1'

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        print("\n" + "="*50)
        print("   🎯 ANALIZADOR SINTÁCTICO - Proyecto Final")
        print("="*50)
        print("1. Ingresar gramática (Formato Proyecto)")
        print("2. Ingresar gramática manualmente (Libre)")
        print("3. Cargar gramática desde archivo")
        print("4. Calcular FIRST y FOLLOW")
        print("5. Generar tabla de análisis sintáctico")
        print("6. Probar análisis de cadena")
        print("7. Ver gramática actual")
        print("8. Asistente IA del Curso")
        print("9. Salir")
        print("="*50)

    def ingresar_gramatica_proyecto(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📝 INGRESAR GRAMÁTICA (Formato Proyecto)")
        print("="*50)
        print("\n📌 Formato requerido:")
        print("   - Primera línea: número n de no-terminales")
        print("   - Siguientes n líneas: <nonterminal> -> <producciones separadas por espacios>")
        print("   - Use 'ε' para epsilon")
        print("   - Use '#' para end of string\n")
        print("Ejemplo:")
        print("   3")
        print("   S -> A B")
        print("   A -> a | ε")
        print("   B -> b\n")
        
        try:
            n = int(input("📊 Ingrese el número de no-terminales: ").strip())
            
            if n <= 0:
                print("❌ El número debe ser positivo.")
                input("\nPresione Enter para continuar...")
                return
            
            print(f"\n📝 Ingrese {n} producciones:\n")
            reglas = []
            for i in range(n):
                linea = input(f"  {i+1}. ").strip()
                if not linea:
                    print("❌ Línea vacía no permitida.")
                    input("\nPresione Enter para continuar...")
                    return
                reglas.append(linea)
            
            gramatica_texto = "\n".join(reglas)
            
            # Extraer el símbolo inicial (primer no-terminal)
            primera_regla = reglas[0].split("->")[0].strip()
            
            self.grammar = Grammar.from_text(gramatica_texto, start_symbol=primera_regla)
            self.first_follow = None
            self.ll1_parser = None
            self.slr1_parser = None
            print("\n✅ Gramática cargada exitosamente!")
            self.mostrar_gramatica()
        except ValueError:
            print("\n❌ Error: Debe ingresar un número válido.")
        except Exception as e:
            print(f"\n❌ Error al cargar gramática: {e}")
        
        input("\nPresione Enter para continuar...")

    def ingresar_gramatica_manual(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📝 INGRESAR GRAMÁTICA MANUALMENTE (Libre)")
        print("="*50)
        print("\nFormato: A -> B C | D")
        print("Use 'ε' para epsilon (cadena vacía)")
        print("Ingrese cada regla (línea vacía para terminar):\n")
        
        reglas = []
        while True:
            linea = input("➤ ")
            if not linea.strip():
                break
            reglas.append(linea)
        
        if not reglas:
            print("❌ No se ingresaron reglas.")
            input("\nPresione Enter para continuar...")
            return
        
        gramatica_texto = "\n".join(reglas)
        simbolo_inicio = input("\n🎯 Ingrese el símbolo inicial (Enter para usar el primero): ").strip()
        
        try:
            self.grammar = Grammar.from_text(gramatica_texto, start_symbol=simbolo_inicio or None)
            self.first_follow = None
            self.ll1_parser = None
            self.slr1_parser = None
            print("\n✅ Gramática cargada exitosamente!")
            self.mostrar_gramatica()
        except Exception as e:
            print(f"\n❌ Error al cargar gramática: {e}")
        
        input("\nPresione Enter para continuar...")

    def cargar_gramatica_archivo(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📂 CARGAR GRAMÁTICA DESDE ARCHIVO")
        print("="*50)
        
        print("\n¿Qué tipo de gramática desea cargar?")
        print("1. LL(1) - Gramática predictiva (data/Sample_ll1.txt)")
        print("2. SLR(1) - Gramática ascendente (data/Sample_slr1.txt)")
        
        
        opcion = input("\n➤ Seleccione una opción (1-2): ").strip()
        
        if opcion == "1":
            archivo = "data/Sample_ll1.txt"
            simbolo_inicio = "E"
        elif opcion == "2":
            archivo = "data/Sample_slr1.txt"
            simbolo_inicio = "E"
        else:
            print("\n❌ Opción no válida.")
            input("\nPresione Enter para continuar...")
            return
        
        if not os.path.exists(archivo):
            print(f"\n❌ El archivo '{archivo}' no existe.")
            input("\nPresione Enter para continuar...")
            return
        
        try:
            self.grammar = Grammar.from_file(archivo, start_symbol=simbolo_inicio or None)
            self.first_follow = None
            self.ll1_parser = None
            self.slr1_parser = None
            print("\n✅ Gramática cargada exitosamente desde archivo!")
            self.mostrar_gramatica()
        except Exception as e:
            print(f"\n❌ Error al cargar gramática: {e}")
        
        input("\nPresione Enter para continuar...")

    def calcular_first_follow(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   🔍 CALCULAR FIRST Y FOLLOW")
        print("="*50)
        
        if not self.grammar:
            print("\n❌ Primero debe cargar una gramática.")
            input("\nPresione Enter para continuar...")
            return
        
        # Mostrar gramática usada
        print("\n📋 Gramática usada:")
        print("-"*50)
        self.grammar.display()
        print("-"*50)
        
        try:
            self.first_follow = FirstFollow(self.grammar)
            self.first_follow.compute_all_first()
            self.first_follow.compute_all_follow()
            
            print("\n✅ Conjuntos FIRST y FOLLOW calculados:\n")
            self.first_follow.display()
            
        except Exception as e:
            print(f"\n❌ Error al calcular FIRST y FOLLOW: {e}")
        
        input("\nPresione Enter para continuar...")

    def generar_tabla_parser(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📊 GENERAR TABLA DE ANÁLISIS SINTÁCTICO")
        print("="*50)
        
        if not self.grammar:
            print("\n❌ Primero debe cargar una gramática.")
            input("\nPresione Enter para continuar...")
            return
        
        # Mostrar gramática usada
        print("\n📋 Gramática usada:")
        print("-"*50)
        self.grammar.display()
        print("-"*50)
        
        if not self.first_follow:
            print("\n⚠️  Calculando FIRST y FOLLOW primero...")
            self.first_follow = FirstFollow(self.grammar)
            self.first_follow.compute_all_first()
            self.first_follow.compute_all_follow()
        
        print("\n¿Qué tipo de parser desea generar?")
        print("1. LL(1) - Análisis predictivo descendente")
        print("2. SLR(1) - Análisis ascendente simple")
        print("3. Ambos (Detectar automáticamente)")
        
        opcion = input("\n➤ Seleccione una opción (1-3): ").strip()
        
        try:
            if opcion == "1":
                self.parser_type = 'll1'
                self.ll1_parser = LL1Parser(self.grammar, self.first_follow)
                self.ll1_parser.build_table()
                print("\n✅ Tabla LL(1) generada exitosamente!\n")
                self.ll1_parser.display_table()
                
            elif opcion == "2":
                self.parser_type = 'slr1'
                self.slr1_parser = SLR1Parser(self.grammar, self.first_follow)
                print("\n⏳ Construyendo autómata LR(0)...")
                self.slr1_parser.build_lr0_automaton()
                print("⏳ Construyendo tablas SLR(1)...")
                self.slr1_parser.build_slr_tables()
                print("\n✅ Tablas SLR(1) generadas exitosamente!\n")
                self.slr1_parser.display_tables()
                
            elif opcion == "3":
                print("\n🔍 Analizando gramática para ambos parsers...\n")
                
                # Intentar LL(1)
                ll1_valido = False
                try:
                    self.ll1_parser = LL1Parser(self.grammar, self.first_follow)
                    self.ll1_parser.build_table()
                    ll1_valido = True
                    print("✅ La gramática es LL(1)")
                    print("-"*50)
                    self.ll1_parser.display_table()
                except Exception as e:
                    print(f"❌ La gramática NO es LL(1): {e}")
                
                print("\n")
                
                # Intentar SLR(1)
                slr1_valido = False
                try:
                    self.slr1_parser = SLR1Parser(self.grammar, self.first_follow)
                    self.slr1_parser.build_lr0_automaton()
                    self.slr1_parser.build_slr_tables()
                    slr1_valido = True
                    print("✅ La gramática es SLR(1)")
                    print("-"*50)
                    self.slr1_parser.display_tables()
                except Exception as e:
                    print(f"❌ La gramática NO es SLR(1): {e}")
                
                # Establecer el parser por defecto
                if ll1_valido:
                    self.parser_type = 'll1'
                elif slr1_valido:
                    self.parser_type = 'slr1'
                else:
                    self.parser_type = None
                    print("\n⚠️  Esta gramática no es ni LL(1) ni SLR(1)")
                
            else:
                print("\n❌ Opción no válida.")
                
        except Exception as e:
            print(f"\n❌ Error al generar tabla: {e}")
        
        input("\nPresione Enter para continuar...")

    def probar_cadena(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   🧪 PROBAR ANÁLISIS DE CADENA")
        print("="*50)
        
        if not self.grammar:
            print("\n❌ Primero debe cargar una gramática.")
            input("\nPresione Enter para continuar...")
            return
        
        if not self.parser_type:
            print("\n❌ Primero debe generar una tabla de parser.")
            input("\nPresione Enter para continuar...")
            return
        
        # Mostrar gramática usada
        print("\n📋 Gramática usada:")
        print("-"*50)
        self.grammar.display()
        print("-"*50)
        
        print(f"\n📌 Parser activo: {self.parser_type.upper()}")
        
        # Mostrar tokens disponibles dinámicamente
        tokens_disponibles = sorted(list(self.grammar.terminals))
        if tokens_disponibles:
            print(f"\n🔤 Tokens disponibles: {', '.join(tokens_disponibles)}")
            
            # Generar ejemplo dinámico
            if len(tokens_disponibles) >= 2:
                ejemplo = ' '.join(tokens_disponibles[:3] if len(tokens_disponibles) >= 3 else tokens_disponibles[:2])
            else:
                ejemplo = tokens_disponibles[0] if tokens_disponibles else "token"
        else:
            ejemplo = "token"
        
        print("\nIngrese los tokens separados por espacios.")
        print(f"Ejemplo: {ejemplo}")
        print("(El símbolo $ se agregará automáticamente)\n")
        
        entrada = input("➤ Tokens: ").strip()
        
        if not entrada:
            print("\n❌ No se ingresaron tokens.")
            input("\nPresione Enter para continuar...")
            return
        
        tokens = entrada.split()
        
        try:
            print(f"\n🔄 Analizando cadena: {' '.join(tokens)}")
            print("-"*50)
            
            if self.parser_type == 'll1':
                if not self.ll1_parser:
                    print("\n❌ Parser LL(1) no ha sido inicializado.")
                    input("\nPresione Enter para continuar...")
                    return
                
                resultado, traza = self.ll1_parser.parse(tokens)
                
                if resultado:
                    print("\n" + "="*50)
                    print("   ✅ CADENA ACEPTADA")
                    print("="*50)
                    if traza:
                        print("\n📜 Derivaciones:")
                        for i, (nt, prod) in enumerate(traza, 1):
                            print(f"  {i}. {nt} → {prod}")
                else:
                    print("\n" + "="*50)
                    print("   ❌ CADENA RECHAZADA")
                    print("="*50)
                    
            elif self.parser_type == 'slr1':
                if not self.slr1_parser:
                    print("\n❌ Parser SLR(1) no ha sido inicializado.")
                    input("\nPresione Enter para continuar...")
                    return
                
                print()
                resultado = self.slr1_parser.parse(tokens)
                
                if not resultado:
                    print("\n" + "="*50)
                    print("   ❌ CADENA RECHAZADA")
                    print("="*50)
                    
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
        
        input("\nPresione Enter para continuar...")

    def mostrar_gramatica(self):
        if not self.grammar:
            return
        
        print("\n" + "-"*50)
        print("📋 GRAMÁTICA ACTUAL:")
        print("-"*50)
        self.grammar.display()
        print("-"*50)

    def ver_gramatica_actual(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📋 GRAMÁTICA ACTUAL")
        print("="*50)
        
        if not self.grammar:
            print("\n❌ No hay gramática cargada.")
        else:
            self.mostrar_gramatica()
            
            if self.first_follow:
                print("\n✓ FIRST y FOLLOW: Calculados")
            else:
                print("\n✗ FIRST y FOLLOW: No calculados")
                
            if self.parser_type:
                print(f"✓ Parser: {self.parser_type.upper()} generado")
            else:
                print("✗ Parser: No generado")
        
        input("\nPresione Enter para continuar...")

    def mostrar_ejemplos(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("   📚 EJEMPLOS DE GRAMÁTICAS")
        print("="*50)
        
        print("\n1. Gramática LL(1) - Expresiones Aritméticas")
        print("-"*50)
        ejemplo_ll1 = """E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id"""
        print(ejemplo_ll1)
        
        print("\n\n2. Gramática SLR(1) - Expresiones Aritméticas")
        print("-"*50)
        ejemplo_slr1 = """E -> E + T | T
T -> T * F | F
F -> ( E ) | id"""
        print(ejemplo_slr1)
        
        print("\n\n3. Gramática LL(1) - Declaraciones simples")
        print("-"*50)
        ejemplo_ll1_2 = """S -> D ;
D -> T id
T -> int | float"""
        print(ejemplo_ll1_2)
        
        print("\n" + "="*50)
        print("\n¿Desea cargar alguno de estos ejemplos?")
        print("1. Ejemplo 1 (LL1)")
        print("2. Ejemplo 2 (SLR1)")
        print("3. Ejemplo 3 (LL1)")
        print("4. Volver al menú principal")
        
        opcion = input("\n➤ Seleccione una opción: ").strip()
        
        try:
            if opcion == "1":
                self.grammar = Grammar.from_text(ejemplo_ll1, start_symbol="E")
                self.first_follow = None
                self.ll1_parser = None
                self.slr1_parser = None
                print("\n✅ Ejemplo 1 cargado exitosamente!")
                input("\nPresione Enter para continuar...")
            elif opcion == "2":
                self.grammar = Grammar.from_text(ejemplo_slr1, start_symbol="E")
                self.first_follow = None
                self.ll1_parser = None
                self.slr1_parser = None
                print("\n✅ Ejemplo 2 cargado exitosamente!")
                input("\nPresione Enter para continuar...")
            elif opcion == "3":
                self.grammar = Grammar.from_text(ejemplo_ll1_2, start_symbol="S")
                self.first_follow = None
                self.ll1_parser = None
                self.slr1_parser = None
                print("\n✅ Ejemplo 3 cargado exitosamente!")
                input("\nPresione Enter para continuar...")
        except Exception as e:
            print(f"\n❌ Error al cargar ejemplo: {e}")
            input("\nPresione Enter para continuar...")

    def asistente_ia(self):
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("    Asistente IA del Curso")
        print("="*50)
        print("\n💡 Pregúntame sobre lo que necesites acerca del curso:")
        print("   - Lenguajes formales")
        print("   - Gramáticas (LL1, SLR1)")
        print("   - FIRST y FOLLOW")
        print("   - Autómatas y compiladores")
        print("   - Información del profesor y curso etc")
        print("\n📝 Escribe 'salir' para volver al menú principal")
        print("📝 Escribe 'limpiar' para borrar el historial")
        print("="*50)
        
        # Inicializar el asistente
        print("\n⏳ Iniciando asistente IA...")
        ai = NeuralInterface()
        
        # Verificar si Ollama está corriendo
        if not ai.check_ollama_status():
            print("\n❌ Error: No se pudo conectar con el servicio de Ollama.")
            input("\nPresione Enter para continuar...")
            return
        
        print("✅ Asistente IA listo!\n")
        
        # Loop de conversación
        while True:
            try:
                pregunta = input("\n🧑 Tú: ").strip()
                
                if not pregunta:
                    continue
                
                if pregunta.lower() == 'salir':
                    print("\n👋 ¡Hasta pronto!")
                    input("\nPresione Enter para continuar...")
                    break
                
                if pregunta.lower() == 'limpiar':
                    ai.clear_history()
                    print("✅ Historial limpiado")
                    continue
                
                # Obtener respuesta del asistente
                print("\n Asistente: ", end="", flush=True)
                respuesta = ai.chat(pregunta)
                print(respuesta)
                
            except KeyboardInterrupt:
                print("\n\n👋 Saliendo del asistente...")
                input("\nPresione Enter para continuar...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue


    def ejecutar(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu_principal()
            
            opcion = input("\n➤ Seleccione una opción (1-9): ").strip()
            
            if opcion == "1":
                self.ingresar_gramatica_proyecto()
            elif opcion == "2":
                self.ingresar_gramatica_manual()
            elif opcion == "3":
                self.cargar_gramatica_archivo()
            elif opcion == "4":
                self.calcular_first_follow()
            elif opcion == "5":
                self.generar_tabla_parser()
            elif opcion == "6":
                self.probar_cadena()
            elif opcion == "7":
                self.ver_gramatica_actual()
            elif opcion == "8":
                self.asistente_ia()
            elif opcion == "9":
                self.limpiar_pantalla()
                print("\n" + "="*50)
                print("   👋 ¡Gracias por usar el Analizador Sintáctico!")
                print("="*50)
                print()
                break
            else:
                print("\n❌ Opción no válida. Intente de nuevo.")
                input("\nPresione Enter para continuar...")


def main():
    analizador = AnalizadorSintactico()
    analizador.ejecutar()


if __name__ == "__main__":
    main()
