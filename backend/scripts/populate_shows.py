import pandas as pd
import requests

CSV_FILE = "D:/ASE/Licenta/Data/TMDB_tv_dataset_v3.csv"
ADMIN_SHOW_URL = "http://localhost:5000/api/admin/show"
ADMIN_SEASON_URL = "http://localhost:5000/api/admin/shows/{show_id}/season"
ADMIN_EPISODE_URL = "http://localhost:5000/api/admin/seasons/{season_id}/episode"
MEDIA_SHOW_URL = "http://localhost:5000/api/media/shows"
TOKEN = "Bearer ..."  # Replace with your actual token

def normalize_date(date_val):
    if pd.isnull(date_val):
        return None
    try:
        return str(pd.to_datetime(date_val).date())
    except Exception:
        return None

df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df.columns = [col.strip() for col in df.columns]

shows_map = {}
seasons_map = {}

# Populate shows_map from DB
resp = requests.get(MEDIA_SHOW_URL, headers={"Authorization": TOKEN})
if resp.status_code == 200:
    for show in resp.json():
        if "title" in show and "id" in show:
            shows_map[show["title"].strip().lower()] = show["id"]

for idx, row in df.iterrows():
    show_title = str(row['series_title']).strip() if pd.notnull(row['series_title']) else None
    if not show_title:
        print(f"{idx + 1} - SKIP: Missing show title")
        continue

    # Publisher from production_companies (first entry)
    publisher_name = None
    if pd.notnull(row['production_companies']):
        publishers = [p.strip() for p in str(row['production_companies']).split(',') if p.strip()]
        publisher_name = publishers[0] if publishers else None

    # Franchise
    franchise_title = str(row['franchise']).strip() if pd.notnull(row['franchise']) else None

    # Genres
    genres = []
    if pd.notnull(row['genres']):
        genres = [g.strip() for g in str(row['genres']).split(',') if g.strip()]

    # Show overview & poster
    show_synopsis = str(row['series_overview']).strip() if pd.notnull(row['series_overview']) else None
    show_image_url = str(row['series_poster_path']).strip() if pd.notnull(row['series_poster_path']) else None
    if show_image_url:
        show_image_url = f"https://image.tmdb.org/t/p/original/{show_image_url.lstrip('/')}"

    # --- SHOW ---
    show_key = show_title.lower()
    show_id = shows_map.get(show_key)
    if not show_id:
        show_payload = {
            "title": show_title,
            "publisher_name": publisher_name,
            "franchise_title": franchise_title,
            "genre_names": genres,
            "synopsis": show_synopsis,
            "image_url": show_image_url
        }
        resp_show = requests.post(ADMIN_SHOW_URL, json=show_payload, headers={"Authorization": TOKEN})
        if resp_show.status_code == 201:
            show_id = resp_show.json()["id"]
            shows_map[show_key] = show_id
            print(f"{idx + 1} - SHOW CREATED: {show_title}")
        else:
            print(f"{idx + 1} - SHOW FAIL: {resp_show.status_code} {resp_show.text}")
            continue

    # --- SEASON ---
    season_number = int(row['season_number']) if pd.notnull(row['season_number']) else 1
    season_key = (show_id, season_number)
    season_id = seasons_map.get(season_key)
    if not season_id:
        season_title = f"Season {season_number}"
        season_synopsis = str(row['season_overview']).strip() if pd.notnull(row['season_overview']) else None
        season_image_url = str(row['season_poster_path']).strip() if pd.notnull(row['season_poster_path']) else None
        if season_image_url:
            season_image_url = f"https://image.tmdb.org/t/p/original/{season_image_url.lstrip('/')}"

        season_payload = {
            "title": season_title,
            "season_number": season_number,
            "synopsis": season_synopsis,
            "publish_date": normalize_date(row['season_air_date']) if pd.notnull(row['season_air_date']) else None,
            "genre_names": genres,
            "image_url": season_image_url
        }
        url = ADMIN_SEASON_URL.format(show_id=show_id)
        resp_season = requests.post(url, json=season_payload, headers={"Authorization": TOKEN})
        if resp_season.status_code == 201:
            season_id = resp_season.json()["id"]
            seasons_map[season_key] = season_id
            print(f"{idx + 1} - SEASON CREATED: Season {season_number} for {show_title}")
        else:
            print(f"{idx + 1} - SEASON FAIL: {resp_season.status_code} {resp_season.text}")
            continue

    # --- EPISODE ---
    episode_number = int(row['episode_number']) if pd.notnull(row['episode_number']) else None
    episode_title = f"Episode {episode_number}" if episode_number else "Episode"
    episode_synopsis = str(row['overview']).strip() if pd.notnull(row['overview']) else None
    episode_image_url = str(row['still_path']).strip() if pd.notnull(row['still_path']) else None
    if episode_image_url:
        episode_image_url = f"https://image.tmdb.org/t/p/original/{episode_image_url.lstrip('/')}"
    episode_payload = {
        "title": episode_title,
        "synopsis": episode_synopsis,
        "publish_date": normalize_date(row['air_date']) if pd.notnull(row['air_date']) else None,
        "genre_names": genres,
        "image_url": episode_image_url
    }
    url = ADMIN_EPISODE_URL.format(season_id=season_id)
    resp_ep = requests.post(url, json=episode_payload, headers={"Authorization": TOKEN})
    if resp_ep.status_code == 201:
        print(f"{idx + 1} - EPISODE CREATED: {episode_title} for {show_title}, S{season_number}")
    else:
        print(f"{idx + 1} - EPISODE FAIL: {resp_ep.status_code} {resp_ep.text}")

print("Import completat pentru episoade.")
