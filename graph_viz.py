import networkx as nx
import matplotlib.pyplot as plt

def build_graph(links_dict):
    """
    links_dict: dict[str, list[str]]
    Example:
        {
            "https://example.com": [
                "https://example.com/about",
                "https://example.com/contact"
            ],
            "https://example.com/about": [
                "https://example.com/team"
            ]
        }
    """
    G = nx.DiGraph()

    for src, targets in links_dict.items():
        for dst in targets:
            G.add_edge(src, dst)

    return G


def draw_graph(G, output_path="site_graph.png"):
    plt.figure(figsize=(14, 10))

    # Layout algorithm for nice spacing
    pos = nx.spring_layout(G, k=0.6, iterations=40)

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=600,
        node_color="#4C72B0",
        alpha=0.9
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        arrowstyle="->",
        arrowsize=15,
        edge_color="#555555",
        width=1.2
    )

    # Labels (URLs can be long, so feel free to shorten)
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Graph saved to {output_path}")
