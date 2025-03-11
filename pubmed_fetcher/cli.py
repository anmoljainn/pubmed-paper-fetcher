import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_papers, save_to_csv

def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Specify output CSV filename.")
    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    papers = fetch_pubmed_papers(args.query)

    if args.file:
        save_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
