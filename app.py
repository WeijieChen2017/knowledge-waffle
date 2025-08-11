import argparse
import json
from typing import Any, Dict

from manuscripts import ManuscriptDB, generate_prompt

def load_details(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    parser = argparse.ArgumentParser(description="Manuscript manager")
    sub = parser.add_subparsers(dest="command")

    # Prompt generator
    sub.add_parser("prompt", help="Show JSON prompt for ChatGPT")

    # Add entry
    add_p = sub.add_parser("add", help="Add a manuscript")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--authors", required=True, help="Comma separated")
    add_p.add_argument("--affiliations", required=True, help="Comma separated")
    add_p.add_argument("--abstract", required=True)
    add_p.add_argument("--details", help="Path to JSON file containing methods/datasets/metrics")

    # Edit entry
    edit_p = sub.add_parser("edit", help="Edit an entry")
    edit_p.add_argument("index", type=int)
    edit_p.add_argument("--title")
    edit_p.add_argument("--authors")
    edit_p.add_argument("--affiliations")
    edit_p.add_argument("--abstract")
    edit_p.add_argument("--details", help="Path to JSON file with methods/datasets/metrics")

    # Delete entry
    del_p = sub.add_parser("delete", help="Delete an entry")
    del_p.add_argument("index", type=int)

    # List entries
    sub.add_parser("list", help="List entries")

    # List fields
    sub.add_parser("fields", help="List all models, datasets and metrics")

    # Filter entries
    filt_p = sub.add_parser("filter", help="Filter entries")
    filt_p.add_argument("--model")
    filt_p.add_argument("--dataset")
    filt_p.add_argument("--metric")

    args = parser.parse_args()
    db = ManuscriptDB()

    if args.command == "prompt":
        print(generate_prompt())
    elif args.command == "add":
        entry: Dict[str, Any] = {
            "title": args.title,
            "authors": [a.strip() for a in args.authors.split(",") if a.strip()],
            "affiliations": [a.strip() for a in args.affiliations.split(",") if a.strip()],
            "abstract": args.abstract,
            "methods": [],
            "datasets": [],
            "metrics": [],
        }
        if args.details:
            entry.update(load_details(args.details))
        db.add(entry)
        print("Entry added.")
    elif args.command == "edit":
        updates: Dict[str, Any] = {}
        if args.title:
            updates["title"] = args.title
        if args.authors:
            updates["authors"] = [a.strip() for a in args.authors.split(",") if a.strip()]
        if args.affiliations:
            updates["affiliations"] = [a.strip() for a in args.affiliations.split(",") if a.strip()]
        if args.abstract:
            updates["abstract"] = args.abstract
        if args.details:
            updates.update(load_details(args.details))
        db.edit(args.index, updates)
        print("Entry updated.")
    elif args.command == "delete":
        db.delete(args.index)
        print("Entry deleted.")
    elif args.command == "list":
        for i, e in enumerate(db.list()):
            print(f"[{i}] {e['title']}")
    elif args.command == "fields":
        print(json.dumps(db.list_fields(), indent=2))
    elif args.command == "filter":
        results = db.filter(model=args.model, dataset=args.dataset, metric=args.metric)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
