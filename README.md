## Privet

`privet` is a tool to find sensitve information in a file. The tool vets and lists files with confidential information. The tool looks for any personal identifiable information (PII), credit card numbers, government id numbers and so on. The tool supports two formats -

- Text
- PDF

Types of information the tool recognizes -

- Australia
  - Bank Names
  - Drivers License
  - Passport
  - Medicare Card Number
  - Bank Account and BSB Numbers
  - ABN and ACN Numbers
  - TFN Numbers
  - Mobile and Fixedline Numbers
- Credit Card Numbers (validated using Luhns Algorithm)
- IBAN
- Passport Numbers
- AWS Access Key IDs and Secret Access Key
- International Bank Names

## Design

Search is supported using two methods 

- Filter (`-s filter`): The search looks through files and searches for patterns and keywords in a range of about 250 words.
- NLP (`-s nlp`): The search looks through files using Spacy's NLP library. It relies on entities and matchers to display the likelyhood of a successful search result.


## Usage

```
usage: privet.py [-h] [-t] [-p] [-d /path1,/path2,...] [-s SEARCHTYPE] [-n NAMESPACE] [-v]

Search for confidential data in files. Requires atleast one file type to run

optional arguments:
  -h, --help            show this help message and exit
  -t, --text            search text files
  -p, --pdf             search PDF files
  -d /path1,/path2,..., --dir /path1,/path2,...
                        search path to find files
  -s SEARCHTYPE, --searchtype SEARCHTYPE
                        search technique; supported values one of: "nlp" or "filter"
  -n NAMESPACE, --namespace NAMESPACE
                        search namespace can indicate region or search domain
  -v, --verbose         verbose output
```
