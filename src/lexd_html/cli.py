from lexd_html.unparse import from_lexd


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "lexd", help="lexd file to parse", type=argparse.FileType("r", encoding="utf-8")
    )
    args = parser.parse_args()
    lexd = args.lexd.read()
    print(from_lexd(lexd, "top"))


if __name__ == "__main__":
    main()
