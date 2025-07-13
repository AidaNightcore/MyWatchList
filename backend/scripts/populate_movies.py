import pandas as pd
import requests

CSV_FILE = "D:/ASE/Licenta/Data/TMDB_all_movies(2).csv"
ADMIN_POST_URL = "http://localhost:5000/api/admin/movie"
TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjQxMjU0NiwianRpIjoiNWJjMTViMDItZjVhMS00YzA2LTgzMzctMzYwYmZiZmViNjcwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTI0MTI1NDYsImNzcmYiOiIwNzNjYTVkYS04OTNlLTRhNzctYjAwMC1jNGU5MjhiZmNmZDgiLCJleHAiOjE3NTI0MTYxNDZ9.UAhdmeC_SlhMVGPJvDmqngNX3RRRX_baxQYATcUfREE"  # your JWT here
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original/"

def normalize_date(date_val):
    if pd.isnull(date_val) or not str(date_val).strip():
        return None
    try:
        return str(pd.to_datetime(date_val).date())
    except Exception:
        return None

df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df.columns = [col.strip() for col in df.columns]

START_IDX = 0  # Set to where you want to resume

for idx, row in df.iterrows():
    if idx < START_IDX:
        continue

    # Title and main fields
    title = str(row['title']).strip() if pd.notnull(row.get('title')) else None
    synopsis = str(row['overview']).strip() if pd.notnull(row.get('overview')) else None
    publishDate = normalize_date(row.get('release_date'))
    imdbID = str(row['imdb_id']).strip() if pd.notnull(row.get('imdb_id')) else None

    # Genres
    genres = []
    if pd.notnull(row.get('genres')):
        genres = [g.strip() for g in str(row['genres']).split(',') if g.strip()]

    # Image URL
    imgURL = None
    if pd.notnull(row.get('poster_path')) and str(row['poster_path']).strip().lower() not in ["", "nan"]:
        imgURL = TMDB_IMAGE_BASE + str(row['poster_path']).strip().lstrip('/')

    # Franchise and publisher
    franchise_title = str(row['franchise']).strip() if pd.notnull(row.get('franchise')) else None
    publishers = []
    if pd.notnull(row.get('production_companies')):
        publishers = [p.strip() for p in str(row['production_companies']).split(',') if p.strip()]
    publisher_name = publishers[0] if publishers else None

    # Crew extraction (director, writer, etc)
    crew = []
    for field, job in [
        ('director', "Director"),
        ('writer', "Writer"),
        ('producer', "Producer"),
        ('music_composer', "Music Composer"),
        ('cast', "Actor"),
        ('director_of_photography', "Director of Photography")
    ]:
        if pd.notnull(row.get(field)):
            for name in str(row[field]).split(','):
                name = name.strip()
                if name:
                    crew.append({"worker": name, "job": job})

    # Duration (if available)
    duration = int(row['runtime']) if 'runtime' in row and pd.notnull(row['runtime']) and str(row['runtime']).isdigit() else None

    # Build the payload as required by create_media_with_metadata (naming must match)
    data = {}
    if title: data["title"] = title
    if genres: data["genre_names"] = genres
    if crew: data["crew"] = crew
    if publisher_name: data["publisher_name"] = publisher_name
    if franchise_title: data["franchise_title"] = franchise_title
    if synopsis: data["synopsis"] = synopsis
    if publishDate: data["publishDate"] = publishDate
    if imdbID: data["imdbID"] = imdbID
    if imgURL: data["imgURL"] = imgURL
    if duration: data["duration"] = duration

    # Send the POST request with the Bearer token
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}
    try:
        resp = requests.post(ADMIN_POST_URL, json=data, headers=headers, timeout=10)
        print(f"{idx + 1}/{len(df)} - POST: {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"EROARE la {title}: {e}")

print("Import completat pentru movies.")
