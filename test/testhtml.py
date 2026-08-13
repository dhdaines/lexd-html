from dataclasses import asdict
import json
from lexd_html.parse import from_html, parse_from_html


examples = [
"""
<lexd-definition id="top">
<table data-section="patterns">
<tr><td>VerbRoot</td><td>VerbInfl</td></tr>
</table>
<table data-section="lexicon" data-name="VerbRoot">
<tr><td>sing</td></tr>
<tr><td>walk</td></tr>
<tr><td>dance</td></tr>
</table>
<table data-section="lexicon" data-name="VerbInfl">
<tr><td>&lt;v&gt;&lt;pres&gt;:</td></tr>
<tr><td>&lt;v&gt;&lt;pres&gt;&lt;p3&gt;&lt;sg&gt;:s</td></tr>
</table>
</lexd-definition>
"""
]


def unfreeze(x):
    if isinstance(x, (frozenset, set)):
        return list(x)
    raise TypeError(f"Cannot serialize object of {type(x)}")


def main():
    for x in examples:
        txt = from_html(x)
        print(txt)
        p = parse_from_html(x)
        print(json.dumps(asdict(p), default=unfreeze))


if __name__ == '__main__':
    main()
