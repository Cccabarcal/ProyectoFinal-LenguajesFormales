# grammar/slr1_parser.py
from typing import List, Dict, Tuple, Set
from .grammar_module import Grammar
from .first_follow import FirstFollow, END

class Item:
    def __init__(self, left: str, right: List[str], dot: int):
        self.left = left
        self.right = right
        self.dot = dot

    def __eq__(self, other):
        return (self.left, tuple(self.right), self.dot) == (other.left, tuple(other.right), other.dot)

    def __hash__(self):
        return hash((self.left, tuple(self.right), self.dot))

    def next_symbol(self):
        if self.dot < len(self.right):
            return self.right[self.dot]
        return None

    def is_complete(self):
        return self.dot >= len(self.right)

    def advance(self):
        return Item(self.left, self.right, self.dot + 1)

    def __repr__(self):
        r = self.right.copy()
        r.insert(self.dot, '•')
        return f"{self.left} -> {' '.join(r)}"

class SLR1Parser:
    def __init__(self, grammar: Grammar, ff: FirstFollow):
        self.G = grammar
        self.ff = ff
        self.states: List[Set[Item]] = []
        self.action: Dict[Tuple[int,str], Tuple[str,int]] = {}
        self.goto: Dict[Tuple[int,str], int] = {}
        self.productions = []
        for A, prods in self.G.rules.items():
            for p in prods:
                self.productions.append((A, self.G._tokenize_prod(p)))

    def closure(self, items: Set[Item]) -> Set[Item]:
        closure_set = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for it in closure_set:
                B = it.next_symbol()
                if B and B in self.G.non_terminals:
                    for prod in self.G.rules[B]:
                        rhs = self.G._tokenize_prod(prod)
                        ni = Item(B, rhs, 0)
                        if ni not in closure_set:
                            new_items.add(ni)
            if new_items:
                closure_set |= new_items
                changed = True
        return closure_set

    def goto_items(self, items: Set[Item], X: str) -> Set[Item]:
        moved = set()
        for it in items:
            if it.next_symbol() == X:
                moved.add(it.advance())
        return self.closure(moved)

    def build_lr0_automaton(self):
        # Producción aumentada S' -> S
        start_prime = "S'"
        self.productions.insert(0, (start_prime, [self.G.start_symbol]))
        start_item = Item(start_prime, [self.G.start_symbol], 0)
        I0 = self.closure({start_item})
        self.states = [I0]
        added = True
        while added:
            added = False
            for I in list(self.states):
                symbols = set()
                for it in I:
                    s = it.next_symbol()
                    if s:
                        symbols.add(s)
                for X in symbols:
                    gotoI = self.goto_items(I, X)
                    if not gotoI:
                        continue
                    if gotoI not in self.states:
                        self.states.append(gotoI)
                        added = True
                    i = self.states.index(I)
                    j = self.states.index(gotoI)
                    if X in self.G.non_terminals:
                        self.goto[(i, X)] = j
                    else:
                        self.action[(i, X)] = ("shift", j)

    def build_slr_tables(self):
        start_prime = "S'"
        for i, I in enumerate(self.states):
            for it in I:
                # caso de reducción
                if it.is_complete():
                    if it.left == start_prime:
                        # Aceptar
                        self.action[(i, END)] = ("accept", 0)
                    else:
                        prod_index = self.productions.index((it.left, it.right))
                        for a in self.ff.follow[it.left]:
                            if (i, a) not in self.action:
                                self.action[(i, a)] = ("reduce", prod_index)
                else:
                    s = it.next_symbol()
                    # shifts ya fueron añadidos en build_lr0_automaton()
                    pass

    def parse(self, tokens: List[str]):
        tokens = tokens + [END] if tokens[-1] != END else tokens
        stack = [0]
        ip = 0
        a = tokens[ip]
        while True:
            s = stack[-1]
            act = self.action.get((s, a))
            if not act:
                print(f"Error: No action for state {s} and symbol {a}")
                return False
            typ, val = act
            if typ == "shift":
                stack.append(val)
                ip += 1
                a = tokens[ip]
            elif typ == "reduce":
                A, rhs = self.productions[val]
                for _ in rhs:
                    stack.pop()
                t = stack[-1]
                goto_state = self.goto.get((t, A))
                if goto_state is None:
                    print(f"Error: No goto for state {t} and nonterminal {A}")
                    return False
                stack.append(goto_state)
                print(f"Reduce: {A} -> {' '.join(rhs)}")
            elif typ == "accept":
                print("Cadena aceptada ✅")
                return True
            else:
                print("Acción desconocida:", act)
                return False

    def display_tables(self):
        print("\nACTION TABLE:")
        for k, v in sorted(self.action.items()):
            print(f"ACTION[{k}] = {v}")
        print("\nGOTO TABLE:")
        for k, v in sorted(self.goto.items()):
            print(f"GOTO[{k}] = {v}")
