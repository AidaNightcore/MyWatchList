import React, { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Box from "@mui/material/Box";
import MediaRow from "../../components/media/MediaRow";
import MediaGrid from "../../components/media/MediaGrid";
import { useMedia } from "../../contexts/MediaContext";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import { useWatchlist } from "../../contexts/WatchlistContext";
import MediaFilterBar from "../../components/media/Filters/MediaFilterBar";
import MediaCard from "../../components/media/MediaCard";

function getQueryParams(search) {
  return Object.fromEntries(new URLSearchParams(search));
}

const MediaListPage = () => {
  const { books, shows, movies, allTitles, loading, error, loadAllMedia } =
    useMedia();
  const { watchlist } = useWatchlist();
  const location = useLocation();
  const navigate = useNavigate();

  // Initial values (parse from URL query params)
  const [genre, setGenre] = useState([]);
  const [publisher, setPublisher] = useState([]);
  const [mediaType, setMediaType] = useState("");

  // Parse params din URL o singură dată la mount
  useEffect(() => {
    const params = getQueryParams(location.search);
    if (params.type) setMediaType(params.type);
    if (params.genre)
      setGenre(Array.isArray(params.genre) ? params.genre : [params.genre]);
    if (params.publisher)
      setPublisher(
        Array.isArray(params.publisher) ? params.publisher : [params.publisher]
      );
    // Poți extinde pentru franchise etc.
  }, [location.search]);

  useEffect(() => {
    const params = {};
    if (mediaType) params.type = mediaType;
    if (genre.length)
      params.genre = genre.map((g) => (typeof g === "string" ? g : g.name));
    if (publisher.length)
      params.publisher = publisher.map((p) =>
        typeof p === "string" ? p : p.name
      );
    const queryString = new URLSearchParams(params).toString();
    navigate(`?${queryString}`, { replace: true });
  }, [mediaType, genre, publisher, navigate]);

  const watchlistItems = useMemo(() => {
    if (!watchlist) return [];
    return Object.values(watchlist).flat().filter(Boolean);
  }, [watchlist]);

  const getWatchlistItemsFor = (mediaId) => {
    return watchlistItems.filter(
      (el) => String(el.titleID) === String(mediaId)
    );
  };

  const filteredTitles = useMemo(() => {
    // Normalizează selecțiile la array de stringuri (nume)
    const selectedGenreNames = genre.map((g) =>
      typeof g === "string" ? g : g.name
    );
    const selectedPublisherNames = publisher.map((p) =>
      typeof p === "string" ? p : p.name
    );

    return allTitles.filter((item) => {
      if (mediaType && item.type !== mediaType) return false;
      // GENURI: verifică dacă cel puțin un gen selectat se regăsește la media
      if (
        selectedGenreNames.length > 0 &&
        !selectedGenreNames.some((g) => item.genres?.includes(g))
      )
        return false;
      // PUBLISHER: verifică dacă cel puțin un publisher selectat e la media
      if (
        selectedPublisherNames.length > 0 &&
        (!item.details ||
          !selectedPublisherNames.includes(item.details.publisher))
      )
        return false;
      return true;
    });
  }, [allTitles, genre, publisher, mediaType]);

  useEffect(() => {
    loadAllMedia();
  }, [loadAllMedia]);

  if (loading)
    return (
      <Box sx={{ textAlign: "center", mt: 6 }}>
        <CircularProgress size={56} />
      </Box>
    );

  if (error)
    return (
      <Box sx={{ p: 4 }}>
        <Alert severity="error">
          Eroare la încărcarea datelor media: {error.message || "Unknown error"}
        </Alert>
      </Box>
    );

  const showRows = !genre.length && !publisher.length && !mediaType;

  return (
    <Box sx={{ p: { xs: 1, sm: 2, md: 4 } }}>
      <MediaFilterBar
        genre={genre}
        setGenre={setGenre}
        publisher={publisher}
        setPublisher={setPublisher}
        mediaType={mediaType}
        setMediaType={setMediaType}
      />

      {showRows && (
        <>
          <MediaRow
            title="Books"
            items={books}
            renderItem={(book) => (
              <MediaCard
                media={book}
                watchlistItems={getWatchlistItemsFor(book.id)}
              />
            )}
          />
          <MediaRow
            title="Shows"
            items={shows}
            renderItem={(show) => (
              <MediaCard
                media={show}
                watchlistItems={getWatchlistItemsFor(show.id)}
              />
            )}
          />
          <MediaRow
            title="Movies"
            items={movies}
            renderItem={(movie) => (
              <MediaCard
                media={movie}
                watchlistItems={getWatchlistItemsFor(movie.id)}
              />
            )}
          />
        </>
      )}

      <MediaGrid
        items={filteredTitles}
        renderItem={(media) => (
          <MediaCard
            media={media}
            watchlistItems={getWatchlistItemsFor(media.id)}
          />
        )}
      />
    </Box>
  );
};

export default MediaListPage;
