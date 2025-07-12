import pandas as pd
import requests

CSV_BOOKS = "D:/ASE/Licenta/Data/books.csv"
CSV_DATA = "D:/ASE/Licenta/Data/data.csv"
MEDIA_API_URL = "http://localhost:5000/api/media/books"
ADMIN_POST_URL = "http://localhost:5000/api/admin/book"
ADMIN_PUT_URL = "http://localhost:5000/api/admin/book"
TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjI3NTk3NCwianRpIjoiNzk0OWM0OTAtYmJhZS00Mjc1LWEyODUtYWEzMWY3NGFjYzg4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3NTIyNzU5NzQsImNzcmYiOiJmNWRkOGJiOC0wZDhmLTQ3ZDQtYWMyZi1kNTM3YTM3MGQ4NTciLCJleHAiOjE3NTIyNzk1NzR9.BHpvaU9KcLaQ9u5xCUOyI-AhHP0aKRR-A32RzN1Qiog"

def normalize_date(date_val):
    if pd.isnull(date_val):
        return None
    try:
        return str(pd.to_datetime(date_val).date())
    except Exception:
        pass
    try:
        year = int(float(str(date_val)))
        return f"{year}-01-01"
    except Exception:
        return None

# Citire CSV cu eliminare spații din header
df_data = pd.read_csv(CSV_DATA, on_bad_lines='skip')
df_data.columns = [col.strip() for col in df_data.columns]
df_books = pd.read_csv(CSV_BOOKS, on_bad_lines='skip')
df_books.columns = [col.strip() for col in df_books.columns]

# Creează un mapping pentru ISBN și pentru titlu+autori (ambele)
isbn_map = {}
title_authors_map = {}

for _, row in df_data.iterrows():
    isbn = str(row['isbn10']).strip() if pd.notnull(row['isbn10']) else None
    title = str(row['title']).strip().lower() if pd.notnull(row['title']) else None
    authors = set(name.strip().lower() for name in str(row['authors']).replace(";", ",").split(",")) if pd.notnull(row['authors']) else set()
    synopsis = str(row['description']) if pd.notnull(row['description']) else None

    # GENURI (cu filtrare life/fictitious)
    categories = None
    if pd.notnull(row.get('categories', None)):
        raw_categories = [g.strip() for g in str(row['categories']).replace(";", ",").split(",")]
        categories = []
        for g in raw_categories:
            g_lower = g.lower()
            if "fictitious character" in g_lower:
                continue
            if g_lower == "slice of life":
                categories.append(g)
            elif "life" in g_lower:
                categories.append(g.replace("life", "", 1).strip())
            else:
                categories.append(g)
        categories = [g for g in categories if g and g.strip()]
        if not categories:
            categories = None

    image_url = str(row['thumbnail']) if 'thumbnail' in row and pd.notnull(row['thumbnail']) else None
    entry = {
        "authors": authors,
        "synopsis": synopsis,
        "categories": categories,
        "image_url": image_url
    }
    if isbn:
        isbn_map[isbn] = entry
    if title:
        title_authors_map.setdefault(title, []).append(entry)

# Map ISBN -> id din /api/media/books (pentru update)
isbn_to_id = {}
title_to_id = {}
resp = requests.get(MEDIA_API_URL, headers={"Authorization": TOKEN})
if resp.status_code == 200:
    for book in resp.json():
        if "isbn_id" in book and "id" in book and book["isbn_id"]:
            isbn_to_id[str(book["isbn_id"]).strip()] = book["id"]
        if "title" in book and "id" in book and book["title"]:
            title_to_id[book["title"].strip().lower()] = book["id"]
print(f"Loaded {len(isbn_to_id)} books with ISBN and {len(title_to_id)} by title from DB (via /api/media/books).")

for idx, row in df_books.iterrows():
    isbn_id = str(row['isbn']).strip() if pd.notnull(row['isbn']) else None
    title = str(row['title']).strip() if pd.notnull(row['title']) else None
    title_lower = title.lower() if title else None
    publisher_name = str(row['publisher']) if pd.notnull(row['publisher']) else None
    publish_date = normalize_date(row['publication_date']) if pd.notnull(row['publication_date']) else None
    pages = int(row['num_pages']) if pd.notnull(row['num_pages']) else None

    crew = []
    author_set = set()
    if pd.notnull(row['authors']):
        names = [name.strip() for name in str(row['authors']).replace("/", ",").split(",")]
        for name in names:
            if name:
                crew.append({"worker": name, "job": "Author"})
                author_set.add(name.lower())

    # Matching logic:
    entry = None
    # 1. Prioritar după ISBN
    if isbn_id and isbn_id in isbn_map:
        entry = isbn_map[isbn_id]
    # 2. Altfel, după titlu + cel puțin un autor comun
    elif title_lower and title_lower in title_authors_map and author_set:
        for candidate in title_authors_map[title_lower]:
            if candidate["authors"] & author_set:
                entry = candidate
                break

    synopsis = entry["synopsis"] if entry else None
    categories = entry["categories"] if entry else []
    image_url = entry["image_url"] if entry else None

    data = {
        "title": title,
        "crew": crew,
        "genre_names": categories
    }
    if publisher_name:
        data["publisher_name"] = publisher_name
    if synopsis:
        data["synopsis"] = synopsis
    if publish_date:
        data["publish_date"] = publish_date
    if isbn_id:
        data["isbn_id"] = isbn_id
    if pages:
        data["pages"] = pages
    if image_url:
        data["image_url"] = image_url

    # Matching pentru id în DB:
    book_id = isbn_to_id.get(isbn_id) if isbn_id else None
    if not book_id and title_lower:
        book_id = title_to_id.get(title_lower)

    if book_id:
        put_url = f"{ADMIN_PUT_URL}/{book_id}"
        resp = requests.put(put_url, json=data, headers={"Authorization": TOKEN})
        print(f"{idx + 1}/{len(df_books)} - UPDATE: {resp.status_code}: {resp.text}")
    else:
        resp = requests.post(ADMIN_POST_URL, json=data, headers={"Authorization": TOKEN})
        print(f"{idx + 1}/{len(df_books)} - POST: {resp.status_code}: {resp.text}")

print("Import completat pentru books.")
