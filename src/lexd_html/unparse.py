"""
Convert text-format lexd to HTML
"""

from html import escape
from pyfoma.lexd import (
    parse_lexd,
    PatExpr,
    Seq,
    Alt,
    Ref,
    Quant,
    Tagged,
    TokRef,
    LexEntry,
    LexiconDef,
    TagSelector,
)


def unparse_expr(pat: PatExpr) -> str:
    if isinstance(pat, Seq):
        return "(" + " ".join(unparse_expr(part) for part in pat.parts) + ")"
    if isinstance(pat, Alt):
        return "(" + " | ".join(unparse_expr(alt) for alt in pat.alts) + ")"
    if isinstance(pat, Ref):
        return unparse_tokref(pat.token)
    if isinstance(pat, Quant):
        return unparse_expr(pat.expr) + pat.q
    if isinstance(pat, Tagged):
        return unparse_expr(pat.expr) + unparse_selector(pat.selector)


def unparse_tokref(ref: TokRef) -> str:
    selector = unparse_selector(ref.selector)
    match ref.kind:
        case "lex":
            if isinstance(ref.col, tuple):
                assert ref.side == "both"
                # X(1):X(2)
                col_in, col_out = ref.col
                return f"{ref.name}({col_in}):{ref.name}({col_out}){selector}"
            # If there's only one column then col will usually be None
            if ref.col is not None:
                out = f"{ref.name}({ref.col}){selector}"
            else:
                out = f"{ref.name}{selector}"
            match ref.side:
                case "in":
                    return f"{out}:"
                case "out":
                    return f":{out}"
                case "both":
                    return out
        case "anonlex":
            # No selectors are possible, there is only lex (who knows systems)
            anon, _, lex = ref.name.partition(":")
            assert anon == "__ANONLEX__"
            return f"[{lex}]"
        case "pair":
            assert ref.side == "both"
            col_in, col_out = ref.col
            return f"{ref.left}({col_in}):{ref.right}({col_out}){selector}"


def unparse_selector(selector: TagSelector) -> str:
    if selector == TagSelector.any():
        return ""
    if hasattr(selector, "raw") and selector.raw:
        return f"[{selector.raw}]"
    # Simplest case: single clause, one or more tags
    if len(selector.clauses) == 1:
        must, mustnot = selector.clauses[0]
        parts = []
        parts.extend(must)
        parts.extend(f"-{x}" for x in mustnot)
        return f"[{','.join(parts)}]"
    # Multiple clauses are an AND of ORs/XORs
    #
    # It's not clear if this is recoverable in the general case
    #
    # Partition must into conjunct/disjunct sets (ugh, what is this
    # algorithm called?)
    corr = {}
    alltags = set()
    for must, _ in selector.clauses:
        alltags.update(must)
        for x in must:
            corr.setdefault(x, set())
            for y in must:
                if x != y:
                    corr[x].add(y)
    # print("corr:", corr)
    # print("alltags:", alltags)
    # Partition is all of the tags that do not co-occur in musts
    parts = set()
    for x, y in corr.items():
        parts.add(frozenset(alltags - y))
    # print("partition:", parts)
    # FIXME: How to detect overlapping components?  This will fail if
    # there are any, e.g. ^[x,y],^[y,z]

    # Any subset overlapping mustnot clauses is an XOR
    mustnots = set()
    for _, mustnot in selector.clauses:
        mustnots.update(mustnot)
    # print("mustnots:", mustnots)
    outparts = []
    for p in parts:
        op = "^" if (p & mustnots) else "|"
        outparts.append(f"{op}[{','.join(p)}]")
    return f"[{','.join(outparts)}]"


def unparse_top_pattern(pat: PatExpr) -> str:
    if isinstance(pat, Seq):
        return ("<tr>\n" + "\n".join(f"  <td>{escape(unparse_expr(part))}</td>"
                                     for part in pat.parts) + "\n</tr>")
    return f"<tr><td>{escape(unparse_expr(pat))}</td></tr>"


def unparse_pattern(pat: PatExpr, name: str) -> list[str]:
    html = []
    html.append(f'<table data-section="pattern" data-name="{escape(name, True)}">')

    if isinstance(pat, Alt):
        for alt in pat.alts:
            html.append(unparse_top_pattern(alt))
    else:
        html.append(unparse_top_pattern(pat))
    html.append("</table>")
    return html


def unparse_lexentry(self: LexEntry) -> str:
    html = ["<tr>"]
    for c in self.cols:
        ctext = escape(c)
        html.append(f"\n<td>{ctext}</td>")
    if self.tags:
        ttext = escape(','.join(self.tags))
        # Possibly mark these with a data attribute
        html.append(f"\n<td>[{ttext}]</td>")
    html.append("\n</tr>")
    return "".join(html)


def unparse_lexdef(lex: LexiconDef, reverse_aliases: dict[str, set[str]]) -> list[str]:
    html = []
    lextag = f'<table data-section="lexicon" data-name="{escape(lex.name, True)}"'
    if lex.arity != 1:
        lextag += f' data-arity="{lex.arity}"'
    if lex.name in reverse_aliases:
        aliases = escape(" ".join(reverse_aliases[lex.name]), True)
        lextag += f' data-aliases="{aliases}"'
    html.append(f"{lextag}>")
    for ent in lex.entries:
        html.append(unparse_lexentry(ent))
    html.append("</table>")
    return html


def from_lexd(grammar: str, name: str) -> str:
    """Convert lexd from text to HTML."""
    parsed = parse_lexd(grammar)
    reverse_aliases: dict[str, set[str]] = {}
    for k, v in parsed.aliases.items():
        reverse_aliases.setdefault(v, set()).add(k)
    html = []
    html.append(f'<lexd-definition id="{escape(name, True)}">')
    html.append('<table data-section="patterns">')
    for expr in parsed.top_patterns:
        html.append(unparse_top_pattern(expr))
    html.append("</table>")
    for name, pat in parsed.patterns.items():
        html.extend(unparse_pattern(pat, name))
    for lex in parsed.lexicons.values():
        html.extend(unparse_lexdef(lex, reverse_aliases))
    html.append("</lexd-definition>")
    return "\n".join(html)
