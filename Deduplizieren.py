import json
import pandas as pd

# 1. Exakte Pfade zu allen 9 JSON-Dateien in den jeweiligen RUN-Ordnern
json_files = [
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 1/1_dataset_tweet-scraper_2026-10-12_10-10-25-485.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 2/2_dataset_tweet-scraper_2026-10-12_10-25-16-990.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 3/3_dataset_tweet-scraper_2026-10-12_10-34-32-570.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 4/4_dataset_tweet-scraper_2026-10-12_10-43-22-676.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 5/5_dataset_tweet-scraper_2026-10-12_12-46-19-207.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN'
        ' 6/6_dataset_tweet-scraper_2026-10-16_11-56-27-896.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN 7/dataset_tweet-scraper_2026-10-16_12-01-58-363.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN 8/dataset_tweet-scraper_2026-10-16_12-18-30-842.json'
    ),
    (
        '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
        ' Scraping/data/APIFY/RUN 9/dataset_tweet-scraper_2026-10-19_09-10-00-361.json'
    ),
]

all_records = []

# 2. Dateien einzeln einlesen
for file_path in json_files:
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
      if isinstance(data, list):
        for item in data:
          item['_source_file'] = file_path
          all_records.append(item)
    print(f'Erfolgreich geladen: {file_path}')
  except Exception as e:
    print(f'Fehler beim Laden von {file_path}: {e}')

# 3. In Pandas DataFrame umwandeln
df = pd.DataFrame(all_records)
print(f'\nGesamtanzahl geladener roher Datensätze: {len(df)}')

# 4. Deduplizierung über die Tweet-ID durchführen
if 'id' in df.columns:
  df['id'] = df['id'].astype(str)
  duplicate_count = df.duplicated(subset=['id']).sum()
  print(f'Gefundene Duplikate (über verschiedene Runs hinweg): {duplicate_count}')

  df_clean = df.drop_duplicates(subset=['id'], keep='first').copy()
  print(f'Verbleibende eindeutige Tweets nach Bereinigung: {len(df_clean)}')
else:
  print("Warnung: Spalte 'id' wurde nicht gefunden.")
  df_clean = df

# 5. Bereinigten Datensatz speichern
output_filename = (
    '/Users/timoschmidt/Desktop/UNI ULM WIN/HiWi/SNA Projekt'
    ' Scraping/data/unique_tweets_cleaned2.json'
)
df_clean.to_json(
    output_filename, orient='records', force_ascii=False, indent=2
)
print(f'\nBereinigte Daten erfolgreich gespeichert unter:\n{output_filename}')