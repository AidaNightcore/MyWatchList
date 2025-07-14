import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Grid,
  Divider,
  Avatar,
} from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import { useNavigate, Link } from "react-router-dom";
import WatchlistButton from "../../components/ui/WatchlistButton"; // asigură-te că ai acest path

export default function BookPage({ book }) {
  const navigate = useNavigate();
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
        <Box
          sx={{
            minWidth: 220,
            maxWidth: 260,
            flexShrink: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "flex-start",
            p: 3,
          }}
        >
          <Avatar
            variant="rounded"
            src={book.imgURL || "/placeholder.jpg"}
            alt={book.title}
            sx={{
              width: 200,
              height: 300,
              boxShadow: 3,
              bgcolor: "#fff",
              mb: 2,
            }}
          />
          {/* WatchlistButton sub copertă */}
          <WatchlistButton titleID={book.id} />
        </Box>

        {/* Informații detaliu */}
        <CardContent sx={{ flex: 1, p: 3, pt: { xs: 0, md: 3 } }}>
          <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
            {book.title}
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <StarIcon sx={{ color: "#f5c518", mr: 1 }} />
            <Typography variant="h6" sx={{ fontWeight: "bold" }}>
              {book.score ? parseFloat(book.score).toFixed(1) : "–"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body1" color="text.secondary">
              <strong>Publisher:</strong>{" "}
              {book.publisher ? (
                <Chip
                  label={book.publisher}
                  color="primary"
                  variant="outlined"
                  clickable
                  component={Link}
                  to={`/publisher/${book.publisherID}`}
                  sx={{ ml: 1 }}
                />
              ) : (
                "-"
              )}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Pages:</strong> {book.pages || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Published:</strong> {book.publishDate || "-"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
              Genres:
            </Typography>
            {book.genres?.length ? (
              book.genres.map((g) => (
                <Chip
                  key={g}
                  label={g}
                  sx={{ mr: 0.7, mb: 0.7 }}
                  color="info"
                  clickable
                  component={Link}
                  to={`/media?genre=${encodeURIComponent(g)}`}
                />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                No genres.
              </Typography>
            )}
          </Box>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Synopsis
          </Typography>
          <Typography variant="body1" color="text.primary">
            {book.synopsis || <i>No synopsis available.</i>}
          </Typography>
          <Divider sx={{ my: 2 }} />

          {book.crew?.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
                Crew:
              </Typography>
              <Grid container spacing={1}>
                {book.crew.map((c, idx) => (
                  <Grid key={idx} item>
                    <Chip
                      label={`${c.job}: ${c.worker}`}
                      size="small"
                      clickable
                      color="secondary"
                      component={Link}
                      to={`/person/${encodeURIComponent(c.worker)}`}
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}
        </CardContent>
      </Box>
    </Card>
  );
}
