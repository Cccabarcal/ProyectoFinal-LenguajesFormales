from typing import Dict, Tuple
from .grammar_module import Grammar
from .first_follow import FirstFollow, EPS, END

class LL1Parser:
    def __init__(self, grammar: Grammar, ff: FirstFollow):
        self.G = grammar
        self.ff = ff
        self.table: Dict[Tuple[str,str], str] = {}  # (nonterminal, terminal) -> production

    def build_table(self):
        self.table.clear()
        for A in self.G.non_terminals:
            for prod in self.G.rules.get(A, []):
                symbols = self.G._tokenize_prod(prod)
                # compute FIRST(prod)
                first_of_prod = set()
                if prod == EPS:
                    first_of_prod.add(EPS)
                else:
                    i = 0
                    while i < len(symbols):
                        X = symbols[i]
                        if X in self.G.terminals:
                            first_of_prod.add(X); break
                        else:
                            first_of_prod.update(x for x in self.ff.first[X] if x != EPS)
                            if EPS in self.ff.first[X]:
                                i += 1
                                if i == len(symbols):
                                    first_of_prod.add(EPS)
                                continue
                            else:
                                break
                for a in (first_of_prod - {EPS}):
                    self.table[(A,a)] = prod
                if EPS in first_of_prod:
                    for b in self.ff.follow[A]:
                        self.table[(A,b)] = prod

    def parse(self, tokens: list):
        # tokens should end with END symbol or we append END
        tokens = tokens + [END] if tokens[-1] != END else tokens
        stack = ['$', self.G.start_symbol]
        ip = 0
        a = tokens[ip]
        output = []
        while stack:
            top = stack.pop()
            if top == '$' and a == END:
                return True, output
            if top in self.G.terminals or top == END or top == '$':
                if top == a:
                    ip += 1
                    a = tokens[ip]
                    continue
                else:
                    return False, output
            else:
                prod = self.table.get((top, a))
                if not prod:
                    return False, output
                output.append((top, prod))
                # push production rhs in reverse (handle epsilon)
                if prod != EPS:
                    rhs = self.G._tokenize_prod(prod)
                    for sym in reversed(rhs):
                        stack.append(sym)
        return False, output

    def display_table(self):
        print("LL(1) Table entries:")
        for k, v in self.table.items():
            print(f"M[{k[0]}, {k[1]}] = {v}")