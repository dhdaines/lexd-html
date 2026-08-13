from dataclasses import asdict
import json
from pyfoma.lexd import parse_lexd
from lexd_html.unparse import unparse_pattern

examples = [
"""PATTERNS
(A B)[x]
(A B)[-x]
""",
"""PATTERNS
NounRoot[count] [<n>:] Number # 'sock' and 'sand', but not 'rice'
NounRoot[mass] [<n>:]         # 'rice' and 'sand', but not 'sock'
""",
"""PATTERNS
A?(1) B A?(1)
""",
"""PATTERNS
(NounStem CaseEnding)[^[Decl1,Decl2],^[N,M,F]]
""",
]


def unfreeze(x):
    if isinstance(x, (frozenset, set)):
        return list(x)
    raise TypeError(f"Cannot serialize object of {type(x)}")


def main():
    for x in examples:
        parsed = parse_lexd(x)
        for p in parsed.top_patterns:
            print(json.dumps(asdict(p), default=unfreeze))
            print(unparse_pattern(p, "unparsed"))



if __name__ == '__main__':
    main()
