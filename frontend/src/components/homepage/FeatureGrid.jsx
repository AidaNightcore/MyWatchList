import React from "react";
import { Grid, Paper, Typography, Button, Box, Stack } from "@mui/material";
import { Link } from "react-router-dom";
import TopicCard from "../forum/TopicCard";

export default function FeatureGrid({ forumBoard }) {
  // Preluăm câte 1 topic din fiecare categorie dacă există
  const forumTopics = [
    forumBoard.Book?.[0],
    forumBoard.Movie?.[0],
    forumBoard.Show?.[0],
  ].filter(Boolean);

  return (
    <Grid container spacing={3} sx={{ mt: 3 }}>
      <Grid item xs={12} md={4}>
        <Paper
          sx={{
            borderRadius: 3,
            p: 2,
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Typography fontWeight={600} sx={{ mb: 1 }}>
            Forum topics
          </Typography>
          <Stack spacing={2} sx={{ mb: 2 }}>
            {forumTopics.length === 0 && (
              <Typography color="text.secondary" align="center">
                No forum topics found.
              </Typography>
            )}
            {forumTopics.map((topic, idx) =>
              topic ? (
                <TopicCard
                  key={topic.id}
                  id={topic.id}
                  title={topic.title}
                  imgURL={topic.imgURL}
                  firstReply={topic.firstReply}
                  mediaId={topic.mediaId}
                  // Poți adăuga props suplimentare pentru detalii topic
                />
              ) : null
            )}
          </Stack>
          <Button
            variant="contained"
            color="secondary"
            component={Link}
            to="/forum"
            fullWidth
            sx={{ mt: "auto" }}
          >
            Go to Forums
          </Button>
        </Paper>
      </Grid>
    </Grid>
  );
}
