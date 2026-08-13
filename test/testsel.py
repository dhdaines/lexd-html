import json
from pyfoma.lexd import parse_tag_selector, TagSelector
from lexd_html.unparse import unparse_selector

examples = [
    "x",
    "x,y",
    "x,-y",
    "|[x,y]",
    "^[x,y]",
    "|[x,y],|[a,b,c]",
    "|[x,y],^[a,b,c]",
    "^[x,y],^[a,b,c]",
    "^[x,y],^[a,b,c],|[d,e,f]",
    "^[nofruit,nocolor,nofun]",
]


def unfreeze(x):
    if isinstance(x, (frozenset, set)):
        return list(x)
    raise TypeError(f"Cannot serialize object of {type(x)}")


for x in examples:
    ts = parse_tag_selector(x)
    print(f"{x}:")
    for must, mustnot in ts.clauses:
        print("   must:", json.dumps(must, default=unfreeze))
        print("   mustnot:", json.dumps(mustnot, default=unfreeze))
        print()
    up = unparse_selector(TagSelector(ts.clauses))
    print(f"[{x}] => {up}")
