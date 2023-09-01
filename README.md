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

## Installation

I have tested it with Python 3.9. It works well if you have a version >= 3.9.

1. Clone the repository `git clone git@github.com:opcoder0/privet.git`
2. Change directory `cd privet`
3. Create a virtual environment `python -m venv venv`
4. Activate the virtual environment `source venv/bin/activate`
5. Install dependencies `pip install -r requirements.txt`
6. Download Spacy's trained model/pipeline. `python -m spacy download en_core_web_sm`
6. Run `python privet.py --help`

## Usage

```
usage: privet.py [-h] [-f FORMAT] [-d /path1,/path2,...] [-n NAMESPACE] [-v] [-z /path/to/file]

Search for confidential data in files

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Specify file format [txt, pdf]
  -d /path1,/path2,..., --dir /path1,/path2,...
                        search path to find files
  -n NAMESPACE, --namespace NAMESPACE
                        search namespace can indicate region or search domain
  -v, --verbose         verbose output
  -z /path/to/file, --visualize /path/to/file
                        Visualize document entites
```
