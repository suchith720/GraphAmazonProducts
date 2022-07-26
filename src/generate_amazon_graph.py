import os
import sys

"""
Adding paths to the configuration files and amazon graph packages.
"""
config_path = os.path.join(os.getcwd(), 'config')
package_path = os.getcwd()
sys.path.append(config_path)
sys.path.append(package_path)


from amazon_paths import *
from amazon_handler import *


if __name__ == '__main__':
    """
    Check if the variable are properly defined in the paths file.
    """
    paths = ['dataset_home', 'amazon_file', 'save_dir', 'xc_dir', 'duplicates_file', 'verbose', 'limit']
    for path in paths:
        if path not in vars():
            raise Exception(f'Variable {path} not defined in the config file.')


    """
    Create amazon dataset from the dumps.
    """
    if verbose:
        print("++ Creating graphs from the dumps.")
    amazon_graphs = AmazonGraphContainer()
    amazon_graphs.create_graph(amazon_file, limit=limit)
    amazon_graphs.save_data(save_dir)


    """
    Replacing similar items field of the amazon_product_titles with
    amazon_product_ids
    """
    if verbose:
        print("++ Replacing product title with product ID for similar products.")
    amazon_graphs.load_data(save_dir)
    amazon_graphs.replace_similar_graph_titles()
    amazon_graphs.save_graph(save_dir, tag='_resolved', graph_type='similar')


    """
    Read duplicates file.
    """
    if verbose:
        print("++ Loading duplicates file.")
    duplicates = load_duplicates_map(duplicates_file)


    """
    Remove duplicates -- ids representing same product with a single
    representative.
    """
    if verbose:
        print("++ Replacing duplicate product IDs with a representative product ID.")
    amazon_graphs.load_graph(save_dir, tag='_resolved', graph_type='similar')
    amazon_graphs.replace_graph_duplicates(duplicates)
    amazon_graphs.remove_dead()
    amazon_graphs.convert_graph()
    amazon_graphs.save_graphs(save_dir, tag='_dict')


    """
    XC dataset creation.
    """
    if verbose:
        print("++ Storing data in XC format.")
    xc_data = XCDataset()
    xc_data.create_XCData(save_dir, xc_dir, tag=f'_dict', verbose=verbose)
