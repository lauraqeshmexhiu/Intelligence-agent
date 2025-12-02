from agent import run_agent_question
import argparse
from pathlib import Path

from scanner import scan_directory


def main():

    """
    Sets up CLI using python's argparse module (built-in).
    """
    parser = argparse.ArgumentParser(
        description="Repository Intelligence Agent CLI",
    )

    """"" 
    Defines subcommands: 'scan' for scanning repos and 'ask' for querying metadata.
    
    """
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- scan command ---
    scan_parser = subparsers.add_parser(
        "scan", help="Scan repositories and generate metadata JSON files",
    )
    scan_parser.add_argument(
        "repos_dir",
        help="Path to directory containing Git repositories",
    )
    scan_parser.add_argument(
        "--output-dir",
        default="metadata",
        help="Directory to write metadata JSON files (default: metadata)",
    )

        # --- ask command ---
    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask a question about the repositories using the metadata",
    )
    ask_parser.add_argument(
        "metadata_dir",
        help="Directory containing metadata JSON files (e.g. 'metadata')",
    )
    ask_parser.add_argument(
        "question",
        help="Natural language question about the repositories",
    )


#    Parse arguments
    args = parser.parse_args()

    if args.command == "scan":
        repos_dir = args.repos_dir
        output_dir = args.output_dir
        # # If the folder does not exist, create it , if it does exist, do nothing
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print(f"Scanning repos in: {repos_dir}")
        print(f"Writing metadata to: {output_dir}\n")
        
        # call Scanner
        scan_directory(repos_dir, output_dir)

    elif args.command == "ask":
        metadata_dir = args.metadata_dir
        question = args.question

        print(f"Using metadata from: {metadata_dir}")
        print(f"Question: {question}\n")

        answer = run_agent_question(metadata_dir, question)
        print("\n🧠 Agent answer:")
        print(answer)



    else:
        parser.error(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
