import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import FranchiseCard from "../../components/media/FranchiseCard";
import api from "../../services/api";

export default function FranchisesPage() {
  const [franchises, setFranchises] = useState([]);

  useEffect(() => {
    api.get("/api/media/franchises").then((res) => setFranchises(res.data));
  }, []);

  const bookFr = franchises.filter((f) => f.books && f.books.length > 0);
  const movieFr = franchises.filter((f) => f.movies && f.movies.length > 0);
  const showFr = franchises.filter((f) => f.shows && f.shows.length > 0);

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", py: 4 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Franchises
      </Typography>

      <Typography variant="h6" sx={{ mt: 3 }}>
        Books
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {bookFr.map((f) => (
          <FranchiseCard key={f.id} franchise={f} />
        ))}
      </Box>
      <Typography variant="h6" sx={{ mt: 3 }}>
        Movies
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {movieFr.map((f) => (
          <FranchiseCard key={f.id} franchise={f} />
        ))}
      </Box>
      <Typography variant="h6" sx={{ mt: 3 }}>
        Shows
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        {showFr.map((f) => (
          <FranchiseCard key={f.id} franchise={f} />
        ))}
      </Box>
    </Box>
  );
}
