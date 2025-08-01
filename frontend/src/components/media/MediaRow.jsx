import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import MediaCard from "./MediaCard";

// Normalizare universală indiferent de sursă
function normalizeMedia(item) {
  // Caz watchlist: are .title ca obiect
  if (item.title && typeof item.title === "object") {
    return {
      id: item.title.id || item.titleID || item.id,
      title: item.title.name || item.title.title || item.title.titleName,
      type: item.title.type,
      imgURL: item.title.imgURL || item.element_details?.imgURL,
      score: item.score ?? item.title.score,
      publishDate: item.title.publishDate,
      genres: item.title.genres,
    };
  }
  // Caz board topic: nu are .title ca obiect, ci string sau alt field
  return {
    id: item.titleID || item.id,
    title: item.title || item.titleName || item.name,
    imgURL: item.imgURL || item.image_url,
    score: item.score,
    type: item.type,
    publishDate: item.publishDate,
    genres: item.genres,
  };
}

const MediaRow = ({ title, items = [] }) => {
  if (!Array.isArray(items)) items = [];
  return (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: "bold" }}>
        {title}
      </Typography>
      <Box
        sx={{
          display: "flex",
          overflowX: "auto",
          pb: 1,
          gap: 2,
          "&::-webkit-scrollbar": { height: 8 },
          "&::-webkit-scrollbar-thumb": { background: "#bbb", borderRadius: 4 },
        }}
      >
        {items.length === 0 && (
          <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>
            No items found.
          </Typography>
        )}
        {items.map((item) => {
          const media = normalizeMedia(item);
          // Nu afișa card dacă nu are titlu sau id
          if (!media.id || !media.title) return null;
          return (
            <Box
              key={media.id}
              sx={{
                flex: "0 0 auto",
                width: { xs: 130, sm: 150, md: 180, lg: 220 },
                scrollSnapAlign: "start",
              }}
            >
              <MediaCard media={media} />
            </Box>
          );
        })}
      </Box>
    </Box>
  );
};

export default MediaRow;
