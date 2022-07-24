#/bin/bash

mkdir datasets
cd datasets

wget --no-check-certificate http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/duplicates.txt
wget --no-check-certificate --header="Host: deepyeti.ucsd.edu" --header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" --header="Accept-Language: en-US,en;q=0.9" --header="Referer: http://deepyeti.ucsd.edu/jianmo/amazon/index.html"
"http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/All_Amazon_Meta.json.gz" -c -O 'All_Amazon_Meta.json.gz'
