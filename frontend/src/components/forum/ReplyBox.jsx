import React, { useState } from "react";
import { Box, TextField, Button, Alert } from "@mui/material";
import api from "../../services/api";

export default function ReplyBox({ topicId, onReplySuccess }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);
    try {
      await api.post(`/api/social/topics/${topicId}/replies`, { message });
      setSuccess(true);
      setMessage("");
      if (onReplySuccess) onReplySuccess();
    } catch (err) {
      setError(
        err?.response?.data?.error || "Eroare la trimiterea răspunsului."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        mt: 3,
        p: 2,
        bgcolor: "#232323",
        borderRadius: 1,
        border: "1px solid #333",
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <TextField
        label="Adaugă un răspuns"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        multiline
        minRows={3}
        maxRows={10}
        fullWidth
        variant="outlined"
        sx={{ bgcolor: "#181818", color: "#fff" }}
        InputLabelProps={{ style: { color: "#bbb" } }}
        InputProps={{
          style: { color: "#fff", borderColor: "#555" },
        }}
        disabled={loading}
      />
      {error && <Alert severity="error">{error}</Alert>}
      {success && <Alert severity="success">Răspuns adăugat!</Alert>}
      <Button
        type="submit"
        variant="contained"
        sx={{ alignSelf: "flex-end" }}
        disabled={loading || !message.trim()}
      >
        Trimite răspunsul
      </Button>
    </Box>
  );
}
