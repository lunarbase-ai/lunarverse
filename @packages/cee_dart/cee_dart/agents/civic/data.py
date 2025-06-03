
def contains_node(feature_aliases, nodes):
    return any(node in alias for alias in feature_aliases for node in nodes)

import requests
import json
import pandas as pd


def get_evidence_items(evidence_ids, first=500):
    """
    Query the CIViC API for evidence items given a list of evidence item IDs.
    The parameter 'first' is set to 500 so up to 500 results are returned in one query.
    """
    API_URL = "https://civicdb.org/api/graphql"

    # GraphQL query for retrieving evidence items.
    # In this example we ask only for a few fields; you can extend this as needed.
    QUERY_EVIDENCE_ITEMS = """
    query evidenceItems(
      $first: Int,
      $ids: [Int!]
    ) {
      evidenceItems(
        first: $first,
        ids: $ids
      ) {
        edges {
          node {
            id
            name
            description
          }
        }
        nodes {
          id
          name
          description
        }
        totalCount
      }
    }
    """
    headers = {"Content-Type": "application/json"}
    variables = {"first": first, "ids": evidence_ids}
    
    response = requests.post(API_URL, json={"query": QUERY_EVIDENCE_ITEMS, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def get_json_results(evidence_ids, first = 100):
      try:
          result = get_evidence_items(evidence_ids, first)
          print("Evidence Items found:", len(result['data']['evidenceItems']['edges']))
          results = json.dumps(result, indent=2)
          return results
      except Exception as e:
          print("Error retrieving evidence items:", e)


class CivicData:
    """
    A class to handle and process civic data including features, molecular profiles, and evidence.
    Attributes:
        features_path (str): Path to the features data file.
        mp_path (str): Path to the molecular profiles data file.
        features (pd.DataFrame): DataFrame containing features data.
        mp (pd.DataFrame): DataFrame containing molecular profiles data.
        evidence (pd.DataFrame): DataFrame containing evidence data.
        features_matching (pd.DataFrame): DataFrame containing features matching nodes.
        mps_matching (pd.DataFrame): DataFrame containing molecular profiles matching nodes.
        mps_summaries (list): List of summaries for molecular profiles.
        features_descriptions (list): List of descriptions for features.
        evidence_df (pd.DataFrame): DataFrame containing evidence item IDs and descriptions.
        all_facts (list): List of all aggregated facts.
    Methods:
        load_data():
            Loads the features and molecular profiles data from the specified paths.
        get_features_matching_nodes(diff_graph):
            Finds and stores features that match nodes in the given diff_graph.
        get_molecular_profiles_matching_nodes(diff_graph):
            Finds and stores molecular profiles that match nodes in the given diff_graph.
        get_mps_summaries():
            Generates and stores summaries for the matched molecular profiles.
        get_features_descriptions():
            Generates and stores descriptions for the matched features.
        get_evidence_ids_df():
            Generates a DataFrame of evidence item IDs for the matched molecular profiles.
        get_evidence_descriptions():
            Fetches and stores descriptions for the evidence items.
        agragate_all_facts():
            Aggregates all facts from features descriptions, molecular profiles summaries, and evidence descriptions.
    """
    def __init__(self, features_path, mp_path):
        """
        Initializes the class with the given file paths.

        Args:
            features_path (str): The path to the features file.
            mp_path (str): The path to the mp file.

        Attributes:
            features_path (str): The path to the features file.
            mp_path (str): The path to the mp file.
            features (None): Placeholder for features data.
            mp (None): Placeholder for mp data.
            evidence (None): Placeholder for evidence data.
        """
        self.features_path = features_path
        self.mp_path = mp_path
        self.features = None
        self.mp = None
        self.evidence = None


    def load_data(self):
        """
        Loads data from specified file paths and processes the data.
        This method performs the following steps:
        1. Reads the features data from a tab-delimited file specified by `self.features_path`.
        2. Joins the 'name' and 'feature_aliases' columns into a new 'names' column in the features DataFrame.
        3. Reads the mp data from a tab-delimited file specified by `self.mp_path`.
        4. Joins the 'name' and 'aliases' columns into a new 'names' column in the mp DataFrame.
        
        Attributes:
            features (pd.DataFrame): DataFrame containing the features data with an additional 'names' column.
            mp (pd.DataFrame): DataFrame containing the mp data with an additional 'names' column.
        """
        def join_name_and_aliases(df, name_column='name', aliases_column='feature_aliases'):
            df['names'] = df[aliases_column].fillna('') + ',' + df[name_column].fillna('')

        self.features = pd.read_csv(self.features_path, delimiter="\t")
        join_name_and_aliases(df = self.features, name_column='name', aliases_column='feature_aliases')
        self.mp = pd.read_csv(self.mp_path, delimiter="\t")
        join_name_and_aliases(df = self.mp, name_column='name', aliases_column='aliases')
        
        
    def get_features_matching_nodes(self, diff_graph):
        """
        Filters and matches features based on nodes present in the given diff_graph.

        This method updates the `features_matching` attribute with a DataFrame containing
        features whose 'names' contain any node from `diff_graph.node_names_no_type`.
        It also adds a 'matched_node' column to the DataFrame, indicating the first matched
        node found in each feature's 'names'.

        Args:
            diff_graph (nx.Graph): An instance of nx.Graph containing the set of node names
                                    to match against the features.

        Returns:
            None
        """
        self.features_matching = self.features[self.features['names'].apply(lambda x: contains_node(x.split(','), diff_graph.node_names_no_type))].reset_index(drop=True)
        self.features_matching['matched_node'] = self.features_matching['names'].apply(lambda x: next((node for node in diff_graph.node_names_no_type if node in x), None))

    def get_molecular_profiles_matching_nodes(self, diff_graph):
        """
        Filters molecular profiles that match nodes in the given differential graph.

        This method updates the `mps_matching` attribute with a DataFrame containing
        molecular profiles whose 'names' contain any of the node names from the 
        `diff_graph`'s `node_names_no_type`. It also adds a 'matched_node' 
        column to the DataFrame, indicating the first matching node found in each 
        profile's 'names'.

        Args:
            diff_graph (nx.Graph): A differential graph object that contains a set of 
                                node names (`node_names_no_type`).

        Returns:
            None
        """
        self.mps_matching = self.mp[self.mp['names'].apply(lambda x: contains_node(x.split(','), diff_graph.node_names_no_type))].reset_index(drop=True)
        self.mps_matching['matched_node'] = self.mps_matching['names'].apply(lambda x: next((node for node in diff_graph.node_names_no_type if node in x), None))

    def get_mps_summaries(self):
        """
        Generates a list of MPS summaries by concatenating a fact-related string with the matched node and summary from the mps_matching DataFrame.

        This method updates the `mps_summaries` attribute with a list of strings. Each string is formed by concatenating the phrase 
        '[Fact related to ' with the 'matched_node' value and the 'summary' value from the `mps_matching` DataFrame, excluding any 
        rows with NaN values.

        Returns:
            None
        """
        self.mps_summaries = list(('[Fact related to ' + self.mps_matching['matched_node'] + '] ' + self.mps_matching['summary']).dropna().values)

    def get_features_descriptions(self):
        """
        Generates a list of feature descriptions by concatenating a fixed string with the 'matched_node' and 'description' 
        fields from the 'features_matching' DataFrame, excluding any NaN values.

        Attributes:
            features_descriptions (list): A list of formatted feature descriptions.
        """
        self.features_descriptions = list(('[Fact related to ' + self.features_matching['matched_node'] + '] ' + self.features_matching['description']).dropna().values)

    def get_evidence_ids_df(self):
        """
        Processes the 'mps_matching' DataFrame to extract and transform evidence item IDs.

        This method groups the 'mps_matching' DataFrame by the 'matched_node' column and aggregates
        the 'evidence_item_ids' for each group. It then splits and cleans these IDs, ensuring they
        are unique and properly formatted. The resulting DataFrame is stored in the 'evidence_df' attribute.

        Returns:
            None
        """
        self.evidence_df = self.mps_matching.groupby('matched_node')['evidence_item_ids'].apply(lambda x: list(set(','.join(x.dropna()).replace(' ', '').split(',')))).reset_index(name='evidence_item_id').explode('evidence_item_id').reset_index(drop=True)
        self.evidence_df ['evidence_item_id'] = self.evidence_df ['evidence_item_id'].astype('int')


    def get_evidence_desctiptions(self):
        """
        Retrieves evidence descriptions and updates the evidence DataFrame.
        This method processes evidence items in batches of 100, retrieves their descriptions
        from an external source, and merges the results with the existing evidence DataFrame.
        It also updates the 'description' column to include a fact related to the matched node.
        Returns:
            None
        """
        all_results = pd.DataFrame()
        evidence_ids = self.evidence_df['evidence_item_id'].to_list()
        for i in range(0, len(evidence_ids), 100):
            batch_ids = evidence_ids[i:i + 100]
            result = get_json_results(batch_ids, first=100)
            evidence_items_dict = json.loads(result)
            evidence_df = pd.DataFrame.from_dict(evidence_items_dict['data']['evidenceItems']['edges'])
            evidence_df = pd.json_normalize(evidence_df['node'])
            all_results = pd.concat((all_results, evidence_df))
            
        self.evidence_df  =self.evidence_df.merge(all_results, left_on='evidence_item_id', right_on='id')
        self.evidence_df['description'] = '[Fact related to ' + self.evidence_df['matched_node'] + '] ' + self.evidence_df['description']


    def agragate_all_facts(self):
        """
        Aggregates all facts from features descriptions, MPS summaries, and evidence descriptions.
        
        This method combines the lists `features_descriptions`, `mps_summaries`, and the 'description' column 
        from the `evidence_df` DataFrame into a single list `all_facts`. The combined list is then sorted 
        in ascending order.
        
        Attributes:
            features_descriptions (list): A list of feature descriptions.
            mps_summaries (list): A list of MPS summaries.
            evidence_df (DataFrame): A DataFrame containing evidence data with a 'description' column.
            all_facts (list): A list that will contain all aggregated and sorted facts.
        """
        self.all_facts = self.features_descriptions + self.mps_summaries + self.evidence_df['description'].to_list()
        self.all_facts.sort()