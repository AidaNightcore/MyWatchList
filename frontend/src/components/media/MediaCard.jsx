import React, { useState, useEffect } from "react";
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
} from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import { Link } from "react-router-dom";
import WatchElementDialogueWindow from "../ui/WatchElementDialogueWindow";
import { useWatchlist } from "../../contexts/WatchlistContext";

const POSTER_RATIO = 1.5;

const statusLabel = {
  planned: "Planned",
  watching: "Watching",
  completed: "Completed",
  on_hold: "On Hold",
  dropped: "Dropped",
};

const MediaCard = ({ media, watchlistItems }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const { refreshWatchlist } = useWatchlist();

  // Sincronizează butonul cu starea actuală din watchlist
  const item = watchlistItems?.find((el) => el.titleID === media.id);
  let watchlistStatus = item?.status;
  let watchlistItemId = item?.id;

  let buttonLabel = "Add to Watchlist";
  if (watchlistStatus && statusLabel[watchlistStatus]) {
    buttonLabel = statusLabel[watchlistStatus];
  }

  // Afișează anul dacă există publishDate
  const year = media.publishDate
    ? new Date(media.publishDate).getFullYear()
    : "";

  // Culoarea butonului (opțional, poți adapta după status)
  let buttonColor = "primary";
  if (watchlistStatus === "completed") buttonColor = "success";
  else if (watchlistStatus === "watching") buttonColor = "info";
  else if (watchlistStatus === "on_hold") buttonColor = "warning";
  else if (watchlistStatus === "dropped") buttonColor = "error";

  return (
    <>
      <Card
        sx={{
          width: { xs: 130, sm: 150, md: 180, lg: 220 },
          display: "flex",
          flexDirection: "column",
          borderRadius: 2,
          overflow: "hidden",
          boxShadow: 2,
          background: "#fff",
          height: {
            xs: 130 * POSTER_RATIO + 100,
            sm: 150 * POSTER_RATIO + 110,
            md: 180 * POSTER_RATIO + 120,
            lg: 220 * POSTER_RATIO + 130,
          },
        }}
      >
        <CardMedia
          component="img"
          image={
            media.image_url ||
            media.imgURL ||
            (media.details && media.details.imgURL) ||
            "/placeholder.jpg"
          }
          alt={media.title}
          sx={{
            width: "100%",
            height: {
              xs: 130 * POSTER_RATIO,
              sm: 150 * POSTER_RATIO,
              md: 180 * POSTER_RATIO,
              lg: 220 * POSTER_RATIO,
            },
            objectFit: "cover",
            backgroundColor: "#ddd",
          }}
        />
        <CardContent
          sx={{
            flex: 1,
            p: 1.5,
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
            background: "#fff",
          }}
        >
          <Typography
            variant="subtitle1"
            sx={{
              fontWeight: "bold",
              mb: 0.5,
              color: "#181818",
              lineHeight: 1.15,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            component={Link}
            to={`/media/${media.id}`}
            style={{ textDecoration: "none" }}
          >
            {media.title}
          </Typography>
          <Typography sx={{ fontSize: 14, color: "#222", mb: 0.2 }}>
            {media.type}
            {media.score !== undefined && (
              <>
                &nbsp;
                <StarIcon
                  sx={{
                    fontSize: 16,
                    verticalAlign: "middle",
                    color: "#f5c518",
                    ml: 0.5,
                    mb: "2px",
                  }}
                />
                {parseFloat(media.score).toFixed(1)}
              </>
            )}
          </Typography>
          <Typography sx={{ fontSize: 13, color: "#222" }}>{year}</Typography>

          <Button
            variant="contained"
            color={buttonColor}
            sx={{ mt: 1, borderRadius: 2, width: "100%" }}
            onClick={() => setDialogOpen(true)}
          >
            {buttonLabel}
          </Button>
        </CardContent>
      </Card>
      <WatchElementDialogueWindow
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        titleID={media.id}
        watchlistItemId={watchlistItemId}
        existingFields={item}
        // După adăugare/actualizare, resetează dialogul și dă refresh la watchlist pentru update instant
        onSuccess={() => {
          setDialogOpen(false);
          refreshWatchlist();
        }}
      />
    </>
  );
};

export default MediaCard;
