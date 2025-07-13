from api.media.models import Show, Book


def enforce_progress(item, requested_progress):
    """
    Returnează (progress_validat, mesaj_info)
    """
    title = item.title  # asigură-te că relationship funcționează
    if not title or not title.media_type:
        return (0, "Title or type not found.")

    type_name = title.media_type.elementTypeName

    if type_name == "Show":
        # Show → total episodes
        show = Show.query.filter_by(title=title.title).first()
        if not show or not show.seasons:
            return (0, "Show or seasons not found.")
        total_episodes = sum([season.episodeCount or 0 for season in show.seasons])
        if total_episodes == 0:
            return (0, "Show has no episodes.")
        progress = min(int(requested_progress), total_episodes)
        return (progress, f"Max progress for show is {total_episodes} episodes.")

    elif type_name == "Book":
        # Book → pages
        book = Book.query.filter_by(title=title.title).first()
        total_pages = book.pages if book and book.pages else 1
        progress = min(int(requested_progress), total_pages)
        return (progress, f"Max progress for book is {total_pages} pages.")

    elif type_name == "Movie":
        # Movie: 1 means completed
        if item.status == "completed":
            return (1, "Progress for movie is 1 (completed).")
        return (0, "Progress for movie is 0 (not completed).")

    # fallback
    return (min(int(requested_progress), 1), "Default max progress 1.")

