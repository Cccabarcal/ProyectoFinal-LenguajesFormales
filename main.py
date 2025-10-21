from grammar.grammar_module import Grammar
from grammar.first_follow import FirstFollow
from grammar.ll1_parser import LL1Parser
from grammar.slr1_parser import SLR1Parser


SAMPLE_LL1 = """
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id
"""

SAMPLE_SLR1 = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
"""

def test_ll1():
    print("="*60)
    print("PROBANDO PARSER LL(1)")
    print("="*60)
    g = Grammar.from_text(SAMPLE_LL1, start_symbol="E")
    g.display()

    ff = FirstFollow(g)
    ff.compute_all_first()
    ff.compute_all_follow()
    ff.display()

    ll1 = LL1Parser(g, ff)
    ll1.build_table()
    ll1.display_table()

    # probar parser LL(1)
    tokens = ['id', '+', 'id', '$']
    print(f"\nParsing tokens: {tokens}")
    ok, trace = ll1.parse(tokens)
    print("Parse result:", "✅ ACEPTADA" if ok else "❌ RECHAZADA")
    if trace:
        print("Derivaciones:")
        for step in trace:
            print(f"  {step}")

def test_slr1():
    print("\n" + "="*60)
    print("PROBANDO PARSER SLR(1)")
    print("="*60)
    g = Grammar.from_text(SAMPLE_SLR1, start_symbol="E")
    g.display()

    ff = FirstFollow(g)
    ff.compute_all_first()
    ff.compute_all_follow()
    ff.display()

    slr = SLR1Parser(g, ff)
    slr.build_lr0_automaton()
    slr.build_slr_tables()
    slr.display_tables()

    # probar parser SLR(1)
    tokens = ['id', '+', 'id', '*', 'id']
    print(f"\nParsing tokens: {tokens}")
    result = slr.parse(tokens)
    print("Parse result:", "✅" if result else "❌")

def main():
    test_ll1()
    test_slr1()

if __name__ == "__main__":
    main()
