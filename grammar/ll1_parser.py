from typing import Dict, Tuple #importamos datos para anotaciones de tipos de variables
from .grammar_module import Grammar
from .first_follow import FirstFollow, EPS, END

class LL1Parser:
    def __init__(self, grammar: Grammar, ff: FirstFollow):
        self.G = grammar
        self.ff = ff
        self.table: Dict[Tuple[str,str], str] = {}  # (nonterminal, terminal) -> production

    def build_table(self): #construye la tabla LL(1) usando los conjuntos first y follow
        self.table.clear()
        for A in self.G.non_terminals: #recorre cada no terminal A y cada produccion prdo asociada
            for prod in self.G.rules.get(A, []):
                symbols = self.G._tokenize_prod(prod)
                # compute FIRST(prod)
                first_of_prod = set() #conjunto vacio para el first de la produccion
                if prod == EPS: #si la produccion es epsilon agrega epsilon al first de la produccion
                    first_of_prod.add(EPS)
                else:
                    i = 0
                    while i < len(symbols):
                        X = symbols[i]
                        if X in self.G.terminals: #si X es un terminal se agrega al first de la produccion y se sale del while
                            first_of_prod.add(X); break
                        else: # X es no terminal
                            first_of_prod.update(x for x in self.ff.first[X] if x != EPS)
                            if EPS in self.ff.first[X]:
                                i += 1
                                if i == len(symbols):
                                    first_of_prod.add(EPS)
                                continue
                            else:
                                break
                for a in (first_of_prod - {EPS}): #para cada terminal en el first de la produccion sin epsilon, agrega la produccion a la tabla LL(1)
                    self.table[(A,a)] = prod
                if EPS in first_of_prod: #si epsilon esta en el first de la produccion, agrega la produccion a la tabla LL(1) para cada terminal en el follow de A
                    for b in self.ff.follow[A]:
                        self.table[(A,b)] = prod

    def parse(self, tokens: list): #parsea una lista de tokens usando la tabla LL(1)
        
        tokens = tokens + [END] if tokens[-1] != END else tokens
        stack = ['$', self.G.start_symbol] #inicializa la pila con el simbolo de fin de pila y el simbolo inicial
        ip = 0
        a = tokens[ip]
        output = []
        while stack: #mientras la pila no este vacia, procesa el simbolo en la cima de la pila
            top = stack.pop()
            if top == '$' and a == END:
                return True, output
            if top in self.G.terminals or top == END or top == '$': #si el simbolo en la cima es un terminal o simbolo de fin de cadena
                if top == a:
                    ip += 1
                    a = tokens[ip]
                    continue
                else:
                    return False, output
            else:
                prod = self.table.get((top, a)) #si el simbolo en la cima es un no terminal busca la produccion en la tabla LL(1)
                if not prod:
                    return False, output
                output.append((top, prod))
                # push production rhs in reverse (handle epsilon)
                if prod != EPS:
                    rhs = self.G._tokenize_prod(prod)
                    for sym in reversed(rhs):
                        stack.append(sym)
        return False, output

    def display_table(self): #muestra la tabla LL(1) en formato legible
        print("LL(1) Table entries:")
        for k, v in self.table.items():
            print(f"M[{k[0]}, {k[1]}] = {v}")