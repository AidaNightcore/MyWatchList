def enforce_progress(item, progress):
    """
    For books: limit progress to pages.
    For movies/episodes: limit to 1.
    For seasons: carry-over progress into next seasons.
    For shows: carry-over progress into seasons, but do not exceed total episode count of the show.
    """

    if not item.title or not item.title.media_type:
        return progress, None

    type_name = item.title.media_type.elementTypeName
    from api.media.models import Book, Show, Season, Episode, Movie

    # BOOK
    if type_name == 'Book':
        book = Book.query.filter_by(titleID=item.titleID).first()
        max_pages = book.pages if book and book.pages else None
        if max_pages is not None:
            return min(progress, max_pages), f"Book: max progress is {max_pages} (pages)."
        return progress, None

    # MOVIE or EPISODE
    if type_name in ('Movie', 'Episode'):
        return min(progress, 1), f"{type_name}: max progress is 1."

    # SEASON
    if type_name == 'Season':
        season = Season.query.filter_by(titleID=item.titleID).first()
        max_episodes = season.episodeCount if season and season.episodeCount else None
        if max_episodes is not None:
            return min(progress, max_episodes), f"Season: max progress is {max_episodes} (episodes)."
        return progress, None

    # SHOW with carry-over
    if type_name == 'Show':
        show = Show.query.filter_by(titleID=item.titleID).first()
        if show:
            # Calculate total episodes in all seasons for the show
            from api.media.models import Season as SeasonModel
            all_seasons = SeasonModel.query.filter_by(showID=show.id).all()
            total_episodes = sum(s.episodeCount or 0 for s in all_seasons)
            if total_episodes:
                return min(progress, total_episodes), f"Show: max progress is {total_episodes} (episodes across all seasons)."
        return progress, None

    return progress, None
