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
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import StarIcon from "@mui/icons-material/Star";
import WatchlistButton from "../../components/ui/WatchlistButton"; // Adjust the path as needed

export default function ShowPage({ show }) {
  return (
    <Card
      sx={{
        maxWidth: 1000,
        margin: "0 auto",
        mt: 6,
        borderRadius: 4,
        boxShadow: 4,
      }}
    >
      <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row" } }}>
        {/* Poster Show */}
        <Box
          sx={{
            minWidth: 220,
            maxWidth: 260,
            flexShrink: 0,
            display: "flex",
            flexDirection: "column", // Asigură vertical
            alignItems: "center",
            justifyContent: "flex-start",
            p: 3,
          }}
        >
          <Avatar
            variant="rounded"
            src={show.imgURL || show.image_url || "/placeholder.jpg"}
            alt={show.title}
            sx={{
              width: 200,
              height: 300,
              boxShadow: 3,
              bgcolor: "#fff",
              mb: 2,
            }}
          />
          {/* WatchlistButton sub copertă */}
          <WatchlistButton titleID={show.id} />
        </Box>

        {/* Show Details */}
        <CardContent sx={{ flex: 1, p: 3, pt: { xs: 0, md: 3 } }}>
          <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
            {show.title}
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <StarIcon sx={{ color: "#f5c518", mr: 1 }} />
            <Typography variant="h6" sx={{ fontWeight: "bold" }}>
              {show.score ? parseFloat(show.score).toFixed(1) : "–"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body1" color="text.secondary">
              <strong>Publisher:</strong> {show.publisher || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Seasons:</strong> {show.seasons?.length || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Franchise:</strong> {show.franchise || "-"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>Published:</strong> {show.publishDate || "-"}
            </Typography>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
              Genres:
            </Typography>
            {show.genres?.length ? (
              show.genres.map((g) => (
                <Chip key={g} label={g} sx={{ mr: 0.7, mb: 0.7 }} />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                No genres.
              </Typography>
            )}
          </Box>
          {show.crew?.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ fontWeight: "bold", mb: 0.5 }}>
                Crew:
              </Typography>
              <Grid container spacing={1}>
                {show.crew.map((c, idx) => (
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
            {show.synopsis || <i>No synopsis available.</i>}
          </Typography>

          {/* Lista sezoanelor și episoadelor (extensibil) */}
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" sx={{ mb: 1 }}>
              Seasons
            </Typography>
            {show.seasons?.length > 0 ? (
              show.seasons.map((season) => (
                <Accordion key={season.id} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle1">
                      Season {season.season_number} ({season.episode_count}{" "}
                      episodes)
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {season.episodes?.length ? (
                      <ul style={{ margin: 0, paddingLeft: 20 }}>
                        {season.episodes.map((ep) => (
                          <li key={ep.id}>
                            <Typography variant="body2">
                              Ep. {ep.number}: {ep.title}
                            </Typography>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No episodes.
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                No seasons found.
              </Typography>
            )}
          </Box>
        </CardContent>
      </Box>
    </Card>
  );
}
