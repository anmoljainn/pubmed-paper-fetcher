## **Installation**

### **1. Clone the Repository**

```sh
git clone https://github.com/anmoljainn/pubmed-paper-fetcher.git
cd pubmed-fetcher
```

### **2. Install Dependencies**

Ensure you have **Python 3.9+** installed, then use **Poetry** to install dependencies:

```sh
poetry install
```

## **Usage**

### **Running the CLI Tool**

To fetch papers for a given query:

```sh
poetry run get-papers-list "cancer treatment"
```

### **Saving Output to CSV**

To save the results as a CSV file:

```sh
poetry run get-papers-list "covid vaccine" -f results.csv
```

### **Debug Mode**

To enable debug mode:

```sh
poetry run get-papers-list "diabetes drug" -d
```

## **Development & Contribution**

### **Running Tests**

```sh
pytest tests/
```

### **Code Formatting**

```sh
black pubmed_fetcher/
```

## **Tools & Technologies Used**

- **Python**: Programming language.
- **Poetry**: Dependency management.
- **PubMed API**: Research paper retrieval.
- **Biopython (Entrez module)**: API calls.
- **argparse**: Command-line argument parsing.

## **References**

- [PubMed API Documentation](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- [Biopython](https://biopython.org/)
