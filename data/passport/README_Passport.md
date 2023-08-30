## Analyze passport data

Source of data https://github.com/vaasha/Data-Analysis_in-Examples/blob/master/EDA_Passport_Numbers/data.csv

1. Sort passport.txt by length of each string
2. Passport with numbers only => 3-17
3. Passports with alphabets and numbers => 6-14
4. Passports starting with single alphabet followed by numbers => 
    - generated.passport.sortedbylen.startwith.1.alpha.txt found following lengths: [6, 7, 8, 9, 10, 11]
    - generated.passport.sortedbylen.startwith.2.alpha.txt found following lengths: [8, 9, 10, 11, 12, 13, 14]
    - generated.passport.sortedbylen.startwith.3.alpha.txt found following lengths: [9, 10, 11, 12, 13]
    - generated.passport.sortedbylen.startwith.4.alpha.txt found following lengths: [9, 10]
    - generated.passport.sortedbylen.startwith.6.alpha.txt found following lengths: [10]
5. Passports with alphabets in the middle
    - generated.passport.sortedbylen.1.alpha.in.middle.txt found following lengths: [9, 10, 11, 12, 13]
    - generated.passport.sortedbylen.2.alpha.in.middle.txt found following lengths: [10, 13]
    - generated.passport.sortedbylen.3.alpha.in.middle.txt found following lengths: [13]
6. Other categories
    - generated.passport.sortedbylen.other.txt             found following lengths: [8, 9, 10]
7. Generate regex pattern based on strings -
   `./7_generate_regex.py -f generated.passport.sortedbylen.txt | sort | uniq > generated.regexes.txt`
   `./6_sortbylen_to_stdout.py generated.regexes.txt > generated.regexes.sortbylen.txt`
8. Optimize generated.regexes.sortbylen.txt manually -

   ```
   \d{3,17}
   [A-Za-z]\d{4,9}
   [A-Za-z]{2,3}\d{5,9}
   [A-Za-z]{4}\d{4,5}
   [A-Za-z]{6}\d{3}
   [A-Za-z]{2}\d{10,11}
   [A-Za-z]\d{7}[A-Za-z]
   [A-Za-z]\d[A-Za-z]\d{5,7}
   [A-Za-z]{2}\d{5}[A-Za-z]\d
   [A-Za-z]{2}\d[A-Za-z]\d{4,6}
   [A-Za-z]\d{2,3}[A-Za-z]\d{4,5}
   [A-Za-z]\d[A-Za-z]{2,3}\d{4,6}
   [A-Za-z]{2}\d{2}[A-Za-z]\d{5}
   [A-Za-z]{2}\d{3}[A-Za-z]{2}\d{2}
   [A-Za-z]\d[A-Za-z]\d[A-Za-z]\d[A-Za-z]{3}
   \d{7,8}[A-Za-z]
   \d[A-Za-z]\d{6,7}
   \d{5}[A-Za-z]{2}
   \d{2}[A-Za-z]\d{6}
   \d{3}[A-Za-z]\d{5,8}
   \d{2,3}[A-Za-z]{2,3}\d{5,7}
   \d{3}[A-Za-z]{2}\d{6}[A-Za-z]
   ```
