## Data Classification

https://www.packetlabs.net/posts/data-classification/#:~:text=Data%20Classification%20Levels,-Data%20Classification%20in&text=These%20can%20be%20adopted%20by,how%20they%20should%20be%20handled.
https://sgp.fas.org/library/quist2/chap_7.html
https://kirkpatrickprice.com/blog/classifying-data/

Data classification in government organizations include five levels:

- Top Secret
- Secret
- Confidential
- Sensitive
- Unclassified

These are adopted by commercial organizations. But most often we find four levels:

- Restricted
- Confidential
- Internal
- Public

### How do you classify information ?

First step is having a data classification standard. After that data needs to be classified. But how ? There are multiple ways to classify information to simplify things. There are two primary methods:

- First is to treat all PII, PCI, PHIPA or trade secrets as restricted and attempting to build rules (regular expressions) in your system to automatically tag using a technology. Credit cards are 16 digits and valid cards pass the mod 10 check. 

- Second involves training your staff to understand levels and tag the documentation.

### Detection

* Ability to read PDF metadata (watermarks)
* https://tokern.io/blog/scan-pii-data-warehouse/
* https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html
* https://www.iban.com/structure
* https://helpx.adobe.com/au/acrobat/using/add-watermarks-pdfs.html

### Detection library

* Open-source NLP library https://spacy.io/usage/spacy-101

## Machine Readable Passport

http://www.highprogrammer.com/alan/numbers/mrp.html

For passport analysis based on `git@github.com:vaasha/Data-Analysis_in-Examples.git` see [Passport Analysis Notes](./data/README_Passport.md)
