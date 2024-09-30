# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import io
from typing import Optional, Any, Union, List, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class CausalGraphViewer(
    BaseComponent,
    component_name="Causal Graph Viewer",
    component_description="""
    Displays JSON serializable graph (node-link format)
    Output (img): binary map""",
    input_types={"graph": DataType.JSON, "name": DataType.TEXT},
    output_type=DataType.ANY,
    component_group=ComponentGroup.DATA_VISUALIZATION,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, graph: Dict, name: str):
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes
        for node in graph["nodes"]:
            G.add_node(node["id"])
        # Add edges
        for link in graph["links"]:
            if "weight" in link.keys():
                if link["weight"] != -1:
                    G.add_edge(link["source"], link["target"], **link)
            else:
                G.add_edge(link["source"], link["target"], **link)

        # Get the list of nodes in the order they appear in the graph
        nodes = list(G.nodes.keys())
        # Sort nodes by alphabetic order
        nodes.sort()

        # Create the adjacency matrix using the node order
        adj_matrix = nx.to_numpy_array(G, nodelist=nodes, dtype=int)

        fig, ax = plt.subplots(figsize=(12, 10))

        im = ax.imshow(adj_matrix, cmap="binary")

        ax.set_title(f"Binary Map - {name}")
        ax.set_xlabel("Influenced Variables")
        ax.set_ylabel("Potential Causal Factors")

        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Edge Presence", rotation=-90, va="bottom")
        fig.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Convert the BytesIO buffer to a base64-encoded PNG string URL
        import base64

        png_string_url = (
            f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"
        )

        # Close the plot to free resources
        plt.close()

        return {"base64Image": png_string_url, "name": name}
