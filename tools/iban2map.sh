# take a file copied from https://www.iban.com/structure
# and convert to python map.
# NOTE 
#  before feeding it in replace tabs with spaces in the input file
#  if country names have spaces replace them with underscores and manually replace them back later
filename=$1

while read -r line 
do
    country=`echo $line | awk '{print $1}'`
    countrycode=`echo $line | awk '{print $2}'`
    sepa=`echo $line | awk '{print $3}'`
    ndigits=`echo $line | awk '{print $4}'`
    echo "\"$countrycode\": { \"country\": \"$country\", \"sepa\": \"$sepa\", \"ndigits\": $ndigits },"
done < ${filename}
