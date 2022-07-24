from .amazon_container import *
from .data_splitter import *


"""
class XCDataset uses AmazonGraphContainer and AmazonSplit to store all
the information in a format that XC algorithms can use it.
"""
class XCDataset:

    def __init__(self):
        self.description = None
        self.id_to_title = {}

        self.data_splitter = {}

    def load_idtotitle(self, save_dir, tag='', verbose=True):
        """
        Loading id_to_title
        """
        if verbose:
            print("** Loading Amazon product 'id_to_title'.")

        graph_data = AmazonGraphContainer()
        graph_data.load_idtotitle(save_dir, tag=tag)

        self.id_to_title = graph_data.id_to_title

    def load_description(self, save_dir, tag='', verbose=True):
        """
        Loading description.
        """
        if verbose:
            print("** Loading Amazon 'description'.")

        graph_data = AmazonGraphContainer()
        graph_data.load_description(save_dir, tag=tag)

        self.description = graph_data.description

    def save_sparse_file(self, matrix, save_file):
        matrix.sort_indices()
        rows, cols = matrix.nonzero()
        data = matrix.data

        with open(save_file, 'w') as fout:
            fout.write(f'{matrix.shape[0]} {matrix.shape[1]}\n')

            row_ctr = -1
            line = ''
            for r, c, d in zip(rows, cols, data):
                if row_ctr == r:
                    line = line+f' {c}:{d}'
                elif row_ctr+1 == r:
                    if line:
                        fout.write(f'{line}\n')
                    line = f'{c}:{d}'
                    row_ctr += 1
                else:
                    raise Exception("Row is missing.")
            if line:
                fout.write(f'{line}\n')

    def save_XY_text(self, save_dir, doc_to_rowindex, tag=''):
        os.makedirs(save_dir, exist_ok=True)

        idtocontent_file = f'{save_dir}/{tag}_id_to_text.txt'
        self.save_XY_content(idtocontent_file, self.id_to_title, doc_to_rowindex, self.description)

        idtotitle_file = f'{save_dir}/{tag}_id_to_title.txt'
        self.save_XY_title(idtotitle_file, self.id_to_title, doc_to_rowindex)

    def save_XY_content(self, idtocontent_file, id_to_title, doc_to_rowindex, content):
        with open(idtocontent_file, 'w') as fout:
            for doc_id in sorted(doc_to_rowindex, key=lambda x : doc_to_rowindex[x]):
                if doc_id in content:
                    fout.write(f'{doc_id}->{content[doc_id]}\n')
                else:
                    fout.write(f'{doc_id}->\n')

    def save_XY_title(self, idtotitle_file, id_to_title, doc_to_rowindex):
        with open(idtotitle_file, 'w') as fout:
            for doc_id in sorted(doc_to_rowindex, key=lambda x : doc_to_rowindex[x]):
                if doc_id in id_to_title:
                    fout.write(f'{doc_id}->{id_to_title[doc_id]}\n')
                else:
                    fout.write(f'{doc_id}\n')

    def load_classification_data(self, save_dir, tag='_dict', graph_type='also_buy', verbose=True):
        """
        Creating Classification train-test split
        """
        if verbose:
            print(f"** Creating {graph_type} classification train-test.")

        graph_data = AmazonGraphContainer()
        graph_data.load_graph(save_dir, tag=tag, graph_type=graph_type)
        if not graph_data.graphs[graph_type].graph:
            return False

        self.data_splitter[graph_type] = AmazonSplit(graph_data.graphs[graph_type].graph)
        self.data_splitter[graph_type].clean_matrix()
        self.data_splitter[graph_type].get_split_bylabel(upper_threshold=10)
        return True

    def save_XCClassification_text(self, xc_dir, graph_type='also_buy', verbose=True):
        """
        Saving Classification XY - title and content(text)
        """
        if verbose:
            print(f"** Saving {graph_type} classification train X-article text")
        self.save_XY_text(xc_dir, self.data_splitter[graph_type].train_doc_to_rowindex,
                          tag=f'{graph_type}_classification_train_X')
        if verbose:
            print(f"** Saving {graph_type} classification test X-article text")
        self.save_XY_text(xc_dir, self.data_splitter[graph_type].test_doc_to_rowindex,
                          tag=f'{graph_type}_classification_test_X')
        if verbose:
            print(f"** Saving {graph_type} classification Y-label text")
        self.save_XY_text(xc_dir, self.data_splitter[graph_type].trn_tst_labels,
                          tag=f'{graph_type}_classification_Y')

    def save_XCClassification_data(self, xc_dir, graph_type='also_buy', verbose=True):
        if verbose:
            print(f"** Saving {graph_type} classification train 'trn_X_Y.txt'.")
        train_file = f'{xc_dir}/{graph_type}_trn_X_Y.txt'
        self.save_sparse_file(self.data_splitter[graph_type].train, train_file)

        if verbose:
            print(f"** Saving {graph_type} classification test 'tst_X_Y.txt'.")
        test_file = f'{xc_dir}/{graph_type}_tst_X_Y.txt'
        self.save_sparse_file(self.data_splitter[graph_type].test, test_file)

    def save_XCClassification(self, save_dir, xc_dir, tag='_dict', graph_type='also_buy', verbose=True):
        """
        XC Classification
        """
        if not self.load_classification_data(save_dir, tag=tag, graph_type=graph_type, verbose=verbose):
            return
        self.save_XCClassification_text(xc_dir, graph_type=graph_type, verbose=verbose)
        self.save_XCClassification_data(xc_dir, graph_type=graph_type, verbose=verbose)

    def load_graph_data(self, save_dir, tag='', graph_type='also_buy', verbose=True):
        """
        Loading Graph
        """
        if verbose:
            print(f"** Loading {graph_type} graph.")

        graph_data = AmazonGraphContainer()
        graph_data.load_graph(save_dir, tag=tag, graph_type=graph_type)
        if not graph_data.graphs[graph_type].graph:
            return False

        self.data_splitter[graph_type] = AmazonSplit(graph_data.graphs[graph_type].graph)
        self.data_splitter[graph_type].clean_matrix(clean_type=1)
        return True

    def save_XCGraph_text(self, xc_dir, graph_type='also_buy', verbose=True):
        """
        Saving XC-Graph text
        """
        if verbose:
            print(f"** Saving {graph_type}_graph X-text.")
        self.save_XY_text(xc_dir, self.data_splitter[graph_type].doc_to_rowindex,
                          tag=f'{graph_type}_graph_X')

        if verbose:
            print(f"** Saving {graph_type}_graph Y-text.")
        self.save_XY_text(xc_dir, self.data_splitter[graph_type].labels,
                          tag=f'{graph_type}_graph_Y')

    def save_XCGraph_data(self, xc_dir, graph_type='also_buy', verbose=True):
        if verbose:
            print(f"** Saving '{graph_type}_graph_trn_X_Y.txt'")
        graph_file = f'{xc_dir}/{graph_type}_graph_trn_X_Y.txt'
        self.save_sparse_file(self.data_splitter[graph_type].graph, graph_file)

    def save_XCGraph(self, save_dir, xc_dir, tag='_dict', graph_type='also_buy', verbose=True):
        """
        XC Graph
        """
        if not self.load_graph_data(save_dir, tag=tag, graph_type=graph_type, verbose=verbose):
            return
        self.save_XCGraph_text(xc_dir, graph_type=graph_type, verbose=verbose)
        self.save_XCGraph_data(xc_dir, graph_type=graph_type, verbose=verbose)

    def create_XCData(self, save_dir, xc_dir, tag='_dict', verbose=True):
        self.load_idtotitle(save_dir, tag='', verbose=verbose)
        self.load_description(save_dir, tag='', verbose=verbose)

        graph_types = ['also_buy', 'also_view', 'similar']
        for graph_type in graph_types:
            if verbose:
                print(f'-- Processing {graph_type} graph.')
            self.save_XCClassification(save_dir, xc_dir, tag=tag, graph_type=graph_type, verbose=verbose)
            self.save_XCGraph(save_dir, xc_dir, tag=tag, graph_type=graph_type, verbose=verbose)
            if verbose:
                print()

