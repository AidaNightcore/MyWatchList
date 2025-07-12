import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import MediaRow from "../../components/media/MediaRow";
import MediaGrid from "../../components/media/MediaGrid";
import { useMedia } from "../../contexts/MediaContext";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";

const MediaListPage = () => {
  const { books, shows, movies, allTitles, loading, error, loadAllMedia } =
    useMedia();

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
      <MediaRow title="Books" items={books} />
      <MediaRow title="Shows" items={shows} />
      <MediaRow title="Movies" items={movies} />
      <MediaGrid items={allTitles} />
    </Box>
  );
};

export default MediaListPage;
