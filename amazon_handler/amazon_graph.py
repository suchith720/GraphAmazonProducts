from .helper import *


"""
class AmazonGraph stores the basic graph information in the adjacency
list format.
"""
class AmazonGraph:

    def __init__(self):
        self.graph = {}

    def add_product(self, prod_id, products):
        products, counts = np.unique(products, return_counts=True)
        self.graph[prod_id] = (products.tolist(), counts.tolist())

    def save_data(self, save_dir, tag=''):
        os.makedirs(save_dir, exist_ok=True)
        filename = f'{save_dir}/amazon_graph{tag}.pickle'
        with open(filename, 'wb') as f:
            pickle.dump(self.graph, f)

        del self.graph
        gc.collect()

    def load_data(self, save_dir, tag=''):
        filename = f'{save_dir}/amazon_graph{tag}.pickle'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.graph = pickle.load(f)
            return True
        print(f"ERROR:: Unable to load the graph at '{filename}'")
        return False

    def replace_duplicates(self, duplicates):
        delete_nodes = []

        for node in self.graph:
            if node in duplicates:
                delete_nodes.append(node)

            for i, (edge, count) in enumerate( zip(*self.graph[node]) ):
                if edge in duplicates:
                    self.graph[node][0][i] = duplicates[edge]

        for node in delete_nodes:
            self.graph[duplicates[node]] = self.graph[node]
            del self.graph[node]

    def convert_graph(self):
        if len(self.graph) and isinstance(self.graph, dict):
            key = list(self.graph.keys())[0]
            if isinstance(self.graph[key], tuple):
                for doc, (edges, counts) in self.graph.items():
                    self.graph[doc] = {e:c for e, c in zip(edges, counts)}
            elif isinstance(self.graph[key], dict):
                for doc, edge_count in self.graph.items():
                    self.graph[doc] = (list(edge_count.keys()), list(edge_count.values()))
            else:
                raise Exception("Invalid graph format.")

    def remove_dead(self, id_to_title):
        delete_nodes = []
        for product_id, (edges, counts) in self.graph.items():
            active_edges = list()
            active_counts = list()

            if product_id in id_to_title and id_to_title[product_id]:
                while edges:
                    edge = edges.pop()
                    count = counts.pop()

                    if edge in id_to_title and id_to_title[edge]:
                        active_edges.append(edge)
                        active_counts.append(count)

                if len(active_edges):
                    self.graph[product_id] = (active_edges, active_counts)
                else:
                    delete_nodes.append(product_id)
            else:
                delete_nodes.append(product_id)

        for node in delete_nodes:
            del self.graph[node]
        return None


