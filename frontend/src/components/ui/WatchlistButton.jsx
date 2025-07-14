import React, { useState, useEffect } from "react";
import { Button, CircularProgress, Tooltip } from "@mui/material";
import BookmarkAddIcon from "@mui/icons-material/BookmarkAdd";
import BookmarkAddedIcon from "@mui/icons-material/BookmarkAdded";
import WatchElementDialogueWindow from "./WatchElementDialogueWindow";
import api from "../../services/api";
import { useAuth } from "../../contexts/AuthContext";

export default function WatchlistButton({ titleID, sx = {} }) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [existingItem, setExistingItem] = useState(null);
  const [loading, setLoading] = useState(false);

  const { user } = useAuth();

  useEffect(() => {
    if (!titleID || !user?.id) return;
    setLoading(true);
    api
      .get(`/api/watchlists/user/${user.id}`)
      .then((res) => {
        const allItems = Object.values(res.data).flat();
        const found = allItems.find((item) => item.titleID === Number(titleID));
        setExistingItem(found || null);
      })
      .catch(() => setExistingItem(null))
      .finally(() => setLoading(false));
  }, [titleID, dialogOpen, user]);

  const handleOpen = () => setDialogOpen(true);
  const handleClose = () => setDialogOpen(false);

  if (loading) return <CircularProgress size={32} sx={sx} />;

  return (
    <>
      <Button
        variant="contained"
        color={existingItem ? "success" : "primary"}
        onClick={handleOpen}
        sx={{ ...sx, fontWeight: 500, minWidth: 200 }}
      >
        {existingItem ? "Edit in Watchlist" : "Add to Watchlist"}
      </Button>
      <WatchElementDialogueWindow
        open={dialogOpen}
        onClose={handleClose}
        titleID={titleID}
        watchlistItemId={existingItem?.id}
        existingFields={existingItem || {}}
        onSuccess={handleClose}
      />
    </>
  );
}
