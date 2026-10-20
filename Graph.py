import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# 1. Kantenliste laden
df = pd.read_csv('network_edges.csv')

# 2. Graphen aufbauen
G = nx.DiGraph()
for _, row in df.iterrows():
  G.add_edge(row['source'], row['target'], weight=row['weight'])

# 3. Reziproke Kanten identifizieren
edge_set = set(zip(df['source'], df['target']))
reciprocal_pairs = []
for u, v in edge_set:
  if (v, u) in edge_set and u < v:
    reciprocal_pairs.append((u, v))

# 4. Plot im Klier-Stil (Schwarz-Weiß) erstellen
fig, ax = plt.subplots(figsize=(16, 12))
pos = nx.spring_layout(G, seed=42, k=0.12, iterations=60)

# Alle Knoten in schlichtem Schwarz
nx.draw_networkx_nodes(G, pos, node_color='black', node_size=15, alpha=0.8, ax=ax)

# Alle normalen Kanten in dünnem Schwarz/Grau
nx.draw_networkx_edges(
    G, pos, width=0.3, edge_color='black', alpha=0.15, arrows=False, ax=ax
)

# Reziproke Kanten als deutliche geschwungene Pfeile (Bögen)
recip_edges_full = []
for u, v in reciprocal_pairs:
  recip_edges_full.append((u, v))
  recip_edges_full.append((v, u))

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=recip_edges_full,
    width=1.5,
    edge_color='black',
    alpha=0.9,
    connectionstyle='arc3, rad=0.25',
    arrows=True,
    arrowsize=8,
    ax=ax,
)

# Reziproke Knoten mit weißer Füllung und schwarzem Rand hervorheben
recip_nodes = set([n[0] for n in reciprocal_pairs] + [n[1] for n in reciprocal_pairs])
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=list(recip_nodes),
    node_color='white',
    edgecolors='black',
    node_size=60,
    linewidths=1.5,
    ax=ax,
)

# Beschriftung nur für die reziproken Knoten
recip_labels = {n: n for n in recip_nodes}
nx.draw_networkx_labels(
    G,
    pos,
    labels=recip_labels,
    font_size=8,
    font_weight='bold',
    font_color='black',
    ax=ax,
)

ax.set_title(
    'Interaktionsgraph zu den AI-Tweets (Reziproke Schleifen)',
    fontsize=14,
    fontweight='bold',
    pad=20,
)
ax.axis('off')

# Speichern
output_path = '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt Scraping/data/data cleared/network_klier_style.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'Grafik im Klier-Stil erfolgreich gespeichert unter:\n{output_path}')