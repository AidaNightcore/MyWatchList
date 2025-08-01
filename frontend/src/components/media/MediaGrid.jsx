import React from "react";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import MediaCard from "./MediaCard";

const MediaGrid = ({ items }) => (
  <Box sx={{ mt: 5 }}>
    <Typography variant="h5" sx={{ mb: 2, fontWeight: "bold" }}>
      All Titles (Newest First)
    </Typography>
    <Grid container spacing={2} columns={{ xs: 2, sm: 4, md: 8, lg: 12 }}>
      {items.map((media) => (
        <Grid item xs={1} sm={1} md={2} lg={2} key={media.id}>
          <MediaCard media={media} />
        </Grid>
      ))}
    </Grid>
  </Box>
);

export default MediaGrid;
