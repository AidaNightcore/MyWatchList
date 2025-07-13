import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Divider,
  Avatar,
  Grid,
} from "@mui/material";
import StarIcon from "@mui/icons-material/Star";

export default function MoviePage({ movie }) {
  return (
    <Card
      sx={{
        maxWidth: 900,
        margin: "0 auto",
        mt: 6,
        borderRadius: 4,
        boxShadow: 4,
      }}
    >
      <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row" } }}>
        {/* Poster Movie */}
        <Box
          sx={{
            minWidth: 220,
            maxWidth: 260,
            flexShrink: 0,
            display: "flex",
            alignItems: "flex-start",
            justifyContent: "center",
            p: 3,
          }}
        >
          <Avatar
            variant="rounded"
            src={movie.imgURL || movie.image_url || "/placeholder.jpg"}
            alt={movie.title}
            sx={{
              width: 200,
              height: 300,
              boxShadow: 3,
              bgcolor: "#fff",
            }}
          />
        </Box>

        {/* Movie Details */}
        <CardContent sx={{ flex: 1, p: 3, pt: { xs: 0, md: 3 } }}>
          <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
            {movie.title}
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <StarIcon sx={{ color: "#f5c518", mr: 1 }} />
            <Typography variant="h6" sx={{ fontWeight: "bold" }}>
              {movie.score ? parseFloat(movie.score).toFixed(1) : "–"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body1" color="text.secondary">
              <strong>Publisher:</strong> {movie.publisher || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Released:</strong> {movie.publishDate || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Duration:</strong>{" "}
              {movie.duration ? `${movie.duration} min` : "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>IMDb ID:</strong> {movie.imdbID || "-"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
              Genres:
            </Typography>
            {movie.genres?.length ? (
              movie.genres.map((g) => (
                <Chip key={g} label={g} sx={{ mr: 0.7, mb: 0.7 }} />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                No genres.
              </Typography>
            )}
          </Box>
          {movie.crew?.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
                Crew:
              </Typography>
              <Grid container spacing={1}>
                {movie.crew.map((c, idx) => (
                  <Grid key={idx} item>
                    <Chip label={`${c.job}: ${c.worker}`} size="small" />
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" sx={{ mb: 1 }}>
            Synopsis
          </Typography>
          <Typography variant="body1" color="text.primary">
            {movie.synopsis || <i>No synopsis available.</i>}
          </Typography>
        </CardContent>
      </Box>
    </Card>
  );
}
