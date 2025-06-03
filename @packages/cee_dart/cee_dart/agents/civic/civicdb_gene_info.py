import requests
"""
Module for retrieving and processing gene information from the CivicDB API.
This module provides functionality to:
- Fetch minimal gene details (name, fullName, myGeneInfoDetails) from CivicDB using gene IDs
- Process the retrieved information into a pandas DataFrame with extracted fields
Classes:
    CivicDbGeneInfo: Handles API interaction with CivicDB for a single gene
Functions:
    process_gene_infos: Processes multiple genes and combines results into a DataFrame
Example:
    python
    # Get information for specific gene IDs
    gene_ids = [1, 2, 3]  # Example gene IDs
    gene_info_df = process_gene_infos(gene_ids)
"""
import json

class CivicDbGeneInfo:
    """Class to fetch minimal gene details: myGeneInfoDetails, fullName, and name."""

    def __init__(self, gene_id, endpoint="https://civicdb.org/api/graphql"):
        """Initialize a CivicDB Genes fetcher for a specific gene.

        Parameters:
        ----------
        gene_id : int
            The ID of the gene to fetch information for from CivicDB.
        endpoint : str, optional
            The URL of the CivicDB GraphQL API endpoint.
            Default is "https://civicdb.org/api/graphql".

        Attributes:
        ----------
        gene_id : int
            The stored gene ID.
        endpoint : str
            The GraphQL API endpoint to query.
        query : str
            The GraphQL query template to fetch gene information."""
        
        self.gene_id = gene_id
        self.endpoint = endpoint
        self.query = """
        {
            gene(
                id: %d
            ) {
                myGeneInfoDetails,
                fullName,
                name
            }
        }
        """

    def fetch_gene_info(self):
        """
        Fetches gene information from the CivicDB API using the stored gene_id.
        This method sends a POST request to the CivicDB endpoint with a GraphQL query
        that includes the gene_id. The query format is defined in the class initialization.
        Returns:
            dict: Gene information if successful, including various annotations and metadata
                  from CivicDB. Returns an empty dictionary if the request fails.
        Prints:
            Success or failure messages, including any API errors that might occur.
        """
        formatted_query = self.query % self.gene_id
        response = requests.post(self.endpoint, data={"query": formatted_query}).json()

        if "data" in response and response["data"].get("gene"):
            gene_info = response["data"]["gene"]
            print(f"Retrieved gene info for gene ID {self.gene_id}")
            return gene_info
        else:
            print(f"Failed to retrieve gene info for gene ID: {self.gene_id}")
            if "errors" in response:
                print(f"API Errors: {response['errors']}")
            return {}

def process_gene_infos(gene_ids):
    """
    Process multiple genes and generate a combined DataFrame with minimal gene information.
    This function fetches gene information for multiple gene IDs using the CivicDbGeneInfo class,
    combines the results into a pandas DataFrame, and processes nested JSON data in the 'myGeneInfoDetails'
    field to extract summaries and protein domain information into separate columns.
    Parameters
    ----------
    gene_ids : list
        A list of gene IDs to process
    Returns
    -------
    pandas.DataFrame
        DataFrame containing processed gene information with columns:
        - gene_id: The original gene ID
        - summary: Gene summary extracted from myGeneInfoDetails
        - Protein_Domains: List of protein domain descriptions
        
    Notes
    -----
    The function handles JSON parsing for 'myGeneInfoDetails' and removes this column
    from the final DataFrame after extracting the relevant information.
    """
    results = []
    for gene_id in gene_ids:
        gene_info_obj = CivicDbGeneInfo(gene_id)
        info = gene_info_obj.fetch_gene_info()
        if info:
            info["gene_id"] = gene_id
            results.append(info)
    import pandas as pd

    df = pd.DataFrame(results)
    # Process 'myGeneInfoDetails': parse JSON and extract 'summary' and 'Protein Domains' into separate columns
    if "myGeneInfoDetails" in df.columns:
        df["myGeneInfoDetails"] = df["myGeneInfoDetails"].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )
        df["summary"] = df["myGeneInfoDetails"].apply(
            lambda d: d.get("summary") if isinstance(d, dict) else None
        )
        # Extract 'Protein Domains': if 'interpro' is a list, join all 'desc' values; if dict, use its 'desc'
        df["Protein_Domains"] = (
            df["myGeneInfoDetails"]
            .apply(lambda d: d.get("interpro"))
            .apply(lambda x: [y["desc"] for y in x] if isinstance(x, list) and all(isinstance(y, dict) for y in x) else [])
        )
        df = df.drop(columns=["myGeneInfoDetails"])
    return df
