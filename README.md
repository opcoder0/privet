## Privet

`privet` is a tool to find confidential information on the filesystem. The tool vets and lists files with confidential information in them. The tool looks for any personal identifiable information (PII), credit card numbers, government id numbers and so on.

The tool supports the following file formats -

- Text
- PDF

Types of information the tool recognizes -

- Credit Card Numbers
- IBAN
- AWS Access Key IDs and Secret Access Key
- Passport Numbers

## Usage

```
usage: privet.py [-h] [-t /path1,/path2,...] [-p /path1,/path2,...]

Search for confidential data in files. Requires atleast one file type to run

optional arguments:
  -h, --help            show this help message and exit
  -t /path1,/path2,..., --text /path1,/path2,...
                        search text files
  -p /path1,/path2,..., --pdf /path1,/path2,...
                        search PDF files
```
