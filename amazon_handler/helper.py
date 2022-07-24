import os
import gc
import json
import gzip
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from scipy.sparse import csr_matrix


def dict_head_random(dictionary, n=10):
    if len(dictionary):
        keys = np.random.choice(list(dictionary.keys()), size=n)
        for k in keys:
            print(f'{k} : {dictionary[k]}')
    else:
        print("EMPTY!!")


def read_amazon_dataset(filename, num_prods=3):
    data = []
    num_prods_cnt = 0
    with gzip.open(filename) as file:
        for i, line in enumerate(file):
            if  num_prods is None or num_prods_cnt < num_prods:
                product = json.loads(line.strip())
                if product['also_buy'] or product['also_view'] or product['similar_item']:
                    data.append(product)
                    num_prods_cnt += 1
            else:
                break
            if i > num_prods:
                break
    return data


def load_duplicates_map(duplicates_file):
    duplicates = {}

    with open(duplicates_file) as file:
        for line in file:
            product_ids = line[:-1].split(' ')

            if len(product_ids):
                representative_id = product_ids[0]
                for product_id in product_ids:
                    duplicates[product_id] = representative_id

    return duplicates

