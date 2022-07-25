# GraphAmazonProducts Dataset

This is product-to-product recommendation dataset.
The link to the raw dataset can be obtained from the following [link](http://deepyeti.ucsd.edu/jianmo/amazon/index.html). If this link does not work please contact me for the dumps. This dataset was primarily created for Extreme classification task, to improve the accuracy of the classification by using additional information in the form of graphs present at the data-point side as well as the label side.

The dataset was created considering three fields present in the dump for a given product, these fields are 'also_buy', 'also_view' and 'similar'. Anyone graph can be used for the classification task and the remaining for boosting the accuracy as additional information.



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

fields/properties | no. of labels | no. of train | no. of test | points per label | labels per point
--- | --- | --- | --- | --- | ---
also_buy | 3,344,455 | 1,796,320 | 773,018 | 16.158 | 9
also_view | 4,557,217 | 2,073,896 | 996,089 | 10.68 | 32
similar | 388,492 | 840,758 | 361,775 | 6.297 | 1

## Baselines

Algorithm | P1 | P3 | P5 | N1 | N3 | N5 | PSP1 | PSP3 | PSP5 | PSN1 | PSN3 | PSN5 | MODELSIZE | TRNTIME | PREDTIME
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
Parabel | 36.88 | 32.70 | 30.01 | 36.88 | 34.54 | 33.31 | 12.59 | 14.71 | 16.19 | 12.59 | 13.67 | 14.43 | 15.74 | 1.27 | 0.95

