from dataclasses import asdict
import json
from pyfoma.lexd import parse_lexd
from lexd_html.unparse import unparse_lexdef

examples = [
"""
LEXICON NounRoot[count]
sock
rice[mass,-count]
sand[mass]
""",
"""
LEXICON C(3)
sh[A] m[B] r[C]
y sh v[D]
"""
]


def unfreeze(x):
    if isinstance(x, (frozenset, set)):
        return list(x)
    raise TypeError(f"Cannot serialize object of {type(x)}")


def main():
    for x in examples:
        parsed = parse_lexd(x)
        for n, p in parsed.lexicons.items():
            print(json.dumps(asdict(p), default=unfreeze))
            print("\n".join(unparse_lexdef(p, {})))


if __name__ == '__main__':
    main()
