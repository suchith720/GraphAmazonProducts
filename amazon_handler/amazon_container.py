from .amazon_graph import *


def extract_similar_items(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    header = soup.find('tr')

    similar_products = []

    if header:
        for th in header.find_all('th'):
            product_html = th.find('span')
            if len(product_html['class']) == 1 and product_html['class'][0] == 'a-size-base':
                similar_products.append(product_html.get_text())

    return similar_products


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield json.loads(l)


"""
AmazonGraphContainer is a container that to stores all the graph related
information.
"""
class AmazonGraphContainer:

    def __init__(self):
        """
        Amazon graphs.
        """
        self.graphs = {}
        self.graphs['similar'] = AmazonGraph()
        self.graphs['also_buy'] = AmazonGraph()
        self.graphs['also_view'] = AmazonGraph()

        """
        Map from prod_id to title.
        """
        self.id_to_title = {}

        """
        Store product description.
        """
        self.description = {}

    def convert_graph(self, graph_type="all"):
        graph_types = []
        if graph_type == "all":
            graph_types = ['similar', 'also_buy', 'also_view']
        else:
            graph_types.append(graph_type)

        for graph_type in graph_types:
            self.graphs[graph_type].convert_graph()

    def create_graph(self, filename, limit=None):
        for i, product in enumerate(parse(filename)):

            similar_items = extract_similar_items(product['similar_item'])

            if len(product['also_view']) or len(product['also_buy']) or len(similar_items):
                product_id = product['asin']

                self.id_to_title[product_id] = product['title']

                if len(product['also_view']):
                    self.graphs['also_view'].add_product(product_id, product['also_view'])
                if len(product['also_buy']):
                    self.graphs['also_buy'].add_product(product_id, product['also_buy'])
                if len(similar_items):
                    self.graphs['similar'].add_product(product_id, similar_items)

                self.description[product_id] = product['description']

            if limit is not None and i > limit:
                break

    def replace_similar_graph_titles(self):
        nodes_to_delete = []
        title_to_id = { product_title:product_id for product_id, product_title in self.id_to_title.items() }

        for node, (title_edges, count_edges) in self.graphs['similar'].graph.items():
            id_edges, new_count_edges = [], []
            for i, edge in enumerate(title_edges):
                if edge in title_to_id:
                    id_edges.append(title_to_id[edge])
                    new_count_edges.append(count_edges[i])

            if not len(id_edges):
                nodes_to_delete.append(node)
            else:
                self.graphs['similar'].graph[node] = (id_edges, new_count_edges)

        for node in nodes_to_delete:
            del self.graphs['similar'].graph[node]

    def replace_graph_duplicates(self, duplicates, graph_type='all'):
        graph_types = []
        if graph_type == "all":
            graph_types = ['similar', 'also_buy', 'also_view']
        else:
            graph_types.append(graph_type)

        for graph_type in graph_types:
            self.graphs[graph_type].replace_duplicates(duplicates)

    def save_graph(self, save_dir, tag='', graph_type='similar'):
        if graph_type != 'similar' and graph_type != 'also_buy' and graph_type != 'also_view':
            raise Exception("graph_type should be in ['similar', 'also_buy', 'also_view']")

        self.graphs[graph_type].save_data(save_dir, tag=f'_{graph_type}{tag}')

    def save_graphs(self, save_dir, tag=''):
        graph_types = ['similar', 'also_view', 'also_buy']

        for graph_type in graph_types:
            self.save_graph(save_dir, tag=tag, graph_type=graph_type)

    def save_idtotitle(self, save_dir, tag=''):
        map_file = f'{save_dir}/id_to_title{tag}.pickle'
        with open(map_file, 'wb') as f:
            pickle.dump(self.id_to_title, f)
        del self.id_to_title
        gc.collect()

    def save_description(self, save_dir, tag=''):
        content_file = f'{save_dir}/description{tag}.pickle'
        with open(content_file, 'wb') as f:
            pickle.dump(self.description, f)
        del self.description
        gc.collect()

    def save_data(self, save_dir, tag=''):
        os.makedirs(save_dir, exist_ok=True)

        self.save_graphs(save_dir, tag)
        self.save_idtotitle(save_dir, tag)
        self.save_description(save_dir, tag)

    def load_graph(self, save_dir, tag='', graph_type='similar'):
        if graph_type != 'similar' and graph_type != 'also_buy' and graph_type != 'also_view':
            raise Exception("graph_type should be in ['similar', 'also_buy', 'also_view']")

        if not self.graphs[graph_type].load_data(save_dir, tag=f'_{graph_type}{tag}'):
            raise Exception(f"Unable to load '{graph_type} graph'.")

    def load_graphs(self, save_dir, tag=''):
        graph_types = ['similar', 'also_view', 'also_buy']

        for graph_type in graph_types:
            self.load_graph(save_dir, tag=tag, graph_type=graph_type)

    def load_idtotitle(self, save_dir, tag=''):
        map_file = f'{save_dir}/id_to_title{tag}.pickle'
        if os.path.exists(map_file):
            with open(map_file, 'rb') as f:
                self.id_to_title = pickle.load(f)
        else:
            raise Exception(f"Unable to load 'id_to_title' from '{map_file}'.")

    def load_description(self, save_dir, tag=''):
        content_file = f'{save_dir}/description{tag}.pickle'
        if os.path.exists(content_file):
            with open(content_file, 'rb') as f:
                self.description = pickle.load(f)
        else:
            raise Exception(f"Unable to load 'description' from '{content_file}'.")

    def load_data(self, save_dir, tag=''):
        self.load_graphs(save_dir, tag)
        self.load_idtotitle(save_dir, tag)
        self.load_description(save_dir, tag)

