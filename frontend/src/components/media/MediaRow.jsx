import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import MediaCard from "./MediaCard";

const MediaRow = ({ title, items }) => {
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
        {items.map((media) => (
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
        ))}
      </Box>
    </Box>
  );
};

export default MediaRow;
