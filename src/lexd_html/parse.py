"""
Parse lexd in HTML (soon to be rewritten in JavaScript)
"""

from xml.etree import ElementTree
from pyfoma.lexd import ParsedLexd, parse_lexd


def parse_from_html(html: str) -> ParsedLexd:
    """Return a parsed lexd (not an FST) from HTML.

    Currently does something a bit silly and basically strips out HTML
    then calls the lexd parser, which we do because we don't want to
    mess around with its internals.
    """
    lexd = from_html(html)
    return parse_lexd(lexd)


def from_html(html: str) -> str:
    """Return a lexd definition (not an FST) from HTML."""
    root = ElementTree.fromstring(html)
    # Either it's a lexd-definition or it contains one
    if root.tag != "lexd-definition":
        root = root.find(".//lexd-definition")
        if root is None:
            raise ValueError("No <lexd-definition> found in input")

    # The HTML is already sorta-parsed, but we don't want to use any
    # internal functions in pyfoma.lexd, so we will unfortunately just
    # create text.
    lines = []
    aliases = []
    # Just as in an actual lexd file there could be more than one
    # (why)
    for t in root.findall("table[@data-section='patterns']"):
        lines.append("PATTERNS")
        # Each row is definitely a top-level pattern or reference
        for tr in t.findall(".//tr"):
            lines.append(" ".join(td.text for td in tr.findall("td")))
        lines.append("")
    for t in root.findall("table[@data-section='pattern']"):
        name = t.attrib["data-name"]
        lines.append(f"PATTERN {name}")
        # Each row is definitely a top-level pattern or reference
        for tr in t.findall(".//tr"):
            lines.append(" ".join(td.text for td in tr.findall("td")))
        lines.append("")
    for t in root.findall("table[@data-section='lexicon']"):
        name = t.attrib["data-name"]
        attr = t.attrib.get("data-aliases")
        if attr is not None:
            for tok in attr.split(","):
                aliases.append((tok.strip(), name))
        lines.append(f"LEXICON {t.attrib['data-name']}")
        # Each row is definitely a top-level pattern or reference
        for tr in t.findall(".//tr"):
            lines.append(" ".join(td.text for td in tr.findall("td")))
        lines.append("")
    if aliases:
        for src, dest in aliases:
            lines.append(f"ALIAS {src} {dest}")
            lines.append("")
    return "\n".join(lines)
