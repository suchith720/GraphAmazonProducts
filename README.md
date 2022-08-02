# GraphAmazonProducts Dataset

This is product-to-product recommendation dataset.
The link to the raw dataset can be obtained from the following [link](http://deepyeti.ucsd.edu/jianmo/amazon/index.html). If this link does not work please contact me for the dumps. This dataset was primarily created for Extreme classification task, to improve the accuracy of the classification by using additional information in the form of graphs present at the data-point side as well as the label side.

The dataset was created considering three fields present in the dump for a given product, these fields are 'also_buy', 'also_view' and 'similar'. Anyone graph can be used for the classification task and the remaining for boosting the accuracy as additional information. Click [here](https://owncloud.iitd.ac.in/nextcloud/index.php/s/Y6DsjWNEjgqyk7R) to download the dataset.



Run all you code from the root directory of the repository, the steps to create the dataset are as follows:

1. Download the raw data:<br>`$ ./scripts/download_dataset.sh`

2. Fill the config file properly 
Config file is present at `./config/amazon_paths.py`, please provide approriate path variable in the file for the scripts to run properly, an example is provided here.<br>
```
verbose = True
limit = None
dataset_home = '/home/scai/phd/aiz218323/scratch/XML/amazon-review-data/'
amazon_file = f'{dataset_home}/datasets/All_Amazon_Meta.json.gz'
save_dir = f'{dataset_home}/GraphAmazonProducts/results'
xc_dir = f'{dataset_home}/GraphAmazonProducts/XCData'
duplicates_file = f'{dataset_home}/datasets/duplicates.txt'
```


3. Run the main script to create the dataset<br> 
`$ python src/generate_amazon_graph.py`


## Dataset statistics

Here are some statistics of the dataset:


field/properties | number of labels |	number of train |	number of test | points per label	| labels per point
--- | --- | --- | --- | --- | --- 
also_buy	| 1,591,824	| 1,502,829	| 645,683 |	16.246278	|	3.0
also_view | 1,712,182 | 1,722,517 |	742,851	| 10.785238	|	1.0
similar items | 388,544 | 840,754 | 361,756 | 6.297799 |	1.0

## Baselines

Algorithm | P1 | P3 | P5 | N1 | N3 | N5 | PSP1 | PSP3 | PSP5 | PSN1 | PSN3 | PSN5 | MODELSIZE | TRNTIME | PREDTIME
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
Parabel | 35.53 | 29.96 | 26.35 | 35.53 | 33.28 | 32.30 | 15.14 | 18.47 | 20.47 | 15.14 | 17.01 | 18.15 | 6.85 | 0.82 | 1.37
Bonsai | 37.53 | 31.48 | 27.55 | 37.53 | 35.35 | 34.41 | 17.23 | 20.74 | 22.77 | 17.23 | 19.45 | 20.80 | 4831.20 | 15777.20 | 38.18
PfastreXML | 28.61 | 24.22 | 21.48 | 28.61 | 28.01 | 27.92 | 21.49 | 23.22 | 24.24 | 21.49 | 22.65 | 23.40 | 22.30 | 5.61 | 20.32
AnneXML | 0.08 | 0.07 | 0.06 | 0.08 | 0.07 | 0.07 | 0.01 | 0.02 | 0.02 | 0.01 | 0.02 | 0.02 | 10355.99 | 3751.42 | 0.11

