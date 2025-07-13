import React, { useEffect, useMemo } from "react";
import Box from "@mui/material/Box";
import MediaRow from "../../components/media/MediaRow";
import MediaGrid from "../../components/media/MediaGrid";
import { useMedia } from "../../contexts/MediaContext";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import { useWatchlist } from "../../contexts/WatchlistContext";

const MediaListPage = () => {
  const { books, shows, movies, allTitles, loading, error, loadAllMedia } =
    useMedia();

  const { watchlist } = useWatchlist();

  const watchlistItems = useMemo(() => {
    if (!watchlist) return [];
    return Object.values(watchlist).flat().filter(Boolean);
  }, [watchlist]);

  const getWatchlistInfo = (mediaId) => {
    const item = watchlistItems.find((el) => el.titleID === mediaId);
    return {
      watchlistStatus: item?.status || null,
      watchlistItemId: item?.id || null,
      existingFields: item || null,
    };
  };

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

  return (
    <Box sx={{ p: { xs: 1, sm: 2, md: 4 } }}>
      <MediaRow
        title="Books"
        items={books.map((book) => {
          const info = getWatchlistInfo(book.id);
          return { ...book, ...info };
        })}
      />
      <MediaRow
        title="Shows"
        items={shows.map((show) => {
          const info = getWatchlistInfo(show.id);
          return { ...show, ...info };
        })}
      />
      <MediaRow
        title="Movies"
        items={movies.map((movie) => {
          const info = getWatchlistInfo(movie.id);
          return { ...movie, ...info };
        })}
      />
      <MediaGrid
        items={allTitles.map((media) => {
          const info = getWatchlistInfo(media.id);
          return { ...media, ...info };
        })}
      />
    </Box>
  );
};

export default MediaListPage;
