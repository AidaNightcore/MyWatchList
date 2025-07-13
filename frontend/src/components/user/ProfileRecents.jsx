import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import MediaCard from "../media/MediaCard";

export default function ProfileRecents({ activity }) {
  const safeActivity = Array.isArray(activity) ? activity : [];
  return (
    <Card elevation={2} sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Activitate Recentă
        </Typography>
        {safeActivity.length === 0 ? (
          <Typography>Nicio activitate recentă.</Typography>
        ) : (
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
            {safeActivity.map((media, idx) => (
              <MediaCard
                key={media.id || idx}
                media={media}
                watchlistItems={[]}
              />
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
