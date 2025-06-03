import pandas as pd
import numpy as np
import logging
import ast
import json

logging.basicConfig(level=logging.INFO)


class CivicEvidenceAnalyzer:
    def __init__(self, path, gene_list):
        """
        Initializes the class with the given path and gene list, and loads several CSV files into pandas DataFrames.
        Args:
            path (str): The file path where the CSV files are located.
            gene_list (list): A list of genes to be used in the analysis.
        Attributes:
            path (str): The file path where the CSV files are located.
            gene_list (list): A list of genes to be used in the analysis.
            features (pd.DataFrame): DataFrame containing features from 'civic_all_features_simple.csv'.
            profiles (pd.DataFrame): DataFrame containing molecular profiles from 'civic_all_molecular_profiles_simple.csv'.
            gene_info (pd.DataFrame): DataFrame containing gene information from 'civic_gene_info.csv'.
            civic_map (pd.DataFrame): DataFrame containing civic map data from 'civic_map.csv'.
            feature_details_dict (dict or None): Dictionary to store feature details, initialized as None.
            matching_features (list or None): List to store matching features, initialized as None.
        """

        self.path = path
        self.gene_list = gene_list
        self.features = pd.read_csv(path + r'/civic_all_features_simple.csv')
        self.profiles = pd.read_csv(path + r'/civic_all_molecular_profiles_simple.csv')
        self.gene_info = pd.read_csv(path + r'/civic_gene_info.csv')
        # self.evidence = pd.read_csv(path + r'\civic_all_evidence_simple.csv')
        self.civic_map = pd.read_csv(path + r'/civic_map.csv').fillna(-1).astype(int)
        self.feature_details_dict = None
        self.matching_features = None

    def contains_gene(self, aliases):
        """
        Check if any gene from self.gene_list is present in the provided aliases.

        Parameters:
        aliases (list or str): A list of gene aliases or a string representation of a list of gene aliases.

        Returns:
        bool: True if any gene from self.gene_list is found in aliases, False otherwise.

        """
        if isinstance(aliases, list):
            return any(gene in aliases for gene in self.gene_list)
        elif isinstance(aliases, str):
            try:
                alias_list = ast.literal_eval(aliases)
                return any(gene in alias_list for gene in self.gene_list)
            except Exception:
                return any(gene == aliases for gene in self.gene_list)
        else:
            return False

    def filter_features(self):
        """
        Filters the features based on the presence of a gene in their aliases.
        This method applies a filter to the 'aliases' column of the features DataFrame,
        retaining only the rows where the 'aliases' contain a gene as determined by the
        `contains_gene` method.
        Returns:
            DataFrame: A DataFrame containing only the features that match the gene criteria.
        """

        mask = self.features["aliases"].apply(lambda x: self.contains_gene(x))
        self.matching_features = self.features[mask]
        return self.matching_features

    def create_feature_details_dict(self):
        """
        Creates a dictionary containing detailed information about features.
        This method filters features and constructs a dictionary where each key is a feature name and the value is another
        dictionary containing the following details:
            - Description: A description of the feature.
            - Summary: A summary of the gene associated with the feature.
            - Molecular_profiles: A list of summaries of molecular profiles associated with the gene.
        Returns:
            dict: A dictionary with feature names as keys and their details as values.
        """

        self.filter_features()
        feature_details_dict = {}
        for _, row in self.matching_features.iterrows():
            fname = row["feature_name"]
            desc = row["description"]
            gene_id = row["feature_id"]
            profiles_ids = self.civic_map.loc[
                self.civic_map["gene_id"] == gene_id, "molecular_profile_id"
            ].tolist()
            # print(fname, ', Profiles Ids: ', profiles_ids)
            summary_val = self.gene_info.loc[
                self.gene_info["gene_id"] == gene_id, "summary"
            ]

            # repalce NaN with None (for later JSON conversion)
            summary = summary_val.values[0] if not summary_val.empty else None
            desc = desc if pd.notna(desc) else None

            feature_details_dict[fname] = {
                "Description": desc,
                "Summary": summary,
                "Molecular_profiles": self.profiles.loc[
                    self.profiles["molecular_profile_id"].isin(profiles_ids), "summary"
                ]
                .dropna()                
                .tolist(),
                # Evidence field will be added separately
            }
        self.feature_details_dict = feature_details_dict
        return feature_details_dict

    def add_evidence_to_dict(self):
        """
        Adds evidence information to the feature details dictionary.
        This method reads evidence data from a CSV file and matches it with features
        in the `matching_features` DataFrame. It then updates the `feature_details_dict`
        with the corresponding evidence details as dictionaries.
        Returns:
            dict: Updated feature details dictionary with added evidence information,
                  or None if `feature_details_dict` is not defined.
        Raises:
            Warning: If `feature_details_dict` is not defined, a warning is logged.
        """

        if not self.feature_details_dict:
            logging.warning(
                "feature_details_dict is not defined. Call create_feature_details_dict first."
            )
            return None

        evidence = pd.read_csv(self.path + r'/civic_all_evidence_simple.csv')
        evidence["pmid"] = pd.to_numeric(evidence["pmid"], errors="coerce").fillna(-1).astype(int)
        evidence["rating"] = pd.to_numeric(evidence["rating"], errors="coerce").fillna(-1).astype(int)

        for _, row in self.matching_features.iterrows():
            fname = row["feature_name"]
            gene_id = row["feature_id"]
            evidence_ids = self.civic_map.loc[
                self.civic_map["gene_id"] == gene_id, "evidence_id"
            ].tolist()
            evidence_details = (
                evidence.loc[
                    evidence["evidence_id"].isin(evidence_ids),
                    [
                        "statement",
                        "evidence_level",
                        "rating",
                        "evidence_type",
                        "evidence_direction",
                        "significance",
                        "variant_origin",
                        "evidence_name",
                        "source",
                        "pmid",
                    ],
                ]
                .dropna()
                
            )
            # replace NaN values with None for JSON conversion
            evidence_details = evidence_details.where(~pd.isna(evidence_details), None)
            
            evidence_details = evidence_details.to_dict("records")
            if fname in self.feature_details_dict:
                self.feature_details_dict[fname]["Evidence"] = evidence_details
        return self.feature_details_dict

    def verbalize_civicdb_knowledge(self):
        civicdb_knowledge = ""

        for feature, details in self.feature_details_dict.items():

            civicdb_knowledge += f"Feature: {feature}\n"
            civicdb_knowledge += f"Description: {details['Description']}\n"
            civicdb_knowledge += f"Summary: {details['Summary']}\n"
            if "Molecular_profiles" in details:
                civicdb_knowledge += "Molecular Profiles:\n"
                for profile in details["Molecular_profiles"]:
                    civicdb_knowledge += f"\t- {profile}\n"
            if "Evidence" in details:
                civicdb_knowledge += "Evidence:\n"
                for evidence in details["Evidence"]:
                    civicdb_knowledge += f"\t- {evidence}\n"
            civicdb_knowledge += "_______________\n"

        self.civicdb_knowledge = civicdb_knowledge
        return civicdb_knowledge

    def to_json(self):
        """
        Convert the feature details dictionary to a JSON formatted string.
        This method converts the `feature_details_dict` attribute to a JSON formatted string
        and stores it in the `json_feature_details` attribute. If `feature_details_dict` is
        not defined, a warning is logged and the method returns None. NaN values are converted
        to None in the JSON output.
        Returns:
            str: A JSON formatted string representation of `feature_details_dict` if it is defined.
            None: If `feature_details_dict` is not defined.
        """

        if self.feature_details_dict is None:
            logging.warning(
                "feature_details_dict is not defined. Call create_feature_details_dict first."
            )
            return None

        # Replace NaN values with None in the dictionary
        sanitized_dict = json.loads(
            json.dumps(self.feature_details_dict, default=lambda x: None if pd.isna(x) else x)
        )

        self.json_feature_details = json.dumps(sanitized_dict, indent=4)
        return self.json_feature_details

    def save_json_to_file(self, directory_path):
        """
        Save the JSON feature details to a file with a proper name.
        Args:
            directory_path (str): The directory path where the JSON file will be saved.
        Returns:
            None
        Logs:
            - A warning if `json_feature_details` is not defined.
            - An info message indicating the file path where the JSON data was saved.
        """

        if self.json_feature_details is None:
            logging.warning("json_feature_details is not defined. Call to_json first.")
            return None

        file_name = "civic_feature_details.json"
        file_path = f"{directory_path}/{file_name}"

        with open(file_path, "w") as json_file:
            json_file.write(self.json_feature_details)
        logging.info(f"JSON data saved to {file_path}")


# Example usage:
# analyzer = CivicEvidenceAnalyzer(r'C:\Users\owysocky\Documents\GitHub\CCE_scGeneRAI\resources\civicdb', ['ALK', 'BRCA1', 'EGFR', 'KRAS', 'PIK3CA'])
# details_dict = analyzer.create_feature_details_dict()
# details_dict = analyzer.add_evidence_to_dict()
