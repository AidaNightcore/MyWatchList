import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Box,
  Alert,
} from "@mui/material";
import api from "../../services/api";

const STATUS_OPTIONS = [
  { value: "planned", label: "Planned" },
  { value: "watching", label: "Watching" },
  { value: "completed", label: "Completed" },
  { value: "on_hold", label: "On hold" },
  { value: "dropped", label: "Dropped" },
];

const defaultFields = {
  status: "planned",
  score: "",
  progress: 0,
  startDate: null,
  endDate: null,
  favourite: false,
};

export default function WatchElementDialogueWindow({
  open,
  onClose,
  titleID,
  watchlistItemId, // Nou
  existingFields = {}, // Pentru precompletare dacă există
  onSuccess,
}) {
  const [fields, setFields] = useState(defaultFields);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) {
      let prefill =
        existingFields && Object.keys(existingFields).length > 0
          ? { ...defaultFields, ...existingFields }
          : {
              ...defaultFields,
              startDate: new Date().toISOString().substring(0, 10),
            };
      if (!STATUS_OPTIONS.some((opt) => opt.value === prefill.status)) {
        prefill.status = "planned";
      }
      if (!prefill.startDate || prefill.startDate === "")
        prefill.startDate = null;
      if (!prefill.endDate || prefill.endDate === "") prefill.endDate = null;
      setFields(prefill);
      setError(null);
    }
  }, [open]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFields((f) => ({
      ...f,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      let res;
      if (watchlistItemId) {
        // PUT dacă deja există în watchlist
        res = await api.put(`/api/watchlists/items/${watchlistItemId}`, {
          ...fields,
          score: fields.score ? Number(fields.score) : null,
          progress: Number(fields.progress),
        });
      } else {
        // POST dacă nu există
        try {
          res = await api.post("/api/watchlists/items", {
            titleID,
            ...fields,
            score: fields.score ? Number(fields.score) : null,
            progress: Number(fields.progress),
          });
        } catch (err) {
          // Dacă primești 409, extrage itemId și dă PUT automat!
          if (
            err.response &&
            err.response.status === 409 &&
            err.response.data?.itemId
          ) {
            res = await api.put(
              `/api/watchlists/items/${err.response.data.itemId}`,
              {
                ...fields,
                score: fields.score ? Number(fields.score) : null,
                progress: Number(fields.progress),
              }
            );
          } else {
            throw err;
          }
        }
      }
      if (onSuccess) onSuccess(res.data);
      onClose();
    } catch (err) {
      let msg =
        err?.response?.data?.error ||
        (err?.response?.data?.errors && err.response.data.errors.join(", ")) ||
        err?.message ||
        "Unknown error";
      setError(msg);
    }
    setLoading(false);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle>
        {watchlistItemId ? "Edit Watchlist Item" : "Add to Watchlist"}
      </DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Box
          component="form"
          sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
        >
          <TextField
            select
            label="Status"
            name="status"
            value={fields.status}
            onChange={handleChange}
            size="small"
            required
          >
            {STATUS_OPTIONS.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Score"
            name="score"
            value={fields.score}
            onChange={handleChange}
            type="number"
            inputProps={{ min: 1, max: 10 }}
            size="small"
            placeholder="1-10"
          />
          <TextField
            label="Progress"
            name="progress"
            value={fields.progress}
            onChange={handleChange}
            type="number"
            inputProps={{ min: 0 }}
            size="small"
          />
          <TextField
            label="Start Date"
            name="startDate"
            value={fields.startDate}
            onChange={handleChange}
            type="date"
            size="small"
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End Date"
            name="endDate"
            value={fields.endDate}
            onChange={handleChange}
            type="date"
            size="small"
            InputLabelProps={{ shrink: true }}
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={fields.favourite}
                name="favourite"
                onChange={handleChange}
              />
            }
            label="Favourite"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="inherit" disabled={loading}>
          Cancel
        </Button>
        <Button variant="contained" onClick={handleSubmit} disabled={loading}>
          {watchlistItemId ? "Update" : "Add"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
