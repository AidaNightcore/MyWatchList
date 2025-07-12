import pandas as pd
import requests

CSV_FILE = "D:/ASE/Licenta/Data/TMDB_all_movies(2).csv"
MEDIA_API_URL = "http://localhost:5000/api/media/movies"
ADMIN_POST_URL = "http://localhost:5000/api/admin/movie"
ADMIN_PUT_URL = "http://localhost:5000/api/admin/movies"
TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjI4MzgyOCwianRpIjoiY2JlNDVmMDQtN2U4NC00NjE4LWE2YzgtMjBjNGU2OWUxNDRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3NTIyODM4MjgsImNzcmYiOiIxYzNlMTFjYy01NTIyLTQ4NWItOTdlMi1kYjJlMzllNTY2MGEiLCJleHAiOjE3NTIyODc0Mjh9.E1qxNv70vtl1u1UIPq6D3HdSUz3zfNbezXy1lRBk0ss"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original/"

def normalize_date(date_val):
    if pd.isnull(date_val):
        return None
    try:
        return str(pd.to_datetime(date_val).date())
    except Exception:
        return None

df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df.columns = [col.strip() for col in df.columns]

resp = requests.get(MEDIA_API_URL, headers={"Authorization": TOKEN})
title_to_id = {}
imdb_to_id = {}
if resp.status_code == 200:
    for movie in resp.json():
        if "title" in movie and "id" in movie:
            title_to_id[movie["title"].strip().lower()] = movie["id"]
        if "imdb_id" in movie and "id" in movie and movie["imdb_id"]:
            imdb_to_id[movie["imdb_id"].strip()] = movie["id"]
print(f"Loaded {len(title_to_id)} movies from DB (via /api/media/movies).")
START_IDX = 1503  # change to where you left off

for idx, row in df.iterrows():
    if idx < START_IDX:
        continue
    title = str(row['title']).strip() if pd.notnull(row['title']) else None
    franchise_title = str(row['franchise']).strip() if 'franchise' in row and pd.notnull(row['franchise']) else None
    synopsis = str(row['overview']).strip() if 'overview' in row and pd.notnull(row['overview']) else None
    publish_date = normalize_date(row['release_date']) if 'release_date' in row and pd.notnull(row['release_date']) else None
    imdb_id = str(row['imdb_id']).strip() if 'imdb_id' in row and pd.notnull(row['imdb_id']) else None

    genres = []
    if 'genres' in row and pd.notnull(row['genres']):
        genres = [g.strip() for g in str(row['genres']).split(',') if g.strip()]

    image_url = None
    if 'poster_path' in row and pd.notnull(row['poster_path']) and str(row['poster_path']).strip() not in ["", "nan"]:
        image_url = TMDB_IMAGE_BASE + str(row['poster_path']).strip().lstrip('/')

    crew = []
    # Director
    if 'director' in row and pd.notnull(row['director']):
        for name in str(row['director']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Director"})

    # Writers
    if 'writer' in row and pd.notnull(row['writer']):
        for name in str(row['writer']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Writer"})

    # Producers
    if 'producer' in row and pd.notnull(row['producer']):
        for name in str(row['producer']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Producer"})

    # Music Composer
    if 'music_composer' in row and pd.notnull(row['music_composer']):
        for name in str(row['music_composer']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Music Composer"})

    # Cast - ACTORS
    if 'cast' in row and pd.notnull(row['cast']):
        for name in str(row['cast']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Actor"})

    # Director of Photography
    if 'director_of_photography' in row and pd.notnull(row['director_of_photography']):
        for name in str(row['director_of_photography']).split(','):
            name = name.strip()
            if name:
                crew.append({"worker": name, "job": "Director of Photography"})

    # Publishers din production_companies
    publishers = []
    if 'production_companies' in row and pd.notnull(row['production_companies']):
        publishers = [p.strip() for p in str(row['production_companies']).split(',') if p.strip()]

    publisher_name = publishers[0] if publishers else None

    data = {}
    if title: data["title"] = title
    if genres: data["genre_names"] = genres
    if crew: data["crew"] = crew
    if publisher_name: data["publisher_name"] = publisher_name
    if franchise_title: data["franchise_title"] = franchise_title
    if synopsis: data["synopsis"] = synopsis
    if publish_date: data["publish_date"] = publish_date
    if imdb_id: data["imdb_id"] = imdb_id
    if image_url: data["image_url"] = image_url

    movie_id = None
    if imdb_id and imdb_id in imdb_to_id:
        movie_id = imdb_to_id[imdb_id]
    elif title and title.lower() in title_to_id:
        movie_id = title_to_id[title.lower()]

    if movie_id:
        put_url = f"{ADMIN_PUT_URL}/{movie_id}"
        resp = requests.put(put_url, json=data, headers={"Authorization": TOKEN})
        print(f"{idx + 1}/{len(df)} - UPDATE: {resp.status_code}: {resp.text}")
    else:
        resp = requests.post(ADMIN_POST_URL, json=data, headers={"Authorization": TOKEN})
        print(f"{idx + 1}/{len(df)} - POST: {resp.status_code}: {resp.text}")

print("Import completat pentru movies.")
