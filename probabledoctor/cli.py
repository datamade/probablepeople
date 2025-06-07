import argparse

from . import parse, tag


def main():
    parser = argparse.ArgumentParser(
        prog="probabledoctor",
        description="CLI for parsing and tagging personal or corporate names",
    )
    parser.add_argument("name", nargs="+", help="Name string to parse or tag")
    parser.add_argument(
        "--type",
        choices=["generic", "person", "company"],
        default="generic",
        help="Model type to use",
    )
    parser.add_argument(
        "--tag", action="store_true", help="Output structured components and name type"
    )
    args = parser.parse_args()

    raw = " ".join(args.name)
    if args.tag:
        result, name_type = tag(raw, args.type)
        print(name_type)
        for label, comp in result.items():
            print(f"{label}: {comp}")
    else:
        tokens = parse(raw, args.type)
        for tok, lbl in tokens:
            print(f"{tok}\t{lbl}")


if __name__ == "__main__":
    main()
