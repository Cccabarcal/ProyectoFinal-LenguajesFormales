from typing import Dict, Set
from .grammar_module import Grammar

EPS = 'ε'
END = '$'

class FirstFollow:
    def __init__(self, grammar: Grammar):
        self.G = grammar
        self.first: Dict[str, Set[str]] = {nt: set() for nt in self.G.non_terminals}
        self.follow: Dict[str, Set[str]] = {nt: set() for nt in self.G.non_terminals}
        if self.G.start_symbol:
            self.follow[self.G.start_symbol].add(END)

    def compute_all_first(self):
        changed = True
        while changed:
            changed = False
            for A in self.G.non_terminals:
                for prod in self.G.rules.get(A, []):
                    symbols = self.G._tokenize_prod(prod)
                    # if production is epsilon
                    if prod == EPS or not symbols:
                        if EPS not in self.first[A]:
                            self.first[A].add(EPS)
                            changed = True
                        continue
                    i = 0
                    while True:
                        X = symbols[i]
                        if X in self.G.terminals:
                            if X not in self.first[A]:
                                self.first[A].add(X); changed = True
                            break
                        else:  # X is non-terminal
                            before = len(self.first[A])
                            # add FIRST(X) - {eps}
                            self.first[A].update(x for x in self.first[X] if x != EPS)
                            if EPS in self.first[X]:
                                i += 1
                                if i >= len(symbols):
                                    if EPS not in self.first[A]:
                                        self.first[A].add(EPS); changed = True
                                    break
                                else:
                                    continue
                            else:
                                if len(self.first[A]) != before:
                                    changed = True
                                break

    def compute_all_follow(self):
        changed = True
        while changed:
            changed = False
            for A in self.G.non_terminals:
                for prod in self.G.rules.get(A, []):
                    symbols = self.G._tokenize_prod(prod)
                    for i, B in enumerate(symbols):
                        if B in self.G.non_terminals:
                            trailer = set()
                            # compute FIRST of beta
                            beta = symbols[i+1:]
                            if not beta:
                                trailer = set(self.follow[A])
                            else:
                                first_beta = set()
                                j = 0
                                while j < len(beta):
                                    X = beta[j]
                                    if X in self.G.terminals:
                                        first_beta.add(X); break
                                    else:
                                        first_beta.update(x for x in self.first[X] if x != EPS)
                                        if EPS in self.first[X]:
                                            j += 1
                                            if j == len(beta):
                                                first_beta.add(EPS)
                                                break
                                            continue
                                        else:
                                            break
                                if EPS in first_beta:
                                    trailer = (first_beta - {EPS}) | self.follow[A]
                                else:
                                    trailer = first_beta
                            before = len(self.follow[B])
                            self.follow[B].update(trailer)
                            if len(self.follow[B]) != before:
                                changed = True

    def display(self):
        print("FIRST sets:")
        for k, v in self.first.items():
            print(f"FIRST({k}) = {v}")
        print("\nFOLLOW sets:")
        for k, v in self.follow.items():
            print(f"FOLLOW({k}) = {v}")