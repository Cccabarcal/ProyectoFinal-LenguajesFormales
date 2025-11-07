from typing import Dict, Set #importamos datos para anotaciones de tipos de variables 
from .grammar_module import Grammar 

EPS = 'ε' #definimos el simbolo de epsilon
END = '$' #definimos el simbolo de fin de cadena

class FirstFollow:
    def __init__(self, grammar: Grammar): #el contructor recibe una gramatica y la guarda
        self.G = grammar
        self.first: Dict[str, Set[str]] = {nt: set() for nt in self.G.non_terminals} #creamos dos diccionarios vacios para first y follow 
        self.follow: Dict[str, Set[str]] = {nt: set() for nt in self.G.non_terminals}
        if self.G.start_symbol:  #si la gramatica tiene simbolo inicial definido se agrega el simbolo de fin de cadena al follow del simbolo inicial
            self.follow[self.G.start_symbol].add(END)

    def compute_all_first(self): #funcion para calcular todos los conjuntos first usando un algoritmo iterativo y changed para detectar cambios
        changed = True
        while changed:
            changed = False
            for A in self.G.non_terminals: #recorre cada no terminal A y cada produccion prdo asociada , convierte la produccion en una lista de simbolos
                for prod in self.G.rules.get(A, []):
                    symbols = self.G._tokenize_prod(prod)
                    # if production is epsilon
                    if prod == EPS or not symbols: #si la produccion es epsilon o vacia agrega epsilon al first de A y pasa a la siguiente produccion
                        if EPS not in self.first[A]:
                            self.first[A].add(EPS)
                            changed = True
                        continue
                    i = 0 #si no es epsilon, procesa los simbolos de la produccion uno a uno desde el primero
                    while True:
                        X = symbols[i] #si X es un no terminal se añade su first al first de A sin incluir epsilon
                        if X in self.G.terminals:
                            if X not in self.first[A]:
                                self.first[A].add(X); changed = True
                            break
                        else:  # X is non-terminal
                            before = len(self.first[A]) 
                            # add FIRST(X) - {eps}
                            self.first[A].update(x for x in self.first[X] if x != EPS)
                            if EPS in self.first[X]: #si X puede derivar epsilon, se continua con el siguiente simbolo
                                i += 1
                                if i >= len(symbols):
                                    if EPS not in self.first[A]:
                                        self.first[A].add(EPS); changed = True #si todos los simbolos pueden derivar epsilon, agrega epsilon al first de A
                                    break
                                else:
                                    continue
                            else:
                                if len(self.first[A]) != before: #si no puede derivar epsilon se verifica si hubo cambios y se sale del while
                                    changed = True
                                break

    def compute_all_follow(self): #funcion para calcular todos los conjuntos follow usando un algoritmo iterativo y changed para detectar cambios
        changed = True
        while changed:
            changed = False
            for A in self.G.non_terminals: #recorre cada no terminal A y cada produccion prdo asociada
                for prod in self.G.rules.get(A, []):
                    symbols = self.G._tokenize_prod(prod)
                    for i, B in enumerate(symbols): #recorre cada simbolo B en la produccion
                        if B in self.G.non_terminals:
                            trailer = set()
                            # compute FIRST of beta
                            beta = symbols[i+1:] #obtiene los simbolos que siguen a B en la produccion
                            if not beta:
                                trailer = set(self.follow[A])
                            else:               #si hay simbolos despues de B, calcula su first
                                first_beta = set()
                                j = 0
                                while j < len(beta):
                                    X = beta[j]
                                    if X in self.G.terminals:
                                        first_beta.add(X); break
                                    else:
                                        first_beta.update(x for x in self.first[X] if x != EPS)
                                        if EPS in self.first[X]: #si X puede derivar epsilon, continua con el siguiente simbolo
                                            j += 1
                                            if j == len(beta):
                                                first_beta.add(EPS)
                                                break
                                            continue
                                        else:
                                            break
                                if EPS in first_beta: #si el first de beta contiene epsilon, follow recibe first de beta sin epsilon mas follow de A
                                    trailer = (first_beta - {EPS}) | self.follow[A]
                                else:
                                    trailer = first_beta
                            before = len(self.follow[B]) #guarda el tamaño actual del follow de B
                            self.follow[B].update(trailer)
                            if len(self.follow[B]) != before:
                                changed = True

    def display(self):     #funcion para mostrar los conjuntos first y follow
        print("FIRST sets:")
        for k, v in self.first.items():
            print(f"FIRST({k}) = {v}")
        print("\nFOLLOW sets:")
        for k, v in self.follow.items():
            print(f"FOLLOW({k}) = {v}")