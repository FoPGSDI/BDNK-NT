"""Allow running as `python -m rag <command>`."""

import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m rag <command>")
        print()
        print("Commands:")
        print("  ingest              Parse, chunk, embed, and index all documents")
        print("  ingest --skip-embeddings  Ingest without dense embeddings")
        print("  query [question]    Ask a question (or start interactive mode)")
        print("  query -i            Interactive mode")
        print("  eval                Run evaluation on benchmark queries")
        print("  api                 Start the FastAPI server")
        sys.exit(1)

    command = sys.argv[1]
    # Remove command from argv so submodules see clean args
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if command == "ingest":
        from .ingest import main as ingest_main
        skip = "--skip-embeddings" in sys.argv
        ingest_main(skip_embeddings=skip)
    elif command == "query":
        from .interface.cli import main as cli_main
        cli_main()
    elif command == "eval":
        from .eval.evaluate import main as eval_main
        eval_main()
    elif command == "api":
        from .interface.api import main as api_main
        api_main()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
