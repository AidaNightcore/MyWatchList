import React, { useState } from "react";
import {
  Box,
  Tabs,
  Tab,
  Grid,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import MediaCard from "../../components/media/MediaCard";
import { useWatchlist } from "../../contexts/WatchlistContext";

const STATUS = [
  { key: "watching", label: "Watching" },
  { key: "planned", label: "Planned" },
  { key: "completed", label: "Completed" },
  { key: "on_hold", label: "On Hold" },
  { key: "dropped", label: "Dropped" },
];

export default function WatchlistPage() {
  const { watchlist, loading, error } = useWatchlist();
  const [tab, setTab] = useState("watching");

  return (
    <Box sx={{ width: "100%", p: { xs: 1, sm: 2, md: 3 } }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 2 }}>
        My Watchlist
      </Typography>
      <Tabs
        value={tab}
        onChange={(e, v) => setTab(v)}
        sx={{ mb: 3, borderBottom: 1, borderColor: "divider" }}
        variant="scrollable"
        scrollButtons="auto"
      >
        {STATUS.map((s) => (
          <Tab
            key={s.key}
            value={s.key}
            label={s.label}
            sx={{
              fontWeight: 600,
              fontSize: 16,
              textTransform: "none",
              minWidth: 120,
            }}
          />
        ))}
      </Tabs>

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 6 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error">{String(error)}</Alert>
      ) : (watchlist[tab] || []).length === 0 ? (
        <Typography color="text.secondary" sx={{ mt: 6, textAlign: "center" }}>
          No items in this list.
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {watchlist[tab].map((item) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={item.id}>
              <MediaCard
                media={formatMediaForCard(item)}
                watchlistItems={[item]}
              />
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

function formatMediaForCard(item) {
  const det = item.element_details || {};
  return {
    id: item.titleID,
    title: item.title?.name || det.title || "",
    type: item.title?.type || det.type || "",
    imgURL: det.imgURL || det.image_url || det.img_url || "",
    score: item.score ?? det.score,
    publishDate: det.publishDate || det.publish_date || "",
    genres: item.title?.genres || det.genres || [],
    details: det,
  };
}
