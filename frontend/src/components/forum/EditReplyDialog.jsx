import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert,
} from "@mui/material";
import api from "../../services/api";

export default function EditReplyDialog({
  open,
  onClose,
  replyId,
  initialMessage,
  onSaveSuccess,
}) {
  const [message, setMessage] = useState(initialMessage || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  React.useEffect(() => {
    setMessage(initialMessage || "");
  }, [initialMessage]);

  const handleSave = async () => {
    setLoading(true);
    setError("");
    try {
      await api.put(`/api/social/replies/${replyId}`, { message });
      setLoading(false);
      if (onSaveSuccess) onSaveSuccess(message);
      onClose();
    } catch (err) {
      setError(err?.response?.data?.error || "Eroare la editarea răspunsului.");
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Editează răspunsul</DialogTitle>
      <DialogContent>
        <TextField
          label="Mesaj"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          multiline
          minRows={3}
          maxRows={10}
          fullWidth
          variant="outlined"
          disabled={loading}
          autoFocus
          sx={{ mt: 1 }}
        />
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Anulează
        </Button>
        <Button
          onClick={handleSave}
          disabled={loading || !message.trim()}
          variant="contained"
        >
          Salvează
        </Button>
      </DialogActions>
    </Dialog>
  );
}
