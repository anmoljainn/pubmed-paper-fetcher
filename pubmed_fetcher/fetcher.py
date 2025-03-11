import requests
from Bio import Entrez
from typing import List, Dict, Tuple
import re
import csv

Entrez.email = "jainanmol064@gmail.com"  # REQUIRED for PubMed API

# List of keywords to identify academic institutions
ACADEMIC_KEYWORDS = ["university", "college", "institute", "research center", "academy"]

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from PubMed API based on a search query."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    paper_ids = record["IdList"]

    papers = []
    for paper_id in paper_ids:
        handle = Entrez.efetch(db="pubmed", id=paper_id, retmode="xml")
        details = Entrez.read(handle)
        handle.close()

        if "PubmedArticle" in details:
            article = details["PubmedArticle"][0]
            papers.append(parse_article(article, paper_id))

    return papers

def parse_article(article, paper_id: str) -> Dict:
    """Extract metadata from a PubMed article."""
    title = article["MedlineCitation"]["Article"]["ArticleTitle"]
    pub_date = article["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
    authors = article["MedlineCitation"]["Article"].get("AuthorList", [])

    non_academic_authors, company_affiliations = extract_non_academic_authors(authors)
    corresponding_email = extract_corresponding_email(article)

    return {
        "PubmedID": paper_id,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(non_academic_authors),
        "Company Affiliation(s)": ", ".join(company_affiliations),
        "Corresponding Author Email": corresponding_email,
    }

def extract_non_academic_authors(authors) -> Tuple[List[str], List[str]]:
    """Identify non-academic authors and their affiliations."""
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        if "AffiliationInfo" in author:
            for aff in author["AffiliationInfo"]:
                affiliation = aff["Affiliation"]
                if not any(kw in affiliation.lower() for kw in ACADEMIC_KEYWORDS):
                    non_academic_authors.append(author["LastName"])
                    company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations

def extract_corresponding_email(article) -> str:
    """Extract corresponding author's email if available."""
    abstract_text = article["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", "")
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", str(abstract_text))
    return email_match.group(0) if email_match else "N/A"

def save_to_csv(papers: List[Dict], filename: str):
    """Save extracted papers to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
