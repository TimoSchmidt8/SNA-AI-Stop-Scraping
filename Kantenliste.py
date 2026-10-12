import json
import pandas as pd

# Exakter Pfad zur bereinigten JSON-Datei im Unterordner 'data cleared'
input_json = (
    '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
    ' Scraping/data/data cleared/unique_tweets_cleaned.json'
)

# Einlesen der bereinigten Daten
with open(input_json, 'r', encoding='utf-8') as f:
  tweets = json.load(f)

print(f'{len(tweets)} bereinigte Tweets geladen. Extrahiere Kanten...')

edges = []

# Interaktionen extrahieren (Replies, Quotes, Mentions)
for tweet in tweets:
  author_dict = tweet.get('author', {})
  source = (
      author_dict.get('userName') if isinstance(author_dict, dict) else None
  )
  if not source:
    continue

  # 1. Replies (Antworten)
  in_reply_to = tweet.get('inReplyToUsername')
  if in_reply_to and in_reply_to != source:
    edges.append({'source': source, 'target': in_reply_to, 'type': 'reply'})

  # 2. Quotes (Zitate)
  quote = tweet.get('quote')
  if isinstance(quote, dict):
    q_author = quote.get('author', {})
    if isinstance(q_author, dict):
      q_username = q_author.get('userName')
      if q_username and q_username != source:
        edges.append({'source': source, 'target': q_username, 'type': 'quote'})

  # 3. Mentions (Erwähnungen im Text)
  entities = tweet.get('entities', {})
  if isinstance(entities, dict):
    mentions = entities.get('user_mentions', [])
    if isinstance(mentions, list):
      for mention in mentions:
        if isinstance(mention, dict):
          m_screen = mention.get('screen_name')
          if m_screen and m_screen != source:
            edges.append(
                {'source': source, 'target': m_screen, 'type': 'mention'}
            )

# In DataFrame umwandeln
edges_df = pd.DataFrame(edges)

if not edges_df.empty:
  # Kanten aggregieren und Gewichte berechnen
  network_edges = (
      edges_df.groupby(['source', 'target']).size().reset_index(name='weight')
  )

  # Speichern als CSV im selben Ordner wie die JSON-Datei
  output_csv = (
      '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
      ' Scraping/data/data cleared/network_edges.csv'
  )
  network_edges.to_csv(output_csv, index=False)

  print(
      f'Erfolgreich! {len(network_edges)} eindeutige Kanten gespeichert unter:'
      f' \n{output_csv}'
  )
  print('\nVorschau:')
  print(network_edges.head(10))
else:
  print('Keine Kanten im Datensatz gefunden.')