import pandas as pd
import requests

CSV_FILE = "D:/ASE/Licenta/Data/TMDB_tv_dataset_v3.csv"
ADMIN_SHOW_URL = "http://localhost:5000/api/admin/show"
JWT_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjQ4ODI0MiwianRpIjoiNjc4YmI0MTktNTM2Ni00MjlmLWI5YTctZTM2ODNhZDdiNjBjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTI0ODgyNDIsImNzcmYiOiJlZWUyNTI2Yi1kMzhiLTQ2YjAtODE5My04YzExZjE2YmJlOWIiLCJleHAiOjE3NTI0OTE4NDJ9.PrrLbEo_9FYKaH3Rrn40d-EkL-uP06KeIpQXlZH2H50"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original/"
df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df.columns = [c.strip() for c in df.columns]

def parse_list_column(val):
    if pd.isnull(val) or not str(val).strip():
        return []
    return [v.strip() for v in str(val).split(',') if v.strip()]

headers = {"Authorization": JWT_TOKEN, "Content-Type": "application/json"}
START_IDX = 0
for idx, row in df.iterrows():
    if idx < START_IDX:
        continue

    title = str(row['name']).strip() if pd.notnull(row['name']) else None
    if not title:
        print(f"{idx + 1} - SKIP: no title")
        continue

    synopsis = str(row['overview']).strip() if pd.notnull(row['overview']) else None
    imgURL = None
    if pd.notnull(row['poster_path']) and str(row['poster_path']).strip().lower() not in ["", "nan"]:
        imgURL = TMDB_IMAGE_BASE + str(row['poster_path']).strip().lstrip('/')
    genres = parse_list_column(row.get('genres')) if pd.notnull(row.get('genres')) else []
    publisher = None
    if pd.notnull(row.get('production_companies')):
        publisher_list = parse_list_column(row['production_companies'])
        publisher = publisher_list[0] if publisher_list else None
    crew = []
    if pd.notnull(row.get('created_by')):
        for creator in parse_list_column(row['created_by']):
            crew.append({"worker": creator, "job": "Creator"})

    payload = {
        "title": title,
        "synopsis": synopsis,
        "imgURL": imgURL,
        "genre_names": genres,
    }
    if publisher:
        payload["publisher_name"] = publisher
    if crew:
        payload["crew"] = crew

    # opțional: adaugă și franchise_title dacă există coloana la CSV
    if 'franchise' in df.columns and pd.notnull(row.get('franchise')):
        payload["franchise_title"] = str(row['franchise']).strip()

    try:
        r = requests.post(ADMIN_SHOW_URL, json=payload, headers=headers, timeout=10)
        print(f"{idx+1}. {title}: {r.status_code} {r.text}")
    except Exception as e:
        print(f"EROARE la {title}: {e}")

print("Gata popularea SHOWS!")
