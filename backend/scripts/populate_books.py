import pandas as pd
import requests

# Configurare căi și endpoint
CSV_BOOKS = "D:/ASE/Licenta/Data/books.csv"
CSV_DATA = "D:/ASE/Licenta/Data/data.csv"
ADMIN_BOOK_URL = "http://localhost:5000/api/admin/book"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjQxMTAwOCwianRpIjoiMjgyYjIwNDQtNWVkNS00OTdmLWE3M2MtZDAyNzkzNGExNjkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTI0MTEwMDgsImNzcmYiOiJjNmU0OTViYy1lZjdlLTQyYjAtOTg4Zi0wYmQ1ZmU4YzJlZTMiLCJleHAiOjE3NTI0MTQ2MDh9.N1fbLiyZAg1v_bHIx4ojrH9Ht5Z83AqLsNb2xi4hl_A"
df_books = pd.read_csv(CSV_BOOKS, on_bad_lines='skip')
df_data = pd.read_csv(CSV_DATA, on_bad_lines='skip')

df_books.columns = [c.strip() for c in df_books.columns]
df_data.columns = [c.strip() for c in df_data.columns]

def normalize_date(val):
    if pd.isnull(val) or not val or str(val).strip() in ['N/A', '']:
        return None
    try:
        return str(pd.to_datetime(val, errors='coerce').date())
    except Exception:
        return None

def parse_list_column(val):
    if pd.isnull(val) or not str(val).strip():
        return []
    for sep in [';', '|', ',','/']:
        if sep in str(val):
            return [s.strip() for s in str(val).split(sep) if s.strip()]
    return [str(val).strip()]

def best_row_match(row_b):
    isbn = str(row_b.get("isbn", "")).strip()
    title = str(row_b.get("title", "")).strip().lower()
    # Caută întâi după ISBN (orice variantă)
    for idx, row_d in df_data.iterrows():
        for col in ['isbn', 'isbn10', 'isbn13']:
            if col in row_d and pd.notnull(row_d[col]) and isbn and str(row_d[col]).strip() == isbn:
                return row_d
    # Dacă nu merge ISBN, caută după titlu
    for idx, row_d in df_data.iterrows():
        if 'title' in row_d and pd.notnull(row_d['title']):
            if str(row_d['title']).strip().lower() == title:
                return row_d
    return {}

def extract_payload(row_b, row_d):
    title = row_b.get("title") or row_d.get("title")
    publisher = row_b.get("publisher") or row_d.get("publisher")
    genres = parse_list_column(row_b.get("genres") or row_d.get("categories"))
    crew = []
    authors = parse_list_column(row_b.get("authors") or row_d.get("authors"))
    for a in authors:
        crew.append({"worker": a, "job": "Author"})
    synopsis = row_b.get("synopsis") or row_d.get("description") or ""
    isbnID = row_b.get("isbn") or row_d.get("isbn10") or row_d.get("isbn13") or row_d.get("isbn")
    pages = row_b.get("num_pages") or row_d.get("num_pages")
    imgURL = row_b.get("imgURL") or row_b.get("image_url") or row_d.get("image_url") or row_d.get("thumbnail")
    publishDate = row_b.get("publishDate") or row_b.get("publication_date") or row_d.get("publishDate") or row_d.get("publication_date")
    publishDate = normalize_date(publishDate)
    payload = {
        "title": title,
        "publisher_name": publisher,
        "genre_names": genres,
        "crew": crew,
        "synopsis": synopsis,
        "isbnID": isbnID,
        "pages": int(pages) if pd.notnull(pages) and str(pages).isdigit() else None,
        "imgURL": imgURL,
        "publishDate": publishDate
    }
    print(payload)
    return {k: v for k, v in payload.items() if v is not None}


headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Content-Type": "application/json"}
START_IDX=0
for idx, row_b in df_books.iterrows():
    if idx < START_IDX:
        continue
    row_d = best_row_match(row_b)
    payload = extract_payload(row_b, row_d)
    try:
        r = requests.post(ADMIN_BOOK_URL, json=payload, headers=headers, timeout=10)
        print(f"{idx+1}. {payload.get('title')}: {r.status_code} {r.text}")
    except Exception as e:
        print(f"EROARE la {payload.get('title')}: {e}")

print("Gata popularea!")