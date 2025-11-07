from typing import Dict, List, Set #importamos datos para anotaciones de tipos de variables

class Grammar:
    def __init__(self, rules: Dict[str, List[str]] = None, start_symbol: str = None): #define el metodo constructor que recibe reglas y simbolo inicial
        self.rules = rules or {}
        self.start_symbol = start_symbol or (next(iter(self.rules)) if self.rules else None)
        self.non_terminals = set(self.rules.keys())
        self.terminals = set()
        self._extract_terminals()

    @classmethod
    def from_text(cls, text: str, start_symbol: str = None): #define un metodo de clase para crear una gramatica a partir de texto
        """
        Formato por línea:
        A -> aB | b
        """
        rules = {} #diccionario vacio para las reglas
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            left, right = line.split("->") #separa la linea en lado izquierdo y derecho
            left = left.strip()
            productions = [p.strip() for p in right.split("|")] #separa las producciones por |
            rules.setdefault(left, []).extend(productions) #agrega las producciones al diccionario de reglas
        g = cls(rules, start_symbol) #crea una instancia de la clase Grammar con las reglas y simbolo inicial
        return g

    @classmethod
    def from_file(cls, path: str, start_symbol: str = None): #define un metodo de clase para crear una gramatica a partir de un archivo
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_text(f.read(), start_symbol)

    def _extract_terminals(self): #metodo para extraer los simbolos terminales de la gramatica
        nts = set(self.rules.keys())
        for left, prods in self.rules.items(): #recorre cada produccion
            for p in prods:
                for sym in self._tokenize_prod(p):
                    if sym not in nts and sym != 'ε':
                        self.terminals.add(sym)

    @staticmethod
    def _tokenize_prod(prod: str):
        # asume símbolos separados por espacios
        # Si no hay espacios, trata cada caracter como un símbolo EXCEPTO secuencias conocidas
        if " " in prod:
            return [s for s in prod.split() if s]
        else:
            # Si la producción contiene símbolos compuestos conocidos (id, num, etc)
            # los preservamos
            result = []
            i = 0
            while i < len(prod):
                # Detectar tokens multicaracter comunes
                if i + 1 < len(prod) and prod[i:i+2] == 'id': # Detecta el token 'id'
                    result.append('id')
                    i += 2
                elif i + 2 < len(prod) and prod[i:i+3] == 'num':
                    result.append('num')
                    i += 3
                else:
                    if prod[i] != ' ':
                        result.append(prod[i])
                    i += 1
            return result #retorna la lista de simbolos tokenizados

    def display(self):    #muestra la gramatica en formato legible
        for left, prods in self.rules.items():
            print(f"{left} -> {' | '.join(prods)}")
        print("Start:", self.start_symbol)
        print("Non-terminals:", self.non_terminals)
        print("Terminals:", self.terminals)