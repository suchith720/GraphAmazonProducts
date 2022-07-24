#GraphAmazonProducts dataset.
This is product-to-product recommendation dataset.
The link to the raw dataset can be obtained from the following link http://deepyeti.ucsd.edu/jianmo/amazon/index.html. If this link does not work please contact me for the dumps.
The dataset was created considering three field in the dumps for a given product, these fields are 'also_buy', 'also_view' and 'similar'. Any of the graph can be used for classification and the result for boosting the accuracy as additional information.

This dataset was primarily created for Extreme classification task, to improve the accuracy of the classification by using additional information in the form of graphs present at the data-point side as well as the label side.

Run all you code from the root directory of the repository,

The steps to create the dataset is as follows:

1. Downlaod the raw data: 
$ ./scripts/download_dataset.sh

2. Fill the config file properly 
Config file is present at ./config/amazon_paths.py, please provide approriate path variable in the file for the scripts to run properly, an example is provided here.
dataset_home = '/home/scai/phd/aiz218323/scratch/XML/amazon-review-data/'
amazon_file = f'{dataset_home}/datasets/All_Amazon_Meta.json.gz'
save_dir = f'{dataset_home}/GraphAmazonProducts/results'
xc_dir = f'{dataset_home}/GraphAmazonProducts/XCData'
duplicates_file = f'{dataset_home}/datasets/duplicates.txt'
verbose=True
limit=None

3. Run the main script to create the dataset 
$ python src/generate_amazon_graph.py


Here are some statistics of the dataset:
| | no. of labels | no. of train | no. of test | points per label | labels per point |
| also_buy | 3,344,455 | 1,796,320 | 773,018 | 16.158 | 9 |
| also_view | 4,557,217 | 2,073,896 | 996,089 | 10.68 | 32 |
| similar | 388,492 | 840,758 | 361,775 | 6.297 | 1 |

