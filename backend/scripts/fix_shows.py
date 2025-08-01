import pandas as pd
import requests

CSV_FILE = "D:/ASE/Licenta/Data/TMDB_all_movies(2).csv"
ADMIN_PUT_SHOW_URL = "http://localhost:5000/api/admin/shows/{show_id}"
JWT_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjQ4ODY2NiwianRpIjoiNjUxMmVjYzktM2JiZS00YmY1LWJmNDktZWEwMWM4NTNkZWFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTI0ODg2NjYsImNzcmYiOiI5NWIzZDBhZi0xMDY1LTRlNjYtOTA0NC0wNmI3MjM3ZDIzZWQiLCJleHAiOjE3NTI0OTIyNjZ9.kbYUHw0d8ZWag1kPXP40jFsiyg-oRDQO_LvPMin55Uw"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original/"
df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
df.columns = [c.strip() for c in df.columns]

def parse_list_column(val):
    if pd.isnull(val) or not str(val).strip():
        return []
    return [v.strip() for v in str(val).split(',') if v.strip()]

headers = {"Authorization": JWT_TOKEN, "Content-Type": "application/json"}

for idx, row in df.iterrows():
    show_id = int(row.get('id')) if 'id' in row and pd.notnull(row['id']) else None
    if not show_id:
        continue

    payload = {}
    if pd.notnull(row.get('name')):
        payload['title'] = str(row['name']).strip()
    if pd.notnull(row.get('overview')):
        payload['synopsis'] = str(row['overview']).strip()
    if pd.notnull(row.get('poster_path')) and str(row['poster_path']).strip().lower() not in ["", "nan"]:
        payload['imgURL'] = TMDB_IMAGE_BASE + str(row['poster_path']).strip().lstrip('/')
    if pd.notnull(row.get('production_companies')):
        publishers = parse_list_column(row['production_companies'])
        if publishers:
            payload['publisher_name'] = publishers[0]
    if pd.notnull(row.get('genres')):
        payload['genre_names'] = parse_list_column(row['genres'])
    if 'franchise' in df.columns and pd.notnull(row.get('franchise')):
        payload['franchise_title'] = str(row['franchise']).strip()

    url = ADMIN_PUT_SHOW_URL.format(show_id=show_id)
    try:
        r = requests.put(url, json=payload, headers=headers, timeout=10)
        print(f"{idx+1}. PUT {show_id} {payload.get('title')}: {r.status_code} {r.text}")
    except Exception as e:
        print(f"EROARE la {show_id}: {e}")

print("Actualizare completă.")
