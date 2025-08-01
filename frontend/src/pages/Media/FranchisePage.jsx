import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Divider,
  Box,
} from "@mui/material";
import api from "../../services/api";
import MediaCard from "../../components/media/MediaCard";

export default function FranchisePage() {
  const { id } = useParams();
  const [franchise, setFranchise] = useState(null);

  useEffect(() => {
    api
      .get(`/api/media/franchises/${id}`)
      .then((res) => setFranchise(res.data));
  }, [id]);

  if (!franchise) return <div>Loading...</div>;

  return (
    <Box sx={{ maxWidth: 1100, mx: "auto", mt: 4 }}>
      <Card sx={{ mb: 3, p: 2 }}>
        <CardContent>
          <Typography variant="h4" fontWeight="bold">
            {franchise.title}
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Box sx={{ display: "flex", gap: 2, mb: 1, flexWrap: "wrap" }}>
            <Chip label={`Books: ${franchise.books.length}`} color="info" />
            <Chip
              label={`Movies: ${franchise.movies.length}`}
              color="secondary"
            />
            <Chip label={`Shows: ${franchise.shows.length}`} color="success" />
          </Box>
          {franchise.synopsis && (
            <Typography variant="body1" sx={{ mt: 2 }}>
              {franchise.synopsis}
            </Typography>
          )}
        </CardContent>
      </Card>
      <Typography variant="h5" fontWeight="bold" sx={{ mt: 2, mb: 1 }}>
        Books
      </Typography>
      <Grid container spacing={2}>
        {franchise.books.map((book) => (
          <Grid item xs={12} sm={6} md={3} key={book.id}>
            <MediaCard media={book} />
          </Grid>
        ))}
      </Grid>
      <Typography variant="h5" fontWeight="bold" sx={{ mt: 4, mb: 1 }}>
        Movies
      </Typography>
      <Grid container spacing={2}>
        {franchise.movies.map((movie) => (
          <Grid item xs={12} sm={6} md={3} key={movie.id}>
            <MediaCard media={movie} />
          </Grid>
        ))}
      </Grid>
      <Typography variant="h5" fontWeight="bold" sx={{ mt: 4, mb: 1 }}>
        Shows
      </Typography>
      <Grid container spacing={2}>
        {franchise.shows.map((show) => (
          <Grid item xs={12} sm={6} md={3} key={show.id}>
            <MediaCard media={show} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
