from pathlib import Path

from lexd_html.parse import from_html
from lexd_html.unparse import from_lexd


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", help="lexd or html file to parse", type=Path
    )
    args = parser.parse_args()
    if args.input.suffix == ".lexd":
        print(from_lexd(args.input.read_text(encoding='utf-8'), "top"))
    else:
        print(from_html(args.input.read_text(encoding='utf-8')))


if __name__ == "__main__":
    main()
