import json
import pandas as pd

# Absoluter Pfad zur bereinigten JSON-Datei
input_json = (
    '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt Scraping/data/data cleared/unique_tweets_cleaned2.json'
)

# 1. Bereinigte JSON einlesen
with open(input_json, 'r', encoding='utf-8') as f:
  tweets = json.load(f)

print(f'{len(tweets)} Tweets geladen. Extrahiere Kanten für Gephi...')

edges = []

# 2. Durch alle Tweets iterieren und Interaktionen extrahieren
for tweet in tweets:
  author_dict = tweet.get('author', {})
  source = (
      author_dict.get('userName') if isinstance(author_dict, dict) else None
  )
  if not source:
    continue

  # A. Replies (Antworten)
  in_reply_to = tweet.get('inReplyToUsername')
  if in_reply_to and in_reply_to != source:
    edges.append({'source': source, 'target': in_reply_to, 'type': 'reply'})

  # B. Quotes (Zitierte Tweets)
  quote = tweet.get('quote')
  if isinstance(quote, dict):
    q_author = quote.get('author', {})
    if isinstance(q_author, dict):
      q_username = q_author.get('userName')
      if q_username and q_username != source:
        edges.append({'source': source, 'target': q_username, 'type': 'quote'})

  # C. Mentions (@Erwähnungen im Text)
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

# 3. In DataFrame umwandeln
edges_df = pd.DataFrame(edges)

if not edges_df.empty:
  # 4. Kanten zusammenfassen und Gewicht (Weight) berechnen
  network_edges = (
      edges_df.groupby(['source', 'target']).size().reset_index(name='weight')
  )

  # 5. Speichern als CSV für Gephi
  output_csv = (
      '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
      ' Scraping/data/network_edges.csv'
  )
  network_edges.to_csv(output_csv, index=False)

  print(
      f'Erfolgreich! {len(network_edges)} eindeutige Kanten gespeichert unter:\n'
      f'{output_csv}'
  )
  print('\nVorschau der ersten Kanten:')
  print(network_edges.head(10))
else:
  print('Keine Kanten gefunden.')