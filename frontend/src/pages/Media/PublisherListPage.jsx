import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import PublisherCard from "../../components/media/PublisherCard";
import api from "../../services/api";

export default function PublishersPage() {
  const [publishers, setPublishers] = useState([]);

  useEffect(() => {
    api.get("/api/media/publishers").then((res) => {
      setPublishers(res.data);
      console.log("UN PUBLISHER EXEMPLU:", res.data[0]);
    });
  }, []);

  // Group by type
  const booksPubs = publishers.filter((p) => p.books && p.books.length > 0);
  const moviesPubs = publishers.filter((p) => p.movies && p.movies.length > 0);
  const showsPubs = publishers.filter((p) => p.shows && p.shows.length > 0);

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", py: 4 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Publishers
      </Typography>

      <Typography variant="h6" sx={{ mt: 3 }}>
        Books
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {booksPubs.map((p) => (
          <PublisherCard key={p.id} publisher={p} />
        ))}
      </Box>
      <Typography variant="h6" sx={{ mt: 3 }}>
        Movies
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {moviesPubs.map((p) => (
          <PublisherCard key={p.id} publisher={p} />
        ))}
      </Box>
      <Typography variant="h6" sx={{ mt: 3 }}>
        Shows
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {showsPubs.map((p) => (
          <PublisherCard key={p.id} publisher={p} />
        ))}
      </Box>
    </Box>
  );
}
